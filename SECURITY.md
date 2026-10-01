# Security policy

## Scope

This repository contains declarative Reason MCP plugins for Codex and Claude Code.
Packages must remain secretless: do not add API keys, client secrets, Authorization
headers, cookies, local hooks, or executable setup scripts.

The plugins configure the remote Streamable HTTP server at
`https://mcp.reasonmachines.com/mcp`. Authentication uses the client's browser OAuth
flow. The user chooses a workspace and reviews permissions before connecting.
Clients manage credentials; the plugin package never contains them.

## Reporting a vulnerability

Please report security issues privately at [security@reasonmachines.com](mailto:security@reasonmachines.com).
Do not include secrets, access tokens, or customer data in the initial report.

## Supported release

Only the default branch and the marketplace packages published from it are
supported. The MCP retains the public API's scope and workspace access checks.
