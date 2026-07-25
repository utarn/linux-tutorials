# Claude Code Settings

Generate a placeholder `settings.json` for Claude Code with the following configuration:

## Linux / macOS

```bash
mkdir -p ~/.claude && cat > ~/.claude/settings.json << 'EOF'
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "",
    "ANTHROPIC_BASE_URL": "https://api.modelharbor.com",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "glm-max-claudecode",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-max-claudecode",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-v4-flash",
    "CLAUDE_CODE_SUBAGENT_MODEL": "deepseek-v4-flash",
    "BRIGHT_DATA_API_TOKEN": ""
  },
  "alwaysThinkingEnabled": true,
  "effortLevel": "xhigh",
  "tui": "default",
  "skipDangerousModePermissionPrompt": true,
  "autoCompactEnabled": true
}
EOF
```

## Windows (PowerShell)

```powershell
$dir = "$env:USERPROFILE\.claude"
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
@'
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "",
    "ANTHROPIC_BASE_URL": "https://api.modelharbor.com",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "glm-max-claudecode",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-max-claudecode",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-v4-flash",
    "CLAUDE_CODE_SUBAGENT_MODEL": "deepseek-v4-flash",
    "BRIGHT_DATA_API_TOKEN": ""
  },
  "alwaysThinkingEnabled": true,
  "effortLevel": "xhigh",
  "tui": "default",
  "skipDangerousModePermissionPrompt": true,
  "autoCompactEnabled": true
}
'@ | Set-Content -Path "$env:USERPROFILE\.claude\settings.json" -NoNewline
```

## macOS / Linux — Install plugins

```bash
for plugin in \
  pyright-lsp clangd-lsp rust-analyzer-lsp gopls-lsp frontend-design \
  superpowers playwright brightdata-plugin typescript-lsp jdtls-lsp \
  php-lsp kotlin-lsp swift-lsp lua-lsp ruby-lsp liquid-lsp \
  code-review skill-creator github claude-md-management csharp-lsp \
  code-simplifier feature-dev security-guidance; do
    claude plugin install "${plugin}@claude-plugins-official" --scope local
done
```

## Windows (PowerShell) — Install plugins

```powershell
$plugins = @(
    "pyright-lsp", "clangd-lsp", "rust-analyzer-lsp", "gopls-lsp", "frontend-design",
    "superpowers", "playwright", "brightdata-plugin", "typescript-lsp", "jdtls-lsp",
    "php-lsp", "kotlin-lsp", "swift-lsp", "lua-lsp", "ruby-lsp", "liquid-lsp",
    "code-review", "skill-creator", "github", "claude-md-management", "csharp-lsp",
    "code-simplifier", "feature-dev", "security-guidance"
)

foreach ($plugin in $plugins) {
    claude plugin install "${plugin}@claude-plugins-official" --scope local
}
```

## macOS / Linux — Install utarn skills

```bash
claude plugin marketplace add utarn/engineer-skills
claude plugin install utarn-skills@utarn
```

## Windows (PowerShell) — Install utarn skills

```powershell
claude plugin marketplace add utarn/engineer-skills
claude plugin install utarn-skills@utarn
```

## Bright Data API key (free tier)

The Bright Data MCP server needs an API token. Sign up on the Bright Data website (free tier available), create a zone, and copy its API token into `BRIGHT_DATA_API_TOKEN` in your `settings.json` `env` block — or export it in your shell.

**Bash** — add to `~/.bashrc` / `~/.zshrc`:
```bash
export BRIGHT_DATA_API_TOKEN="paste-your-token-here"
```

**PowerShell** — add to your profile:
```powershell
$env:BRIGHT_DATA_API_TOKEN = "paste-your-token-here"
```