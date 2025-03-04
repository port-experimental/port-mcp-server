#!/usr/bin/env python3

import asyncio
import sys
import click
from mcp.server.fastmcp import FastMCP
from mcp_server_port.client import PortClient
from mcp_server_port.utils import setup_logging, PortError

# Initialize logging
logger = setup_logging()

# Initialize FastMCP server
mcp = FastMCP("Port")

# Initialize Port.io client
port_client = PortClient()

def create_port_tools(client_id: str, client_secret: str):
    @mcp.tool()
    async def get_port_token() -> str:
        """Get a Port.io authentication token."""
        try:
            token = await port_client.get_token(client_id, client_secret)
            return token.to_text()
        except Exception as e:
            return f"❌ Error getting Port.io token: {str(e)}"

    @mcp.tool()
    async def trigger_port_agent(prompt: str) -> str:
        """Trigger the Port.io AI agent with a prompt and wait for completion."""
        try:
            # Get token
            token = await port_client.get_token(client_id, client_secret)
            
            # Trigger agent
            response = await port_client.trigger_agent(token.access_token, prompt)
            
            # Get identifier from response
            identifier = (
                response.get("invocation", {}).get("identifier") or
                response.get("identifier") or
                response.get("id") or
                response.get("invocationId")
            )
            
            if not identifier:
                return "❌ Error: Could not get invocation identifier from response"
            
            # Poll for completion
            max_attempts = 30
            attempt = 0
            while attempt < max_attempts:
                status = await port_client.get_invocation_status(token.access_token, identifier)
                if status.status.lower() in ["completed", "failed", "error"]:
                    return status.to_text()
                await asyncio.sleep(2)
                attempt += 1
            
            return f"⏳ Operation timed out. You can check the status later with identifier: {identifier}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

async def cleanup():
    """Cleanup resources."""
    try:
        await port_client.close()
        logger.info("Port client closed successfully")
    except Exception as e:
        logger.error(f"Error closing Port client: {e}")

@click.command()
@click.option(
    "--client-id",
    required=True,
    help="Port.io client ID",
)
@click.option(
    "--client-secret",
    required=True,
    help="Port.io client secret",
)
def main(client_id: str, client_secret: str):
    """Main entry point."""
    try:
        logger.info("Starting Port MCP server...")
        
        # Create tools with credentials
        create_port_tools(client_id, client_secret)
        
        # Run the server
        mcp.run(transport='stdio')
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
        asyncio.run(cleanup())
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        print(f"Error: {e}", file=sys.stderr)
        asyncio.run(cleanup())
        sys.exit(1)

if __name__ == "__main__":
    main() 