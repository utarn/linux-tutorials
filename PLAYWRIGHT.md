# Playwright — การติดตั้งบน Windows และ Linux

[Playwright](https://playwright.dev) เป็นเฟรมเวิร์กสำหรับ Web Testing และ Automation รองรับ Cross-browser Testing บน Chromium, Firefox และ WebKit

> **ข้อกำหนดเบื้องต้น (Prerequisites):**
> - ต้องติดตั้ง **Node.js** เวอร์ชัน 18 ขึ้นไป (แนะนำ LTS)
> - ตรวจสอบเวอร์ชันด้วย `node -v`

---

## สารบัญ

1. [ติดตั้งบน Windows](#ติดตั้งบน-windows)
2. [ติดตั้งบน Linux (Ubuntu/Debian)](#ติดตั้งบน-linux-ubuntudebian)
3. [คำสั่งที่ใช้งานบ่อย](#คำสั่งที่ใช้งานบ่อย)
4. [การติดตั้งด้วยวิธีอื่น](#การติดตั้งด้วยวิธีอื่น)

---

## ติดตั้งบน Windows

Windows สามารถติดตั้ง Playwright ผ่าน PowerShell หรือ Command Prompt ได้ไม่กี่ขั้นตอน

### 1. สร้างโปรเจกต์ Playwright

เปิด PowerShell หรือ Terminal แล้วรัน:

```powershell
npx playwright install --with-deps
```

หรือสร้างโปรเจกต์ใหม่พร้อมตั้งค่า:

```powershell
npm init playwright@latest
```

### 2. ตอบคำถามการตั้งค่า (Interactive Prompts)

ระบบจะถามค่าพื้นฐาน ให้เลือกตามต้องการ:

- **TypeScript หรือ JavaScript:** แนะนำ TypeScript (ค่าเริ่มต้น)
- **Where to put tests:** กด Enter เพื่อใช้โฟลเดอร์ `tests`
- **Add GitHub Actions workflow:** เลือก `true` หรือ `false`
- **Install Playwright browsers:** พิมพ์ `true` เพื่อให้ดาวน์โหลดเบราว์เซอร์ (Chromium, Firefox, WebKit)

### 3. ทดสอบรัน

```powershell
npx playwright test
```

หากต้องการดูรายงานผลการทดสอบ:

```powershell
npx playwright show-report
```

---

## ติดตั้งบน Linux (Ubuntu/Debian)

บน Linux มีขั้นตอนเพิ่มเติมคือการติดตั้ง System Dependencies เพื่อให้เบราว์เซอร์ Headless ทำงานได้

### 1. สร้างโปรเจกต์ Playwright

```bash
npm init playwright@latest
```

*(ตอบคำถามการตั้งค่าเหมือน Windows ข้างต้น)*

### 2. ติดตั้ง System Dependencies (สำคัญ)

Linux มักขาด Shared Libraries ที่เบราว์เซอร์ต้องการ ให้รันคำสั่งนี้:

```bash
npx playwright install-deps
```

หรือติดตั้งเบราว์เซอร์พร้อม System Dependencies ในคำสั่งเดียว:

```bash
npx playwright install --with-deps
```

### 3. ทดสอบรัน

```bash
npx playwright test
```

---

## คำสั่งที่ใช้งานบ่อย

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `npx playwright test` | รันเทสทั้งหมด |
| `npx playwright test --ui` | รันเทสแบบ UI mode |
| `npx playwright test --headed` | รันเทสแบบแสดงเบราว์เซอร์ |
| `npx playwright test --debug` | รันเทสแบบ Debug mode |
| `npx playwright show-report` | เปิดรายงาน HTML |
| `npx playwright codegen` | เปิดตัวบันทึกการกระทำเพื่อสร้างเทสอัตโนมัติ |
| `npx playwright install` | ติดตั้งเบราว์เซอร์ทั้งหมด |
| `npx playwright install chromium` | ติดตั้งเฉพาะ Chromium |
| `npx playwright install-deps` | ติดตั้ง System Dependencies (Linux) |
| `npx playwright uninstall` | ถอนการติดตั้งเบราว์เซอร์ |

### System Requirements อย่างเป็นทางการ

Playwright รองรับ:
- **Node.js:** 18.x, 22.x, 24.x หรือ 26.x
- **Windows:** 11+ หรือ Windows Server 2019+
- **macOS:** 14 (Sonoma) หรือใหม่กว่า
- **Linux:** Debian 12/13, Ubuntu 22.04/24.04/26.04 (x86-64 และ arm64)

---

## การติดตั้งด้วยวิธีอื่น

### ติดตั้งเฉพาะไลบรารี (ไม่สร้างโปรเจกต์)

```bash
npm install -D @playwright/test
npx playwright install
```

### ติดตั้งเฉพาะเบราว์เซอร์ที่ต้องการ

```bash
# Chromium อย่างเดียว
npx playwright install chromium

# Chromium + Webkit
npx playwright install chromium webkit

# Firefox อย่างเดียว
npx playwright install firefox
```

### ติดตั้งลง Docker

สำหรับ CI/CD หรือ Docker environment ให้เพิ่มใน `Dockerfile`:

```dockerfile
FROM node:22-slim

# ติดตั้ง System Dependencies
RUN npx playwright install-deps

# ติดตั้ง Playwright browsers
RUN npx playwright install chromium

WORKDIR /app
COPY . .
```

---

## แหล่งอ้างอิง

- [Playwright Documentation](https://playwright.dev/docs/intro)
- [GitHub: microsoft/playwright](https://github.com/microsoft/playwright)
