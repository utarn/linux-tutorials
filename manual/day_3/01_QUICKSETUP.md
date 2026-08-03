# การตั้งค่าด่วน (Quick Setup)

เริ่มใช้งาน Claude Code พร้อมเครื่องมือทั้งหมดที่คุณต้องการในขั้นตอนเดียว: ปลั๊กอิน engineer-skills, Context7 สำหรับดึงเอกสารสด, Bright Data CLI + skill สำหรับ scraping เว็บ และ Fallow CLI สำหรับวิเคราะห์ codebase

เลือก shell ของคุณแล้วรันบล็อก **install** ครั้งเดียว สิ่งนี้จะให้คู่คำสั่ง `ccc` / `cccc` สำหรับเปิด Claude Code พร้อมฟังก์ชัน `quicksetup` ที่เชื่อมต่อ skills ให้ จากนั้นเพียงพิมพ์ `quicksetup` เพื่อรันได้เลย

> `ccc` และ `cccc` คือ wrapper สะดวกสำหรับ `claude` — ข้ามการขออนุญาตต่อคำสั่งและต่อเซสชันล่าสุด สอดคล้องกับ flow `--dangerously-skip-permissions` ที่เหลือของ repo นี้สันนิษฐานไว้ พวกมันเรียก `claude` โดยตรง จึงทำงานได้กับทุกคน ไม่ใช่แค่ alias ส่วนตัวของผู้เขียน

## เงื่อนไขเบื้องต้นสำหรับ Windows (รันครั้งเดียว)

ก่อนติดตั้ง Claude Code บน Windows ให้ติดตั้ง Git for Windows, PowerShell 7, Windows Terminal, Node.js (ที่ Context7 และ Bright Data CLI ต้องใช้), GitHub CLI, GitLab CLI และ Python 3.14 ด้วย winget จากนั้นตั้งค่าให้ PowerShell 7 เป็นโปรไฟล์เริ่มต้นของ Windows Terminal:

```powershell
winget install --id Git.Git -e
winget install --id Microsoft.PowerShell -e
winget install --id Microsoft.WindowsTerminal -e
winget install --id OpenJS.NodeJS.LTS -e
winget install -e --id GitHub.cli
winget install --id glab.glab -e
winget install --id Python.Python.3.14 -e

# ตั้งค่า PowerShell 7 ให้เป็นโปรไฟล์เริ่มต้นใน Windows Terminal

```

## เงื่อนไขเบื้องต้นสำหรับ Linux (รันครั้งเดียว)

ก่อนติดตั้ง Claude Code บน Linux (Debian/Ubuntu) ให้ติดตั้ง build dependencies, GitHub CLI, GitLab CLI และ PowerShell 7 ดังนี้ Node.js 22 และ Python 3.14 จะถูกติดตั้งโดย `quicksetup` ผ่าน nvm + pyenv (ขั้นตอนที่ 0–0b):

```bash
sudo apt update && sudo apt install -y git curl build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev libffi-dev libncursesw5-dev \
  xz-utils tk-dev libxml2-dev libxmlsec1-dev liblzma-dev

# GitHub CLI
sudo apt install -y gh

# GitLab CLI — ดาวน์โหลด .deb จาก GitLab releases
GLAB_VER="1.52.0"
curl -sL "https://gitlab.com/gitlab-org/cli/-/releases/v${GLAB_VER}/downloads/glab_${GLAB_VER}_linux_amd64.deb" -o /tmp/glab.deb \
  && sudo dpkg -i /tmp/glab.deb

# PowerShell 7 — เพิ่ม Microsoft repository (ปรับ 24.04 เป็นเวอร์ชัน Ubuntu ของคุณ)
wget -q "https://packages.microsoft.com/config/ubuntu/24.04/packages-microsoft-prod.deb" -O /tmp/packages-microsoft-prod.deb \
  && sudo dpkg -i /tmp/packages-microsoft-prod.deb \
  && sudo apt update && sudo apt install -y powershell
```

## เงื่อนไขเบื้องต้นสำหรับ macOS (รันครั้งเดียว)

