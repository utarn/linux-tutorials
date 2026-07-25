# Quick Setup

Get Claude Code working with all the tools you need in one shot: the engineer-skills plugin, Context7 for live docs, and Bright Data for web scraping (CLI + skill).

Pick your shell and run the **install** block once. That gives you a `ccc` / `cccc` pair to launch Claude Code, plus a `quicksetup` function that wires up the skills. Then just type `quicksetup` to run it.

> `ccc` and `cccc` are convenience wrappers around `claude` — they skip the per-command permission prompt and continue the last session, matching the `--dangerously-skip-permissions` flow the rest of this repo assumes. They call `claude` directly, so they work for anyone, not just the author's private aliases.

## Windows prerequisites (run once)

Before installing Claude Code on Windows, install Git for Windows, PowerShell 7, and Windows Terminal with winget, then make PowerShell 7 the default profile for Windows Terminal:

```powershell
winget install --id Git.Git -e
winget install --id Microsoft.PowerShell -e
winget install --id Microsoft.WindowsTerminal -e

# Set PowerShell 7 as the default profile in Windows Terminal
$settingsPath = "$env:LOCALAPPDATA\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"
$ps7 = (Get-Command pwsh).Source
$settings = Get-Content $settingsPath -Raw | ConvertFrom-Json
($settings.profiles.list | Where-Object { $_.commandline -eq $ps7 }).guid | ForEach-Object { $settings.defaultProfile = $_ }
$settings | ConvertTo-Json -Depth 10 | Set-Content $settingsPath
```

## Install Claude Code

Install the `claude` CLI first (the rest of this guide calls it). Pick one method.

**Linux prerequisites** — on Debian/Ubuntu, make sure Git (and curl) are installed before the native installer:

```bash
sudo apt update && sudo apt install -y git curl
```

**Native installer (recommended)** — macOS / Linux / WSL:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows PowerShell:**

```powershell
irm https://claude.ai/install.ps1 | iex
```

**Windows CMD:**

```batch
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

Alternatives: `brew install --cask claude-code` (macOS), `winget install Anthropic.ClaudeCode` (Windows), or `npm install -g @anthropic-ai/claude-code` (needs Node.js 22+). See the [Claude Code setup docs](https://code.claude.com/docs/en/setup) for Linux package-manager (apt/dnf/apk) install and version pinning.

Verify, then log in:

```bash
claude --version      # prints e.g. 2.1.211 (Claude Code)
claude                # opens an interactive session and walks you through login
```

## Bash (Linux / macOS)

Add this to `~/.bashrc` (or `~/.zshrc` on macOS), then start a new shell:

```bash
# Convenience launchers for Claude Code
ccc()  { claude --dangerously-skip-permissions "$@"; }
cccc() { claude --dangerously-skip-permissions --continue "$@"; }

# One-shot setup: engineer-skills plugin + Context7 + Bright Data (CLI + skill)
quicksetup() {
  # 1. engineer-skills plugin
  claude plugin marketplace add utarn/engineer-skills
  claude plugin install utarn-skills@utarn

  # 2. Context7 — live library docs
  npx ctx7@latest setup

  # 3. Bright Data — CLI / MCP server (needs an API token, see below)
  claude mcp add brightdata -- npx -y @brightdata/mcp

  # 4. Bright Data — skill surface inside Claude Code
  claude plugin install brightdata-plugin@claude-plugins-official --scope local
}
```

Run it:

```bash
quicksetup
```

## PowerShell (Windows)

### Create / open your PowerShell profile

If the profile file doesn't exist yet, create it and open it in Notepad:

```powershell
if (!(Test-Path -Path $PROFILE)) { New-Item -ItemType File -Path $PROFILE -Force }; notepad $PROFILE
```

Add this to your PowerShell profile, then open a new terminal:

```powershell
# Convenience launchers for Claude Code
function ccc  { claude --dangerously-skip-permissions @args }
function cccc { claude --dangerously-skip-permissions --continue @args }

# One-shot setup: engineer-skills plugin + Context7 + Bright Data (CLI + skill)
function quicksetup {
  # 1. engineer-skills plugin
  claude plugin marketplace add utarn/engineer-skills
  claude plugin install utarn-skills@utarn

  # 2. Context7 — live library docs
  npx ctx7@latest setup

  # 3. Bright Data — CLI / MCP server (needs an API token, see below)
  claude mcp add brightdata -- npx -y @brightdata/mcp

  # 4. Bright Data — skill surface inside Claude Code
  claude plugin install brightdata-plugin@claude-plugins-official --scope local
}
```

Run it:

```powershell
quicksetup
```

## Bright Data API key (free tier)

The Bright Data MCP server needs an API token to talk to Bright Data's scraping network.

1. Go to the Bright Data website and sign up — there's a **free tier** you can use without a paid plan.
2. Create a zone (Web Unlocker is the general-purpose one) and copy its API token.
3. Export it before you launch Claude so the MCP server can read it:

   **Bash** — add to `~/.bashrc` / `~/.zshrc`:
   ```bash
   export BRIGHT_DATA_API_TOKEN="paste-your-token-here"
   ```

   **PowerShell** — add to your profile:
   ```powershell
   $env:BRIGHT_DATA_API_TOKEN = "paste-your-token-here"
   ```

Start a new shell (or reload your profile) after exporting the token, then run `ccc` / `cccc`.

## What each step does

| Step | Command | Effect |
|---|---|---|
| 1 | `claude plugin marketplace add utarn/engineer-skills` | Register this repo as a Claude Code plugin marketplace. |
| 2 | `claude plugin install utarn-skills@utarn` | Install the whole engineer-skills bundle as a managed, auto-updating plugin. |
| 3 | `npx ctx7@latest setup` | Install Context7 into your coding agent so it can fetch live library docs. |
| 4 | `claude mcp add brightdata -- npx -y @brightdata/mcp` | Register the Bright Data MCP server (CLI) so Claude can call its scraping tools. Needs the API token above. |
| 5 | `claude plugin install brightdata-plugin@claude-plugins-official --scope local` | Add the Bright Data skill surface to this project. |

After `quicksetup` finishes, run `/setup-utarn-skills` once per repo to configure issue tracker, triage labels, and docs location — see the [Quickstart](./README.md#quickstart-30-second-setup) in the README.
