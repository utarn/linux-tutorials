# คู่มือ VS Code + Remote - SSH

เอกสารสอนการดาวน์โหลดและติดตั้ง Visual Studio Code ติดตั้ง extension **Remote - SSH** ของ Microsoft และใช้เข้าไปแก้ไขไฟล์บน Linux server ผ่าน SSH เหมือนนั่งแก้ที่เครื่องนั้น

---

## สารบัญ

1. [ทำไมต้อง Remote - SSH](#1-ทำไมต้อง-remote---ssh)
2. [ดาวน์โหลดและติดตั้ง VS Code](#2-ดาวน์โหลดและติดตั้ง-vs-code)
3. [ติดตั้ง extension Remote - SSH](#3-ติดตั้ง-extension-remote---ssh)
4. [เตรียมการเชื่อมต่อ](#4-เตรียมการเชื่อมต่อ)
5. [เชื่อมต่อ Linux Server](#5-เชื่อมต่อ-linux-server)
6. [เปิดโฟลเดอร์และแก้ไขไฟล์](#6-เปิดโฟลเดอร์และแก้ไขไฟล์)
7. [ใช้ร่วมกับ ~/.ssh/config](#7-ใช้ร่วมกับ-sshconfig)
8. [เคล็ดลับและการใช้งาน](#8-เคล็ดลับและการใช้งาน)
9. [แก้ปัญหาที่พบบ่อย](#9-แก้ปัญหาที่พบบ่อย)

---

## 1. ทำไมต้อง Remote - SSH

ปกติการแก้ไฟล์บน server ทำผ่าน `ssh` + `nano`/`vim` ใน terminal แต่ถ้าอยากได้ประสบการณ์เหมือนแก้ไฟล์ local (IntelliSense, ไฮไลต์, หาทั่วโปรเจกต์, terminal, ดีบัก) ให้ใช้ **Remote - SSH**

Extension นี้จะ:
1. ติดตั้งส่วนประกอบ VS Code Server ลงบน Linux server อัตโนมัติ
2. เปิดไฟล์/โฟลเดอร์บน server ในหน้าต่าง VS Code
3. ทุกการแก้ไข/รันเทอร์มินัลเกิดขึ้นที่ **เครื่อง server** ไม่ใช่เครื่องเรา

```
[ เครื่องเรา ]                       [ Linux Server ]
  VS Code (UI)  ──── SSH (พอร์ต 22) ────►  VS Code Server
  แสดงผลจอ/รับคีย์บอร์ด                   อ่าน/เขียนไฟล์, รันคำสั่ง
```

> ข้อดี: ไม่ต้องโคลนโค้ดมา local, รัน/ดีบักบนสภาพแวดล้อมจริง, ใช้ extension ได้เหมือนปกติ
> ข้อเสีย: ต้องเชื่อมต่อเน็ตเวิร์กตลอด, ใช้แบนด์วิดท์บ้าง

---

## 2. ดาวน์โหลดและติดตั้ง VS Code

### 2.1 Windows

1. เข้าเว็บ https://code.visualstudio.com/Download
2. คลิกดาวน์โหลด **Windows** (เลือก **User Installer x64** สำหรับคนส่วนใหญ่)
   - **System Installer** สำหรับติดตั้งให้ผู้ใช้ทุกคนในเครื่อง (ต้องสิทธิผู้ดูแล)
   - **ARM64** สำหรับเครื่อง Windows on ARM
3. รันไฟล์ `.exe` ที่ดาวน์โหลด
4. คลิก Next จนถึงหน้าเลือกงานเพิ่มเติม — **แนะนำให้ติ๊ก**:
   - ✅ Add "Open with Code" action to Windows Explorer file context menu
   - ✅ Add "Open with Code" action to Windows Explorer directory context menu
   - ✅ Register Code as an editor for supported file types
   - ✅ Add to PATH (สำคาญ — ให้เรียก `code` ใน terminal ได้)
5. Next → Install → Finish

> **ทางเลือกผ่าน winget:** ใน PowerShell รัน `winget install --id Microsoft.VisualStudioCode -e`

### 2.2 macOS

1. เข้า https://code.visualstudio.com/Download
2. ดาวน์โหลดไฟล์ `.zip` สำหรับ macOS (เลือก **Apple Silicon** สำหรับ M1/M2/M3 หรือ **Intel** สำหรับเครื่อง Intel)
3. แตก zip แล้วลาก **Visual Studio Code** ไปในโฟลเดอร์ **Applications**
4. ครั้งแรกที่เปิด: คลิกขวา → Open → กด Open อีกครั้ง (เพราะไม่ได้ติดตั้งผ่าน App Store)
5. เพิ่มคำสั่ง `code` ใน terminal: เปิด VS Code → Cmd+Shift+P → พิมพ์ **shell command** → เลือก **Shell Command: Install 'code' command in PATH**

> **ทางเลือกผ่าน Homebrew:** `brew install --cask visual-studio-code`

### 2.3 Linux

**ติดตั้งผ่าน package manager (แนะนำ — อัปเดตง่าย):**

```bash
# Debian/Ubuntu — ติดตั้ง repo ของ Microsoft
sudo apt install -y wget gpg
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
rm -f packages.microsoft.gpg
sudo apt update
sudo apt install -y code

# Fedora/RHEL
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'
sudo dnf install -y code

# Arch/Manjaro (ใช้ AUR)
yay -S visual-studio-code-bin
```

**หรือติดตั้งผ่าน snap/flatpak:**
```bash
sudo snap install code --classic        # snap
flatpak install flathub com.visualstudio.code   # flatpak
```

**หรือดาวน์โหลดไฟล์ติดตั้งโดยตรง:**
- เข้า https://code.visualstudio.com/Download → เลือก `.deb` (Debian/Ubuntu) หรือ `.rpm` (Fedora/RHEL)
- ติดตั้ง: `sudo apt install ./code_*.deb` หรือ `sudo dnf install code-*.rpm`

---

## 3. ติดตั้ง extension Remote - SSH

### 3.1 ผู้จัดพิมพ์: Microsoft (เป็น extension ทางการ)

### 3.2 ขั้นตอนติดตั้ง

1. เปิด VS Code
2. เปิด Extensions ด้วยวิธีใดวิธีหนึ่ง:
   - คลิกไอคอน **Extensions** ที่แถบซ้าย (รูปสี่เหลี่ยมจัตุรัส)
   - หรือกด **Ctrl+Shift+X** (Windows/Linux) / **Cmd+Shift+X** (macOS)
   - หรือเมนู **View → Extensions**
3. ในช่องค้นหาพิมพ์: **Remote - SSH**
4. มองหา extension ที่:
   - ชื่อ: **Remote - SSH**
   - ผู้จัดพิมพ์: **Microsoft**
   - คำอธิบาย: "Remote Development - SSH"

   > ⚠️ **ระวัง extension ชื่อคล้ายจากผู้จัดพิมพ์อื่น** — ใช้ของ **Microsoft** เท่านั้น (มักมีเครื่องหมาย ✓ สีฟ้า "Verified Publisher")
5. กด **Install**
6. รอจนปุ่มเปลี่ยนเป็น "Installed" / สีน้ำเงิน

### 3.3 ตรวจว่าติดตั้งสำเร็จ

- กด **F1** หรือ **Ctrl+Shift+P** (Cmd+Shift+P บน macOS) เพื่อเปิด Command Palette
- พิมพ์ **Remote-SSH** — ถ้าเห็นรายการคำสั่ง `Remote-SSH: Connect to Host...`, `Remote-SSH: Add New SSH Host...` ฯลฯ คือติดตั้งสำเร็จ

> **แพ็กแนะนำ:** ติดตั้ง **Remote - SSH: Editing Configuration Files** (Microsoft) เพิ่มด้วย ช่วยเติม/ตรวจ `~/.ssh/config` ได้สะดวกขึ้น

---

## 4. เตรียมการเชื่อมต่อ

ก่อนเชื่อมต่อต้องมีสิ่งต่อไปนี้:

1. **SSH บนเครื่อง local ใช้ได้**
   - Windows 10/11: มี OpenSSH ในตัว (หากไม่มี → Settings → Apps → Optional features → เพิ่ม OpenSSH Client)
   - macOS/Linux: มี `ssh` มาให้
2. **ล็อกอินเซิร์ฟเวอร์ด้วย SSH ได้** (รหัสผ่านหรือ public key)
   - ถ้ายังไม่ได้ตั้ง SSH key ดู [PUBLICKEY.md](PUBLICKEY.md)
3. **ข้อมูลการเชื่อมต่อ**
   - IP/domain ของ server
   - ชื่อผู้ใช้
   - พอร์ต (ค่าเริ่มต้น 22)
   - ตำแหน่งไฟล์ private key (ถ้าใช้ key auth)
4. **โฟลเดอร์ที่จะเปิด** บน server เช่น `/home/user/project`

ตรวจก่อนว่าล็อกอินได้:
```bash
ssh user@192.168.1.10            # ต้องเข้าได้ก่อน ถึงจะเชื่อม VS Code ได้
```

---

## 5. เชื่อมต่อ Linux Server

### วิธีที่ 5.1 — ใช้ Command Palette (เริ่มต้น)

1. กด **F1** / **Ctrl+Shift+P** (Cmd+Shift+P บน macOS)
2. พิมพ์และเลือก: **Remote-SSH: Connect to Host...**
3. คลิก **+ Add New SSH Host...**
4. ใส่คำสั่ง SSH แบบเดียวกับที่ใช้ใน terminal:
   ```
   ssh user@192.168.1.10
   ```
   กรณีใช้ key หรือพอร์ตเฉพาะ:
   ```
   ssh -i ~/.ssh/id_ed25519 -p 2222 user@192.168.1.10
   ```
5. เลือกไฟล์คอนฟิกที่จะบันทึก (VS Code แนะนำให้ใช้ `~/.ssh/config`)
6. ครั้งต่อไปเลือก `Remote-SSH: Connect to Host...` จะเห็น host นี้อยู่ในรายการแล้ว

### วิธีที่ 5.2 — ใช้ปุ่มสีเขียว (Remote Window)

มุมล่างซ้ายของ VS Code มี **ไอคอนสีเขียว/ฟ้า** (Remote indicator):

1. คลิกไอคอนสีเขียว → เลือก **Connect to Host...**
2. เลือก host ที่ตั้งไว้ หรือ **+ Add New SSH Host...** ถ้ายังไม่มี
3. เลือก OS ของ server (Linux) หากระบบถาม
4. รอ VS Code ติดตั้ง **VS Code Server** ลงบน server (ครั้งแรกใช้เวลา ~30 วินาที – 2 นาที)

### ระหว่างการเชื่อมต่อ

- กด **F1** → **Remote-SSH: Show Log** ดูความคืบหน้าได้
- ถ้าใช้ key ที่มี passphrase จะมีหน้าต่างถาม passphrase ที่ด้านบน
- ถ้าใช้รหัสผ่านจะมีหน้าต่างถามรหัสผ่านด้านบน
- เมื่อเชื่อมต่อสำเร็จ ไอคอนมุมล่างซ้ายจะเปลี่ยนเป็น **สีเขียว** พร้อมข้อความ **SSH: <ชื่อ host>**

---

## 6. เปิดโฟลเดอร์และแก้ไขไฟล์

หลังเชื่อมต่อสำเร็จ:

1. เมนู **File → Open Folder...** (Ctrl+K แล้ว Ctrl+O / Cmd+O)
2. VS Code จะแสดงหน้าต่างเลือกโฟลเดอร์ **บนเซิร์ฟเวอร์** (ไม่ใช่ local)
3. พิมพ์เส้นทางหรือเลือกจาก list เช่น `/home/user/project` → กด OK
4. ครั้งแรกอาจมีหน้าต่างถาม "Do you trust the authors..." → กด **Yes, I trust the authors**

ตอนนี้ทุกอย่างทำงานบน server:

| สิ่งที่ทำ | เกิดที่ไหน |
|---|---|
| แก้ไข/บันทึกไฟล์ | บน server |
| Terminal (Ctrl+\`) | บน server (เป็น shell ของ server) |
| รัน/ดีบักโปรแกรม | บน server |
| Search ทั่วโปรเจกต์ | บน server |
| Extensions | บางตัวติดตั้งที่ local (UI), บางตัวติดตั้งที่ server (ดูหัวข้อ 8.3) |

### เปิด terminal ของ server

- เมนู **Terminal → New Terminal** หรือ **Ctrl+\`** (backtick)
- Terminal นี้คือ shell ของ server ใช้รันคำสั่งได้เหมือน `ssh` เข้าไปตรง ๆ
- ใช้ควบคู่กับการแก้ไฟล์ได้สะดวก เช่น `npm install`, `python app.py`, `systemctl restart nginx`

### ปิดการเชื่อมต่อ

- **File → Close Remote Connection** ปิดเซสชันกลับสู่หน้าต่าง local
- หรือคลิกไอคอนสีเขียวมุมล่างซ้าย → **Close Remote Connection**
- ปิดหน้าต่าง VS Code ทิ้งก็ได้ การเชื่อมต่อจะถูกตัด

---

## 7. ใช้ร่วมกับ ~/.ssh/config

ถ้ามีไฟล์ `~/.ssh/config` ตั้ง host ไว้แล้ว (ดู [PUBLICKEY.md](PUBLICKEY.md) หัวข้อ 6) VS Code จะอ่านรายชื่อ host มาแสดงให้เลือกโดยอัตโนมัติ

ตัวอย่าง `~/.ssh/config`:
```ssh-config
Host prod
    HostName 192.168.1.10
    User user
    IdentityFile ~/.ssh/id_ed25519
    Port 22

Host staging
    HostName staging.example.com
    User deploy
    Port 2222
    IdentityFile ~/.ssh/key_staging
```

ใน VS Code:
1. **Remote-SSH: Connect to Host...**
2. จะเห็น `prod` และ `staging` ในรายการ → คลิกเลือกได้เลย ไม่ต้องพิมพ์ `ssh -i ... -p ...` ทุกครั้ง

> **แก้ไขคอนฟิกจาก VS Code:** F1 → **Remote-SSH: Open SSH Configuration File...** → เลือก `~/.ssh/config` → VS Code จะเปิดให้แก้พร้อมเติมคำสั่ง/ตัวเลือกให้อัตโนมัติ

---

## 8. เคล็ดลับและการใช้งาน

### 8.1 Reopen โปรเจกต์ล่าสุด

หลังเชื่อมต่อ host แล้ว เมนู **File → Open Recent** จะแสดงโฟลเดอร์บน server ที่เคยเปิด คลิกเปิดซ้ำได้เลย

### 8.2 เปิดเทอร์มินัล/พอร์ตการโอน (Port Forwarding)

VS Code ส่งต่อพอร์ตอัตโนมัติเมื่อ app บน server ฟังพอร์ต (เช่น `python -m http.server 8000`) ทำให้เปิดเว็บบน `localhost:8000` ของเครื่องเราได้เลย

- เมนู **Ports** ที่แถบล่าง (หรือ View → Ports) ดู/จัดการพอร์ตที่ส่งต่อ
- คลิกขวาพอร์ต → **Open in Browser**

### 8.3 Extension บน server

เมื่อเปิดโปรเจกต์บน server บาง extension (เช่น Python, ESLint, Prettier) ต้อง **ติดตั้งบน server** จึงจะทำงานกับไฟล์บน server ได้

- เปิดแผง Extensions จะเห็นสองส่วน: **Local - Installed** และ **SSH: <host> - Installed**
- ในส่วนของ host จะมีปุ่ม **Install in SSH: <host>** สำหรับ extension ที่ยังไม่ได้ติดตั้งบน server
- คลิกปุ่มนั้น รอติดตั้ง แล้วโหลดใหม่ (Reload Required)

### 8.4 ลบ VS Code Server ออกจาก server

VS Code Server ติดตั้งอยู่ที่ `~/.vscode-server/` บน server หากติดปัญหา/เวอร์ชันเก่า สามารถลบแล้วให้ติดตั้งใหม่ได้:

```bash
# บน server (ผ่าน ssh ปกติ)
rm -rf ~/.vscode-server
# หรือใช้คำสั่งจาก VS Code: F1 → Remote-SSH: Uninstall VS Code Server from Host...
```

ครั้งต่อไปที่เชื่อมต่อ VS Code จะติดตั้งส่วนประกอบใหม่ให้อัตโนมัติ

### 8.5 เลือก OS ของ server ล่วงหน้า

เพื่อไม่ให้ VS Code ถาม OS ทุกครั้ง เพิ่มใน `~/.ssh/config`:
```ssh-config
Host prod
    HostName 192.168.1.10
    User user
    IdentityFile ~/.ssh/id_ed25519
    RemoteCommand bash --login    # (optional)
```
หรือตั้งค่าใน VS Code: F1 → **Preferences: Open Settings (JSON)** → เพิ่ม:
```json
"remote.SSH.remoteServerListenOnSocket": true
```

### 8.6 ความปลอดภัย

- อย่าเปิดโฟลเดอร์ `/` หรือ `/etc` ทั้งโฟลเดอร์ — VS Code จะพยายาม index ทั้งหมด ช้าและกินทรัพยากร
- เปิดเฉพาะโฟลเดอร์โปรเจกต์เท่านั้น
- ใช้ public key auth แทกรหัสผ่านเมื่อทำได้ (ดู [PUBLICKEY.md](PUBLICKEY.md))

---

## 9. แก้ปัญหาที่พบบ่อย

| อาการ | สาเหตุ/วิธีแก้ |
|---|---|
| "Could not establish connection" | ลอง `ssh user@host` ใน terminal ก่อน ถ้าใน terminal ก็ไม่ติด แก้ฝั่ง SSH ก่อน |
| ถามรหัสผ่านทุกครั้ง | ตั้ง `~/.ssh/config` ใส่ `IdentityFile` + ใช้ key auth หรือเพิ่ม `AddKeysToAgent yes` |
| "The VS Code Server failed to start" | ลบ `~/.vscode-server` แล้วเชื่อมต่อใหม่ (ดู 8.4) |
| ติดตั้ง server ไม่สำเร็จ (พื้นที่ไม่พอ) | server ต้องมีพื้นที่ว่าง ~1 GB ที่ `~` ตรวจ `df -h ~` |
| รุ่นเซิร์ฟเวอร์เก่า (glibc ต่ำ) | ระบบต้องมี glibc ≥ 2.28 (เช่น Ubuntu 18.04+, Debian 10+, CentOS 7+ บางส่วน) ระบบเกว่านั้นใช้ไม่ได้ |
| Extension ไม่ทำงาน | ตรวจว่าติดตั้งบนส่วน **SSH: <host>** แล้วหรือยัง (ดู 8.3) |
| เชื่อมต่อช้า | เพิ่ม `ServerAliveInterval 60` ใน `~/.ssh/config` และตั้ง `"remote.SSH.serverInstallOnConnect": true` |
| โคลด้วย `code .` ไม่ได้ | บนเซิร์ฟเวอร์ไม่จำเป็นต้องมีคำสั่ง `code` ทุกอย่างทำผ่าน VS Code ฝั่ง local อยู่แล้ว |
| หน้าต่าง terminal เปิดที่ server ผิดโฟลเดอร์ | ใช้ `cd` ใน terminal หรือตั้ง `terminal.integrated.cwd` |

### ดู log การเชื่อมต่อ

- **F1 → Remote-SSH: Show Log** — ดู log ฝั่ง VS Code
- **F1 → Remote-SSH: Show Server Log** — ดู log ฝั่ง server
- **View → Output** → เลือก channel **Remote - SSH** ในดรอปดาวน์

### ตรวจสถานะ SSH บน server

```bash
sudo systemctl status ssh          # SSH daemon รันอยู่ไหม
sudo ss -tlnp | grep :22            # ฟังพอร์ต 22 ไหม
sudo ufw status                     # ไฟร์วอลล์เปิด 22 ไหม
df -h ~                             # พื้นที่ว่างพอไหม (ต้องการ ~1GB)
```

---

## สรุปลำดับขั้นโดยรวม

```bash
# 1. ดาวน์โหลด/ติดตั้ง VS Code (จาก https://code.visualstudio.com/Download)

# 2. ใน VS Code: ติดตั้ง extension "Remote - SSH" โดย Microsoft
#    (Ctrl+Shift+X → ค้น "Remote - SSH" → Install ของ Microsoft)

# 3. ตรวจว่า ssh เข้า server ได้ก่อน
ssh user@192.168.1.10

# 4. ใน VS Code: F1 → Remote-SSH: Connect to Host... → + Add New SSH Host...
#    ใส่: ssh user@192.168.1.10  (หรือ ssh -i ~/.ssh/id_ed25519 -p 2222 user@host)

# 5. รอ VS Code ติดตั้ง server component (~30 วินาที – 2 นาที)
#    ไอคอนมุมล่างซ้ายเป็นสีเขียว "SSH: host"

# 6. File → Open Folder... → เลือกโฟลเดอร์บน server เช่น /home/user/project

# 7. แก้ไขไฟล์/เปิด terminal (Ctrl+`) — ทุกอย่างรันบน server
```
