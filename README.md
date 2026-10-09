# Reason plugins for Claude Code and Codex

Connect a coding agent to your Reason workspace at **https://mcp.reasonmachines.com/mcp**.
Sign in through your browser, choose a workspace, review permissions, and connect.
The plugin contains no API key, credential, local executable or hook.

## Install the Reason plugin

### Claude Code

```sh
claude plugin marketplace add reason-machines/reason-plugins
claude plugin install reason@reason
```

Open `/mcp` in Claude Code and authenticate Reason when prompted.

### Codex

```sh
codex plugin marketplace add reason-machines/reason-plugins
codex plugin add reason@reason
```

Enable Reason and complete the browser authentication prompt. Reload the client if
its tool list was already open when you installed the plugin.

These are Reason Machines' publisher-owned plugins. Installation does not depend
on acceptance into Anthropic's curated marketplace or OpenAI's public directory;
those services review and approve listings separately.

In the Codex app, open **Plugins → Add → Add plugin marketplace**, paste
`https://github.com/reason-machines/reason-plugins`, and add the marketplace. Leave
**Git ref** and **Sparse paths** empty. Select **Reason MCP → Install**, then
complete the browser authentication prompt. No separate MCP configuration is needed.

The marketplace identifier is `reason`.

## More from Reason

- [reason-agent](https://github.com/reason-machines/reason-agent): what Reason Agent is, how to use it, releases and benchmarks.
- [reason-cli](https://github.com/reason-machines/reason-cli): the `reason` command line.
- [reason-marketplace](https://github.com/reason-machines/reason-marketplace): every plugin and connector Reason can use inside your workspace.

## Connect without a plugin

### Claude Code

```sh
claude mcp add --transport http reason https://mcp.reasonmachines.com/mcp
```

Then open `/mcp` and authenticate Reason.

### Codex

```sh
codex mcp add reason --url https://mcp.reasonmachines.com/mcp
codex mcp login reason
```

### Other MCP clients

Choose a remote **Streamable HTTP** server with URL
`https://mcp.reasonmachines.com/mcp` and OAuth authentication. For example:

```json
{
  "mcpServers": {
    "reason": {
      "type": "http",
      "url": "https://mcp.reasonmachines.com/mcp"
    }
  }
}
```

For headless integrations, a scoped Reason API key can be provided by your
client's secret manager as an Authorization bearer header. Never put a token in
this repository, a prompt, a shared configuration file, or a URL. OAuth credentials
are audience-bound: a REST login cannot be reused as an MCP login.

## Try it

- “Show my Reason projects and recent sessions.”
- “Create a project for this repository and add these instructions.”
- “Find my session about the billing bug and show its latest messages.”
- “Archive this project, then restore it.”

The tools follow the active public v3 contract and your granted scopes. Start with
`getSelf` to check the connected workspace. Path and query arguments are top-level;
JSON request bodies go in `body`. Workspace selection is automatic and pinned to
the connection.

For example, `listProjects` accepts `{"archived":"include"}`. `updateProject`
accepts `{"projectId":"…","body":{"project_md":{"content":"…","expected_revision":1}}}`.
Read the current `project_document.revision` with `getProject` first. A stale
revision returns 409, preserving the newer instructions.

Creating a session starts asynchronous work; inspect its status before assuming
it finished. Follow pagination cursors for complete lists. Tool results preserve
API status and data, including permission errors, conflicts and rate limits.

All active v3 operations are represented. Deprecated compatibility aliases and
retired routes are omitted. File uploads take `body.filename` and
`body.data_base64`, limited to 1 MiB; use REST for larger uploads. Downloads return
an authorized `download_url`, never forward your Reason bearer to that URL.
Large results are bounded at 2 MiB; request a smaller page or use REST.

## Permissions and disconnection

Each connection is bound to the workspace chosen during consent. Tools reuse the
API's scope, membership, role, private-project and IP access checks. Stored secrets
remain write-only. MCP does not grant arbitrary control of your Mac or bypass a
service's OAuth approval. Revoking a connection or removing its workspace
membership stops access. Use your client's disconnect/logout controls and Reason's
connected-app controls when the integration is no longer needed.

## Support and validation

Contact [Reason Machines](mailto:contact@reasonmachines.com).
See [SECURITY.md](SECURITY.md) for vulnerability reporting.

```sh
claude plugin validate --strict plugins/reason
claude plugin validate --strict .claude-plugin/marketplace.json
```

Validate the Codex manifest with the Codex plugin validator. Test installations in
an isolated client configuration directory, preserving personal installations.
Production connection and directory approval are separate from manifest validation.
