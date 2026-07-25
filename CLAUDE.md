# CLAUDE.md

คู่มือสำหรับ AI assistant ที่ทำงานใน repository นี้ (`linux-tutorial`) — คลังเอกสาร/ตัวอย่างการใช้งานเครื่องมือบน Linux/WSL/macOS

## ลักษณะของ repository

- เป็นคลัง **เอกสาร + ตัวอย่าง** (markdown-first) ไม่ใช่แอปพลิเคชันรันได้เพียงตัวเดียว
- แต่ละไฟล์ `.md` หมายเลขนำหน้า (เช่น `01_LINUX.md`, `04_VSCODE.md`) คือบทเรียนตามลำดับ
- โฟลเดอร์ `docker-compose/` เก็บตัวอย่าง compose สำหรับบริการต่าง ๆ (postgresql, redis, meilisearch, pgvector, timescaledb) — เป็นตัวอย่างอ้างอิง ไม่ใช่บริการหลักของ repo
- โฟลเดอร์ `monte_carlo/` เป็นตัวอย่างโค้ดประกอบบท `MONTE_CARLO.md`

## การเขียนเอกสาร

- ภาษา: เนื้อหาหลักเป็น **ภาษาอังกฤษ** ไฟล์ที่ลงท้ายด้วย `-th.md` (เช่น `QUICKSETUP-th.md`) คือเวอร์ชันภาษาไทย
- ข้อยกเว้น: `QUICKSETUP.md` เป็นภาษาไทยเท่านั้น (ไม่มีคู่ภาษาอังกฤษ เนื่องจาก `QUICKSETUP-th.md` ถูก rename มาแทนที่)
- เวลาเพิ่ม/แก้ไฟล์ ให้ดูว่ามีคู่ภาษาไทยหรือไม่ แล้วอัปเดตทั้งคู่ให้ sync กัน
- ใช้ GitHub-flavored markdown เน้นคำสั่งที่ copy-paste รันได้ทันที

## แนวทางการหาข้อมูลเวอร์ชัน

- สำหรับ library/framework/SDK/API/CLI ให้ใช้ `ctx7` CLI (`npx ctx7@latest library/docs`) ตามกฎใน `~/.claude/rules/context7.md`
- สำหรับค้นเว็บ/scrape ให้ใช้ Bright Data CLI (`bdata search` / `bdata scrape`) ตามกฎใน `~/.claude/rules/brightdata-search.md` — **ห้าม** ใช้ built-in `WebSearch`/`WebFetch`
- หากข้อมูลจาก context7 ไม่ชัดเจนหรือล้าหลัง ให้เสริมด้วย `bdata search` + `bdata scrape`

## การจัดการ Docker / port

- ตัวอย่าง compose ใน `docker-compose/` ใช้ image version ล่าสุดที่เสถียร (เช่น `postgres:18`)
- เมื่อสร้าง compose ใหม่ที่ต้อง map host port ให้ **สแกนหา port ว่าง** ก่อน เพื่อไม่ให้ชนกับ instance อื่น ๆ บนเครื่อง (เช่น `5432` มักถูกใช้) ดูวิธีใน `SAMPLE_PROMPT.md` และ `DOCKER.md`
- ใช้ named volume แยกตามบริการ และใส่ `healthcheck` เสมอ

## โครงสร้างหลัก

```
00_WSL_INSTALLATION.md .. 05_TMUX.md   # บทเรียนหลักตามลำดับ
CLAUDE.md / SAMPLE_PROMPT.md            # คู่มือ + ตัวอย่าง prompt
DOCKER.md / docker-compose/             # Docker & compose ตัวอย่าง
ORM.md / DATA_VALIDATION.md             # ORM & validation
GIT.md / TOKEN.md / SETTING.md           # Git, token, การตั้งค่า
QUICKSETUP.md                           # ติดตั้งสภาพแวดล้อมด่วน (ภาษาไทย)
SETUP_CLAUDE_CODE.md                    # ติดตั้ง Claude Code
CLOUDFLARE.md / CLOUDFLARE-th.md        # Cloudflare
OCR.md / MONTE_CARLO.md                 # OCR & Monte Carlo (พร้อมโค้ด)
PLAYWRIGHT.md                           # Playwright ติดตั้งบน Windows/Linux
TESTING.md                              # TDD และ Test Framework (Vitest + pytest)
DBWEAVER.md                             # DBeaver
```

## หมายเหตุสำหรับ SAMPLE_PROMPT.md

ไฟล์นี้คือ **prompt ตัวอย่าง** สำหรับสร้าง Todo App (Next.js 16 + Prisma 7 + PostgreSQL + Auth.js v5) — เป็นเทมเพลตให้ผู้ใช้คัดลอกไปใช้ ไม่ใช่โค้ดที่ต้องรันใน repo นี้ ห้ามสร้างไฟล์โค้ดของ Todo App ใน repo นี้โดยไม่ได้รับการขอ
