# Quick Setup

Get Claude Code working with all the tools you need in one shot: the engineer-skills plugin, Context7 for live docs, and the Bright Data CLI + skill for web scraping.

Pick your shell and run the **install** block once. That gives you a `ccc` / `cccc` pair to launch Claude Code, plus a `quicksetup` function that wires up the skills. Then just type `quicksetup` to run it.

> `ccc` and `cccc` are convenience wrappers around `claude` — they skip the per-command permission prompt and continue the last session, matching the `--dangerously-skip-permissions` flow the rest of this repo assumes. They call `claude` directly, so they work for anyone, not just the author's private aliases.

## Windows prerequisites (run once)

Before installing Claude Code on Windows, install Git for Windows, PowerShell 7, Windows Terminal, Node.js (needed by Context7 and the Bright Data CLI), the GitHub CLI, and Python 3.14 with winget, then make PowerShell 7 the default profile for Windows Terminal:

```powershell
winget install --id Git.Git -e
winget install --id Microsoft.PowerShell -e
winget install --id Microsoft.WindowsTerminal -e
winget install --id OpenJS.NodeJS.LTS -e
winget install -e --id GitHub.cli
winget install --id Python.Python.3.14 -e

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

# One-shot setup: engineer-skills plugin + Context7 + Bright Data CLI + skill
quicksetup() {
  # 1. engineer-skills plugin
  claude plugin marketplace add utarn/engineer-skills
  claude plugin install utarn-skills@utarn

  # 2. Context7 — live library docs
  npx ctx7@latest setup

  # 3. Bright Data — install the CLI globally (needs Node.js, see below)
  npm install -g @brightdata/cli

  # 4. Bright Data — register the skills repo as a plugin marketplace
  claude plugin marketplace add brightdata/skills

  # 5. Bright Data — install the skills plugin from that marketplace
  claude plugin install brightdata-plugin@brightdata-plugins --scope local

  # 6. Bright Data — one-time login so the CLI is authenticated
  bdata login
}
```

> **Node.js required:** Step 3 needs Node.js (>= 20). On macOS install it with `brew install node@20` (or via the official installer); on Linux use your package manager or [NodeSource](https://github.com/nodesource/distributions). On Windows it was already installed via winget in the prerequisites above.

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

# One-shot setup: engineer-skills plugin + Context7 + Bright Data CLI + skill
function quicksetup {
  # 1. engineer-skills plugin
  claude plugin marketplace add utarn/engineer-skills
  claude plugin install utarn-skills@utarn

  # 2. Context7 — live library docs
  npx ctx7@latest setup

  # 3. Bright Data — install the CLI globally (needs Node.js, see below)
  npm install -g @brightdata/cli

  # 4. Bright Data — register the skills repo as a plugin marketplace
  claude plugin marketplace add brightdata/skills

  # 5. Bright Data — install the skills plugin from that marketplace
  claude plugin install brightdata-plugin@brightdata-plugins --scope local

  # 6. Bright Data — one-time login so the CLI is authenticated
  bdata login
}
```

Run it:

```powershell
quicksetup
```

## Bright Data setup

The Bright Data CLI (`brightdata` / `bdata`) is installed globally in step 3 of `quicksetup` and authenticated in step 6 via `bdata login`, which opens a browser for OAuth and auto-creates the required proxy zones. You do **not** need an MCP server or a manually-exported API token — the CLI stores its credentials locally after login.

- **Headless / SSH** (no browser available): run `bdata login --device` instead and follow the device-code flow.
- **Non-interactive** (e.g. in a script): run `bdata login --api-key <key>` with an API key from your Bright Data dashboard.
- Verify it works with `bdata config` or `bdata budget`.

The `brightdata-plugin` (steps 4–5, sourced directly from the [brightdata/skills](https://github.com/brightdata/skills) GitHub repo) installs 21 Bright Data skills into Claude Code — including `brightdata-cli`, `search`, `scrape`, `data-feeds`, `competitive-intel`, `discover-api`, `live-research`, and more — so the agent knows how to drive the `bdata` CLI for scraping, SERP search, and 40+ structured-data pipelines. A matching global rule (`~/.claude/rules/brightdata-search.md`) tells Claude to prefer `bdata` over the built-in `WebSearch`/`WebFetch` tools.

## What each step does

| Step | Command | Effect |
|---|---|---|
| 1 | `claude plugin marketplace add utarn/engineer-skills` | Register this repo as a Claude Code plugin marketplace. |
| 2 | `claude plugin install utarn-skills@utarn` | Install the whole engineer-skills bundle as a managed, auto-updating plugin. |
| 3 | `npx ctx7@latest setup` | Install Context7 into your coding agent so it can fetch live library docs. |
| 4 | `npm install -g @brightdata/cli` | Install the Bright Data CLI (`brightdata` / `bdata`) globally. Needs Node.js >= 20. |
| 5 | `claude plugin marketplace add brightdata/skills` | Register the [brightdata/skills](https://github.com/brightdata/skills) GitHub repo as a Claude Code plugin marketplace. |
| 6 | `claude plugin install brightdata-plugin@brightdata-plugins --scope local` | Install the 21-skill Bright Data plugin from that marketplace into this project. |
| 7 | `bdata login` | Authenticate the CLI once — opens the browser for OAuth and auto-creates proxy zones. |

After `quicksetup` finishes, run `/setup-utarn-skills` once per repo to configure issue tracker, triage labels, and docs location — see the [Quickstart](./README.md#quickstart-30-second-setup) in the README.
