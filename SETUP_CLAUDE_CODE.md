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
    "CLAUDE_CODE_SUBAGENT_MODEL": "deepseek-v4-flash"
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
    "CLAUDE_CODE_SUBAGENT_MODEL": "deepseek-v4-flash"
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
  superpowers playwright typescript-lsp jdtls-lsp \
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
    "superpowers", "playwright", "typescript-lsp", "jdtls-lsp",
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

## Bright Data CLI (free tier)

The Bright Data CLI (`brightdata` / `bdata`) authenticates with `bdata login` — no API token needed in `settings.json`. Sign up on the Bright Data website (free tier available), then run:

```bash
bdata login            # browser OAuth — auto-creates cli_unlocker + cli_browser zones
# or, headless/SSH:
bdata login --device
# or, non-interactive with an API key from your dashboard:
bdata login --api-key "paste-your-token-here"
```

Verify with `bdata config` or `bdata budget`.