ก่อนติดตั้ง Claude Code บน macOS ให้ติดตั้ง Xcode Command Line Tools (รวม Git), Homebrew, GitHub CLI, GitLab CLI และ PowerShell 7 ดังนี้ Node.js 22 และ Python 3.14 จะถูกติดตั้งโดย `quicksetup` ผ่าน nvm + pyenv (ขั้นตอนที่ 0–0b) เช่นเดียวกับ Linux:

```bash
# Xcode Command Line Tools (รวม Git)
xcode-select --install

# Homebrew (ถ้ายังไม่มี)
which brew >/dev/null || /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# GitHub CLI
brew install gh

# GitLab CLI
brew install glab

# PowerShell 7
brew install --cask powershell
```

## ติดตั้ง Claude Code

ติดตั้ง CLI `claude` ก่อน (คู่มือที่เหลือเรียกใช้มัน) เลือกวิธีใดวิธีหนึ่ง:

**Native installer (แนะนำ)** — macOS / Linux / WSL:

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

ทางเลือก: `brew install --cask claude-code` (macOS), `winget install Anthropic.ClaudeCode` (Windows) หรือ `npm install -g @anthropic-ai/claude-code` (ต้องใช้ Node.js 22+) ดู [เอกสารติดตั้ง Claude Code](https://code.claude.com/docs/en/setup) สำหรับการติดตั้งผ่าน Linux package manager (apt/dnf/apk) และการกำหนดเวอร์ชัน

ตรวจสอบแล้วเข้าสู่ระบบ:

```bash
claude --version      # พิมพ์เช่น 2.1.211 (Claude Code)
claude                # เปิดเซสชันโต้ตอบแล้วพาเข้าสู่ระบบ
```

## Bash (Linux / macOS)

เพิ่มโค้ดนี้ลงใน `~/.bashrc` (หรือ `~/.zshrc` บน macOS) แล้วเริ่ม shell ใหม่:

```bash
# ตัวเปิด Claude Code แบบสะดวก
ccc()  { claude --dangerously-skip-permissions "$@"; }
cccc() { claude --dangerously-skip-permissions --continue "$@"; }

# ตั้งค่าแบบรอบเดียว: ปลั๊กอิน engineer-skills + Context7 + Bright Data CLI + skill
quicksetup() {
  # 0. nvm — Node Version Manager (ติดตั้ง Node.js 22 ล่าสุด)
  curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash
  [ -s "$HOME/.nvm/nvm.sh" ] && . "$HOME/.nvm/nvm.sh"
  nvm install 22
  nvm use 22

  # 0b. pyenv — Python Version Manager (ติดตั้ง Python 3.14 ล่าสุด)
  curl -fsSL https://pyenv.run | bash
  export PYENV_ROOT="$HOME/.pyenv"
  [ -s "$PYENV_ROOT/bin/pyenv" ] && eval "$(pyenv init -)"
  pyenv install 3.14
  pyenv global 3.14

  # 1. ปลั๊กอิน engineer-skills
  claude plugin marketplace add utarn/engineer-skills
  claude plugin install utarn-skills@utarn

  # 2. Context7 — เอกสาร library แบบสด
  npx ctx7@latest setup

  # 3. Bright Data — ติดตั้ง CLI แบบ global
  npm install -g @brightdata/cli

  # 4. Bright Data — ลงทะเบียน skills repo เป็น plugin marketplace
  claude plugin marketplace add brightdata/skills

  # 5. Bright Data — ติดตั้ง skills plugin จาก marketplace นั้น
  claude plugin install brightdata-plugin@brightdata-plugins --scope local

  # 6. Bright Data — login ครั้งเดียวเพื่อยืนยันตัวตนของ CLI
  bdata login

  # 7. Fallow — ติดตั้ง CLI วิเคราะห์ codebase แบบ global
  npm install -g fallow
}
```

> **Node.js / Python:** ขั้นตอนที่ 0–0b จะติดตั้ง nvm + Node.js 22 และ pyenv + Python 3.14 ให้อัตโนมัติทั้งบน Linux และ macOS (nvm และ pyenv ทำงานได้ทั้งสองระบบ) บน Windows ได้ติดตั้งผ่าน winget ในเงื่อนไขเบื้องต้นด้านบนแล้ว

รันคำสั่ง:

```bash
quicksetup
```

## PowerShell (Windows)

### สร้าง / เปิดโปรไฟล์ PowerShell ของคุณ

หากไฟล์โปรไฟล์ยังไม่มีอยู่ ให้สร้างขึ้นแล้วเปิดด้วย Notepad:

```powershell
if (!(Test-Path -Path $PROFILE)) { New-Item -ItemType File -Path $PROFILE -Force }; notepad $PROFILE
```

เพิ่มโค้ดนี้ลงในโปรไฟล์ PowerShell ของคุณ แล้วเปิดเทอร์มินัลใหม่:

```powershell
# ตัวเปิด Claude Code แบบสะดวก
function ccc  { claude --dangerously-skip-permissions @args }
function cccc { claude --dangerously-skip-permissions --continue @args }

# ตั้งค่าแบบรอบเดียว: ปลั๊กอิน engineer-skills + Context7 + Bright Data CLI + skill
function quicksetup {
  # 1. ปลั๊กอิน engineer-skills
  claude plugin marketplace add utarn/engineer-skills
  claude plugin install utarn-skills@utarn

  # 2. Context7 — เอกสาร library แบบสด
  npx ctx7@latest setup

  # 3. Bright Data — ติดตั้ง CLI แบบ global (ต้องใช้ Node.js ดูด้านล่าง)
  npm install -g @brightdata/cli

  # 4. Bright Data — ลงทะเบียน skills repo เป็น plugin marketplace
  claude plugin marketplace add brightdata/skills

  # 5. Bright Data — ติดตั้ง skills plugin จาก marketplace นั้น
  claude plugin install brightdata-plugin@brightdata-plugins --scope local

  # 6. Bright Data — login ครั้งเดียวเพื่อยืนยันตัวตนของ CLI
  bdata login

  # 7. Fallow — ติดตั้ง CLI วิเคราะห์ codebase แบบ global
  npm install -g fallow
}
```

รันคำสั่ง:

```powershell
quicksetup
```

## การตั้งค่า Bright Data

Bright Data CLI (`brightdata` / `bdata`) ถูกติดตั้งแบบ global ในขั้นตอนที่ 3 ของ `quicksetup` และยืนยันตัวตนในขั้นตอนที่ 6 ผ่าน `bdata login` ซึ่งจะเปิดเบราว์เซอร์สำหรับ OAuth และสร้าง proxy zones ที่จำเป็นโดยอัตโนมัติ คุณ **ไม่ต้อง** ใช้ MCP server หรือ export API token ด้วยมือ — CLI เก็บข้อมูลรับรองไว้ในเครื่องหลังจาก login

- **Headless / SSH** (ไม่มีเบราว์เซอร์): รัน `bdata login --device` แทน แล้วทำตามขั้นตอน device-code flow
- **Non-interactive** (เช่นในสคริปต์): รัน `bdata login --api-key <key>` ด้วย API key จากแดชบอร์ด Bright Data ของคุณ
- ตรวจสอบว่าใช้งานได้ด้วย `bdata config` หรือ `bdata budget`

`brightdata-plugin` (ขั้นตอนที่ 4–5 ดึดจาก GitHub repo [brightdata/skills](https://github.com/brightdata/skills) โดยตรง) ติดตั้ง Bright Data skills 21 ตัวเข้าไปใน Claude Code — รวมถึง `brightdata-cli`, `search`, `scrape`, `data-feeds`, `competitive-intel`, `discover-api`, `live-research` และอื่น ๆ — เพื่อให้ agent รู้วิธีขับ `bdata` CLI สำหรับ scraping, ค้น SERP และ structured-data pipelines กว่า 40 แบบ มี global rule ที่ตรงกัน (`~/.claude/rules/brightdata-search.md`) ที่บอก Claude ให้เลือกใช้ `bdata` แทนเครื่องมือ `WebSearch`/`WebFetch` ที่มากับระบบ

## Fallow — codebase intelligence

[Fallow](https://docs.fallow.tools) คือตัววิเคราะห์ codebase สำหรับ TypeScript/JavaScript ช่วยหาโค้ดที่ไม่ได้ใช้, การอ้างอิงแบบวงกลม, โค้ดที่ซ้ำกัน, complexity hotspot และการละเมิดขอบเขตสถาปัตยกรรม ติดตั้งแบบ global ในขั้นตอนที่ 7 ของ `quicksetup` (ไบนารี `fallow`) ต้องใช้ Node.js >= 20 และไม่ต้องตั้งค่าในครั้งแรก

```bash
# สแกนครั้งเดียว — ไม่ต้องตั้งค่า
fallow                       # สรุปภาพรวม
fallow health                # complexity, maintainability, hotspots, coverage gaps
fallow dead-code             # ไฟล์, exports และ dependencies ที่ไม่ได้ใช้
fallow dupes                 # โค้ดที่ซ้ำกันแบบ copy-paste และโครงสร้าง
fallow audit                 # ตรวจไฟล์ที่เปลี่ยนแปลง (เหมาะใน PR)

# สร้าง config ของโปรเจกต์ (ไม่บังคับ — เพิ่มไฟล์ fallow config และ Git hook ได้)
fallow init

# ดูตัวอย่าง auto-fix ที่ปลอดภัยก่อนนำไปใช้
fallow fix --dry-run
```

ดู [เอกสาร Fallow](https://docs.fallow.tools) สำหรับการเชื่อม CI, rule packs และ runtime coverage

## แต่ละขั้นตอนทำอะไร

| ขั้นตอน | คำสั่ง | ผลลัพธ์ |
|---|---|---|
| 0 | `curl ... nvm install 22` | ติดตั้ง nvm + Node.js 22 (Linux / macOS) |
| 0b | `curl ... pyenv install 3.14` | ติดตั้ง pyenv + Python 3.14 (Linux / macOS) |
| 1 | `claude plugin marketplace add utarn/engineer-skills` | ลงทะเบียน repo นี้เป็น Claude Code plugin marketplace |
| 2 | `claude plugin install utarn-skills@utarn` | ติดตั้งแพ็กเกจ engineer-skills ทั้งหมดเป็นปลั๊กอินที่จัดการและอัปเดตอัตโนมัติ |
| 3 | `npx ctx7@latest setup` | ติดตั้ง Context7 ลงใน coding agent ของคุณเพื่อให้ดึงเอกสาร library แบบสดได้ |
| 4 | `npm install -g @brightdata/cli` | ติดตั้ง Bright Data CLI (`brightdata` / `bdata`) แบบ global ต้องใช้ Node.js >= 20 |
| 5 | `claude plugin marketplace add brightdata/skills` | ลงทะเบียน GitHub repo [brightdata/skills](https://github.com/brightdata/skills) เป็น Claude Code plugin marketplace |
| 6 | `claude plugin install brightdata-plugin@brightdata-plugins --scope local` | ติดตั้งปลั๊กอิน Bright Data 21 skills จาก marketplace นั้นเข้าโปรเจกต์นี้ |
| 7 | `bdata login` | ยืนยันตัวตน CLI ครั้งเดียว — เปิดเบราว์เซอร์สำหรับ OAuth และสร้าง proxy zones อัตโนมัติ |
| 8 | `npm install -g fallow` | ติดตั้ง CLI วิเคราะห์ codebase ของ Fallow (`fallow`) แบบ global ต้องใช้ Node.js >= 20 |

หลังจาก `quicksetup` เสร็จ ให้รัน `/setup-utarn-skills` ครั้งเดียวต่อ repo เพื่อตั้งค่า issue tracker, triage labels และตำแหน่ง docs — ดู [Quickstart](./README.md#quickstart-30-second-setup) ใน README
