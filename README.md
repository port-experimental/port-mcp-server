# Port MCP Server

A Model Context Protocol (MCP) server for the [Port.io API](https://www.getport.io/), enabling Claude to interact with Port.io's developer platform capabilities.

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

## Capabilities

### Agent Tools

1. `trigger_port_agent`
   - Trigger the Port.io AI agent with a prompt and wait for completion
   - Required inputs:
     - `prompt` (string): The prompt to send to the Port.io AI agent
   - Returns: Agent response with status, output, and any required actions
   - Note: The agent may return action URLs for bug reports or other tasks that require user interaction

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
   - Returns: Formatted text representation of the specified blueprint

### Entity Tools

Will be added in the future.

## Development

### Local Setup

1. Create and activate a virtual environment:
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

3. Run the server locally:
```bash
python -m src.mcp_server_port --client-id "CLIENT_ID" --client-secret "CLIENT_SECRET" --region "REGION"
```

### Publishing a New Version

There are two ways to publish a new version: manually following all steps, or using the automated Make commands.

#### Manual Process

1. Ensure you're on the main branch and it's up to date:
```bash
git checkout main
git pull origin main
```

2. Merge the feature/release branch with changelog updates:
```bash
git merge feature/your-release-branch
```

3. Update version in `pyproject.toml`

4. Commit version bump:
```bash
git add pyproject.toml
git commit -m "chore: bump version to X.Y.Z"
git push origin main
```

5. Create and push a new Git tag:
```bash
git tag -a vX.Y.Z -m "Release version X.Y.Z"
git push origin vX.Y.Z
```

6. Build and publish to PyPI:
```bash
# Ensure you have the latest build tools
pip install --upgrade build twine

# Build the package
python -m build

# Check the package
twine check dist/*

# Upload to PyPI
twine upload dist/mcp_server_port-X.Y.Z*
```

7. Create a GitHub release:
   - Go to the repository's Releases page
   - Click "Create new release"
   - Select the tag you just pushed
   - Title it "Release X.Y.Z"
   - Include the changelog in the description
   - Publish the release

#### Automated Process

You can use the provided Makefile commands to automate the release process:

```bash
# Update version and create release
make release VERSION=X.Y.Z

# Or run steps individually:
make bump-version VERSION=X.Y.Z  # Updates pyproject.toml
make tag VERSION=X.Y.Z          # Creates and pushes git tag
make build                      # Builds the package
make publish                    # Publishes to PyPI
```

Note: The automated process still requires you to manually create the GitHub release with changelog information.

### Troubleshooting

If you encounter authentication errors, verify that:
1. Your Port credentials are correctly set in the arguments
2. You have the necessary permissions
3. The credentials are properly copied to your configuration

## License

This MCP server is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.