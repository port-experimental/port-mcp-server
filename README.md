# Port MCP Server

A Model Context Protocol (MCP) server for the [Port.io API](https://www.getport.io/), enabling Claude to interact with Port.io's developer platform capabilities using natural language.

## What You Can Do With Port MCP

Transform how you work with Port.io using natural language:

### Find Information Quickly
- **Get entity details** - "Who is the owner of service X?"
- **Check on-call status** - "Who is on call right now?"
- **Get catalog insights** - "How many services do we have in production?"

### Analyze Scorecards 
- **Identify weak points** - "Which services are failing for the gold level and why?"
- **Get compliance status** - "Show me all services that don't meet our security requirements"
- **Improve quality** - "What do I need to fix to reach the next scorecard level?"

### Create Resources
- **Build scorecards** - "Create a new scorecard called 'Security Posture' with levels Basic, Silver, and Gold"
- **Define rules** - "Add a rule that requires services to have a team owner to reach the Silver level"
- **Setup quality gates** - "Create a rule that checks if services have proper documentation"

We're continuously expanding Port MCP's capabilities. Have a suggestion? We'd love to hear your feedback on our [roadmap](https://roadmap.getport.io/ideas)!

## Installation

### Obtain your Port credentials
1. Create a Port.io Account:
   - Visit [Port.io](https://www.port.io/)
   - Sign up for an account if you don't have one

2. Create an API Key:
   - Navigate to your Port.io dashboard
   - Go to Settings > Credentials
   - Save both the Client ID and Client Secret

### Claude Desktop

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "port": {
      "command": "uvx",
      "args": [
        "mcp-server-port@0.1.4",
        "--client-id", "YOUR_CLIENT_ID",
        "--client-secret", "YOUR_CLIENT_SECRET",
        "--region", "REGION" # US or EU
      ]
    }
  }
} 
```

### Cursor

1. Make sure `uvx` is installed:
```bash
pip install uvx
```

2. Get its location:
```bash
which uvx
# Example output: /Users/janedoe/.local/bin/uvx
```

3. Create a script to run the server:
```bash
# run-port-mcp.sh

cd /Users/janedoe/.local/bin/uvx

# Run the server with the specified credentials
./.venv/bin/uvx mcp-server-port@0.1.4 --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET --region YOUR_REGION
```

4. Make it executable:
```bash
chmod +x /path/to/your/file/run-port-mcp.sh
```

5. Configure in Cursor settings:
   - Go to Cursor settings > MCP Servers
   - Configure with:
     * Name - `Port`
     * Type - `Command`
     * Command - `/path/to/your/file/run-port-mcp.sh`

![Cursor MCP Screenshot](/assets/cursor_mcp_screenshot.png)

## Available Tools

### Blueprint Tools

1. `get_blueprints`
   - Retrieve a list of all blueprints from Port
   - Optional inputs:
     - `detailed` (boolean, default: false): Return complete schema details for each blueprint
   - Returns: Formatted text representation of all available blueprints

2. `get_blueprint`
   - Retrieve information about a specific blueprint by its identifier
   - Required inputs:
     - `blueprint_identifier` (string): The unique identifier of the blueprint to retrieve
   - Optional inputs:
     - `detailed` (boolean, default: true): Return complete schema details

### Scorecard Tools

1. `get_scorecards`
   - Retrieve all scorecards from Port
   - Optional inputs:
     - `detailed` (boolean, default: false): Return complete scorecard details

2. `get_scorecard`
   - Retrieve information about a specific scorecard by its identifier
   - Required inputs:
     - `scorecard_id` (string): The unique identifier of the scorecard to retrieve
     - `blueprint_id` (string, optional): The identifier of the blueprint the scorecard belongs to

3. `create_scorecard`
   - Create a new scorecard for a specific blueprint
   - Required inputs:
     - `blueprint_id` (string): The identifier of the blueprint to create the scorecard for
     - `identifier` (string): The unique identifier for the new scorecard
     - `title` (string): The display title of the scorecard
     - `levels` (list): List of levels for the scorecard
   - Optional inputs:
     - `rules` (list): List of rules for the scorecard
     - `description` (string): Description for the scorecard

## Feedback and Roadmap

We're continuously improving Port MCP and would love to hear from you! Please share your feedback and feature requests on our [roadmap page](https://roadmap.getport.io/ideas).

## Troubleshooting

If you encounter authentication errors, verify that:
1. Your Port credentials are correctly set in the arguments
2. You have the necessary permissions
3. The credentials are properly copied to your configuration

## License

This MCP server is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.