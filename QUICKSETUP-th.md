# การตั้งค่าด่วน (Quick Setup)

เริ่มใช้งาน Claude Code พร้อมเครื่องมือทั้งหมดที่คุณต้องการในขั้นตอนเดียว: ปลั๊กอิน engineer-skills, Context7 สำหรับดึงเอกสารสด, และ Bright Data CLI + skill สำหรับ scraping เว็บ

เลือก shell ของคุณแล้วรันบล็อก **install** ครั้งเดียว สิ่งนี้จะให้คู่คำสั่ง `ccc` / `cccc` สำหรับเปิด Claude Code พร้อมฟังก์ชัน `quicksetup` ที่เชื่อมต่อ skills ให้ จากนั้นเพียงพิมพ์ `quicksetup` เพื่อรันได้เลย

> `ccc` และ `cccc` คือ wrapper สะดวกสำหรับ `claude` — ข้ามการขออนุญาตต่อคำสั่งและต่อเซสชันล่าสุด สอดคล้องกับ flow `--dangerously-skip-permissions` ที่เหลือของ repo นี้สันนิษฐานไว้ พวกมันเรียก `claude` โดยตรง จึงทำงานได้กับทุกคน ไม่ใช่แค่ alias ส่วนตัวของผู้เขียน

## เงื่อนไขเบื้องต้นสำหรับ Windows (รันครั้งเดียว)

ก่อนติดตั้ง Claude Code บน Windows ให้ติดตั้ง Git for Windows, PowerShell 7, Windows Terminal และ Node.js (ที่ Context7 และ Bright Data CLI ต้องใช้) ด้วย winget จากนั้นตั้งค่าให้ PowerShell 7 เป็นโปรไฟล์เริ่มต้นของ Windows Terminal:

```powershell
winget install --id Git.Git -e
winget install --id Microsoft.PowerShell -e
winget install --id Microsoft.WindowsTerminal -e
winget install --id OpenJS.NodeJS.LTS -e

# ตั้งค่า PowerShell 7 ให้เป็นโปรไฟล์เริ่มต้นใน Windows Terminal
$settingsPath = "$env:LOCALAPPDATA\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"
$ps7 = (Get-Command pwsh).Source
$settings = Get-Content $settingsPath -Raw | ConvertFrom-Json
($settings.profiles.list | Where-Object { $_.commandline -eq $ps7 }).guid | ForEach-Object { $settings.defaultProfile = $_ }
$settings | ConvertTo-Json -Depth 10 | Set-Content $settingsPath
```

## ติดตั้ง Claude Code

ติดตั้ง CLI `claude` ก่อน (คู่มือที่เหลือเรียกใช้มัน) เลือกวิธีใดวิธีหนึ่ง

**เงื่อนไขเบื้องต้นสำหรับ Linux** — บน Debian/Ubuntu ให้ติดตั้ง Git (และ curl) ก่อนตัวติดตั้งแบบ native:

```bash
sudo apt update && sudo apt install -y git curl
```

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
  # 1. ปลั๊กอิน engineer-skills
  claude plugin marketplace add utarn/engineer-skills
  claude plugin install utarn-skills@utarn

  # 2. Context7 — เอกสาร library แบบสด
  npx ctx7@latest setup

  # 3. Bright Data — ติดตั้ง CLI แบบ global (ต้องใช้ Node.js ดูด้านล่าง)
  npm install -g @brightdata/cli

  # 4. Bright Data — skill surface ภายใน Claude Code
  claude plugin install brightdata-plugin@claude-plugins-official --scope local

  # 5. Bright Data — login ครั้งเดียวเพื่อยืนยันตัวตนของ CLI
  bdata login
}
```

> **ต้องใช้ Node.js:** ขั้นตอนที่ 3 ต้องใช้ Node.js (>= 20) บน macOS ติดตั้งด้วย `brew install node@20` (หรือใช้ตัวติดตั้งทางการ) บน Linux ใช้ package manager หรือ [NodeSource](https://github.com/nodesource/distributions) บน Windows ได้ติดตั้งผ่าน winget ในเงื่อนไขเบื้องต้นด้านบนแล้ว

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

  # 4. Bright Data — skill surface ภายใน Claude Code
  claude plugin install brightdata-plugin@claude-plugins-official --scope local

  # 5. Bright Data — login ครั้งเดียวเพื่อยืนยันตัวตนของ CLI
  bdata login
}
```

รันคำสั่ง:

```powershell
quicksetup
```

## การตั้งค่า Bright Data

Bright Data CLI (`brightdata` / `bdata`) ถูกติดตั้งแบบ global ในขั้นตอนที่ 3 ของ `quicksetup` และยืนยันตัวตนในขั้นตอนที่ 5 ผ่าน `bdata login` ซึ่งจะเปิดเบราว์เซอร์สำหรับ OAuth และสร้าง proxy zones ที่จำเป็นโดยอัตโนมัติ คุณ **ไม่ต้อง** ใช้ MCP server หรือ export API token ด้วยมือ — CLI เก็บข้อมูลรับรองไว้ในเครื่องหลังจาก login

- **Headless / SSH** (ไม่มีเบราว์เซอร์): รัน `bdata login --device` แทน แล้วทำตามขั้นตอน device-code flow
- **Non-interactive** (เช่นในสคริปต์): รัน `bdata login --api-key <key>` ด้วย API key จากแดชบอร์ด Bright Data ของคุณ
- ตรวจสอบว่าใช้งานได้ด้วย `bdata config` หรือ `bdata budget`

`brightdata-plugin` (ขั้นตอนที่ 4) ติดตั้ง skill `brightdata-cli` เข้าไปใน Claude Code เพื่อให้ agent รู้วิธีขับ `bdata` CLI สำหรับ scraping, ค้น SERP และ structured-data pipelines กว่า 40 แบบ มี global rule ที่ตรงกัน (`~/.claude/rules/brightdata-search.md`) ที่บอก Claude ให้เลือกใช้ `bdata` แทนเครื่องมือ `WebSearch`/`WebFetch` ที่มากับระบบ

## แต่ละขั้นตอนทำอะไร

| ขั้นตอน | คำสั่ง | ผลลัพธ์ |
|---|---|---|
| 1 | `claude plugin marketplace add utarn/engineer-skills` | ลงทะเบียน repo นี้เป็น Claude Code plugin marketplace |
| 2 | `claude plugin install utarn-skills@utarn` | ติดตั้งแพ็กเกจ engineer-skills ทั้งหมดเป็นปลั๊กอินที่จัดการและอัปเดตอัตโนมัติ |
| 3 | `npx ctx7@latest setup` | ติดตั้ง Context7 ลงใน coding agent ของคุณเพื่อให้ดึงเอกสาร library แบบสดได้ |
| 4 | `npm install -g @brightdata/cli` | ติดตั้ง Bright Data CLI (`brightdata` / `bdata`) แบบ global ต้องใช้ Node.js >= 20 |
| 5 | `claude plugin install brightdata-plugin@claude-plugins-official --scope local` | เพิ่ม Bright Data skill surface ให้โปรเจกต์นี้ |
| 6 | `bdata login` | ยืนยันตัวตน CLI ครั้งเดียว — เปิดเบราว์เซอร์สำหรับ OAuth และสร้าง proxy zones อัตโนมัติ |

หลังจาก `quicksetup` เสร็จ ให้รัน `/setup-utarn-skills` ครั้งเดียวต่อ repo เพื่อตั้งค่า issue tracker, triage labels และตำแหน่ง docs — ดู [Quickstart](./README.md#quickstart-30-second-setup) ใน README
