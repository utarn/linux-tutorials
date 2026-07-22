# คู่มือ SCP, SFTP และ FileZilla

เอกสารสอนการโอนย้ายไฟล์ระหว่างเครื่อง local กับ Linux server ผ่าน SSH — ทั้งบรรทัดคำสั่ง (`scp`/`rsync`) และแบบกราฟิก (FileZilla ผ่าน SFTP)

---

## สารบัญ

1. [แนวคิด SCP และ SFTP](#1-แนวคิด-scp-และ-sftp)
2. [ใช้ scp คัดลอกไฟล์](#2-ใช้-scp-คัดลอกไฟล์)
3. [ใช้ rsync ซิงค์ไฟล์ (ทางเลือกที่ดีกว่า)](#3-ใช้-rsync-ซิงค์ไฟล์-ทางเลือกที่ดีกว่า)
4. [ดาวน์โหลดและติดตั้ง FileZilla](#4-ดาวน์โหลดและติดตั้ง-filezilla)
5. [ตั้งค่า SFTP ใน FileZilla](#5-ตั้งค่า-sftp-ใน-filezilla)
6. [เชื่อมต่อและโอนย้ายไฟล์](#6-เชื่อมต่อและโอนย้ายไฟล์)
7. [ตั้งค่า FileZilla ให้ใช้ SSH Key](#7-ตั้งค่า-filezilla-ให้ใช้-ssh-key)
8. [แก้ปัญหาที่พบบ่อย](#8-แก้ปัญหาที่พบบ่อย)

---

## 1. แนวคิด SCP และ SFTP

- **SCP (Secure Copy Protocol)** — โอนไฟล์ผ่าน SSH แบบคำสั่งเดียวจบ เหมาะกับการคัดลอกไฟล์เป็นครั้งคราว
- **SFTP (SSH File Transfer Protocol)** — โอนไฟล์ผ่าน SSH แบบมี session (เหมือน FTP แต่เข้ารหัส) รองรับการเรียกดู/ลบ/สร้างโฟลเดอร์ ใช้กับโปรแกรมกราฟิกเช่น FileZilla
- **rsync** — โอนแบบซิงค์ ส่งเฉพาะส่วนที่เปลี่ยน ประหยัดแบนด์วิดท์ เหมาะกับไฟล์ใหญ่/โอนซ้ำ

ทั้งสามวิธีทำงานบนพอร์ต **22** (พอร์ต SSH) จึงใช้คีย์/รหัสผ่าน SSH เดียวกับที่ล็อกอินผ่าน `ssh` ปกติ

```
[ Local ]                           [ Remote Server ]
                ┌──── scp ────►
   file.txt     │                 /home/user/file.txt
                ◄──── sftp ────
                └──── rsync ──►
```

ก่อนเริ่ม: ต้องล็อกอิน server ด้วย SSH ได้แล้ว (`ssh user@host`) ถ้ายังไม่ได้ตั้ง SSH key ดูได้จาก [PUBLICKEY.md](PUBLICKEY.md)

---

## 2. ใช้ scp คัดลอกไฟล์

รูปแบบคำสั่ง:
```
scp [ตัวเลือก] ต้นทาง ปลายทาง
```
ต้นทาง/ปลายทางที่เป็น server จะอยู่ในรูป `user@host:เส้นทาง` ส่วนเครื่อง local ใช้เส้นทางธรรมดา

### 2.1 อัปโหลด (Local → Server)

```bash
# คัดลอกไฟล์เดียวขึ้น server
scp file.txt user@192.168.1.10:/tmp/
#                  └─ ปลายทางเป็นโฟลเดอร์ /tmp (ชื่อไฟล์เดิม)

# คัดลอกพร้อมเปลี่ยนชื่อ
scp file.txt user@192.168.1.10:/tmp/backup.txt

# คัดลอกทั้งโฟลเดอร์ขึ้น server (ต้องมี -r)
scp -r myproject user@192.168.1.10:/home/user/
```

### 2.2 ดาวน์โหลด (Server → Local)

```bash
# ดาวน์โหลดไฟล์จาก server มาเครื่องเรา
scp user@192.168.1.10:/var/log/syslog ./
#                                                   └─ โฟลเดอร์ปัจจุบัน

# ดาวน์โหลดทั้งโฟลเดอร์
scp -r user@192.168.1.10:/home/user/logs ./
```

### 2.3 ระหว่างสอง server (โอนตรง ไม่ผ่านเครื่องเรา)

```bash
scp user1@server1:/data/file.txt user2@server2:/data/
# -3  ใช้ถ้าต้องการให้เครื่อง local เป็นตัวกลาง (ช้ากว่า แต่ใช้ได้แม้ server สองตัวไม่รู้จักกัน)
scp -3 user1@server1:/data/file.txt user2@server2:/data/
```

### 2.4 ตัวเลือกที่ใช้บ่อย

| ตัวเลือก | ความหมาย |
|---|---|
| `-r` | คัดลอกแบบ recursive (สำหรับโฟลเดอร์) |
| `-P <port>` | ระบุพอร์ต SSH (ตัวใหญ่ P สำหรับ scp) |
| `-i <key>` | ระบุไฟล์ private key |
| `-C` | บีบอัดระหว่างทาง (ประหยัดแบนด์วิดท์ แต่ใช้ CPU) |
| `-v` | verbose สำหรับ debug |
| `-p` | รักษาเวลาแก้ไข/สิทธิ์ไฟล์เดิม (ตัวเล็ก p) |

**ตัวอย่าง:**
```bash
# ใช้พอร์ต 2222
scp -P 2222 file.txt user@192.168.1.10:/tmp/

# ใช้ SSH key เฉพาะ
scp -i ~/.ssh/id_ed25519 file.txt user@192.168.1.10:/tmp/

# บีบอัด + recursive
scp -Cr myproject user@192.168.1.10:/home/user/

# ใช้ร่วมกับ ~/.ssh/config (แนะนำ พิมพ์สั้นลง)
#    ถ้ามี: Host prod / HostName 192.168.1.10 / User user / IdentityFile ~/.ssh/id_ed25519
scp file.txt prod:/tmp/        # เท่ากับ scp -i ~/.ssh/id_ed25519 file.txt user@192.168.1.10:/tmp/
```

### 2.5 รวมเป็น tar ก่อนโอน (เร็วกว่า scp หลายไฟล์มาก)

`scp` โอนทีละไฟล์ ถ้ามีหลายพันไฟล์จะช้ามาก เทคนิคคือรวมเป็น tar ส่งผ่าน SSH ทีเดียว:

```bash
# ส่งโฟลเดอร์ไป server ผ่าน SSH (บีบ + ส่ง + แตก ทีเดียว)
tar czf - myproject | ssh user@192.168.1.10 "tar xzf - -C /home/user/"

# รับโฟลเดอร์จาก server มาเครื่องเรา
ssh user@192.168.1.10 "tar czf - /var/log" | tar xzf - -C ./
```

---

## 3. ใช้ rsync ซิงค์ไฟล์ (ทางเลือกที่ดีกว่า)

`rsync` โอนเฉพาะส่วนที่เปลี่ยน เร็วและประหยัดกว่า `scp` ตอนโอนซ้ำ/ไฟล์ใหญ่

```bash
# ซิงค์โฟลเดอร์ local ขึ้น server (สังเกต / ปิดท้ายต้นทาง)
rsync -avz myproject/ user@192.168.1.10:/home/user/myproject/
# -a  archive (รักษาสิทธิ์/เวลา/symlink/recursive)
# -v  verbose (แสดงรายการที่โอน)
# -z  บีบอัดระหว่างทาง

# ซิงค์จาก server ลง local
rsync -avz user@192.168.1.10:/var/log/ ./logs/

# ลบไฟล์ที่ปลายทางไม่มีในต้นทางด้วย (mirror)
rsync -avz --delete myproject/ user@192.168.1.10:/home/user/myproject/

# ใช้พอร์ต 2222
rsync -avz -e "ssh -p 2222" myproject/ user@192.168.1.10:/home/user/myproject/

# ทดสอบก่อนโอนจริง (dry-run — แสดงว่าจะทำอะไร แต่ไม่ทำจริง)
rsync -avz --dry-run myproject/ user@192.168.1.10:/home/user/myproject/
```

> **สำคัญเรื่อง `/` ปิดท้าย:** `folder/` คือ "เนื้อหาข้างใน folder" ส่วน `folder` คือ "ตัวโฟลเดอร์เอง" เช่น
> - `rsync -avz src/ dest/` → คัดลอก *เนื้อหา* ของ src ไปไว้ใน dest
> - `rsync -avz src dest/` → คัดลอก *โฟลเดอร์* src ไปไว้ใน dest (ได้ dest/src/)

---

## 4. ดาวน์โหลดและติดตั้ง FileZilla

FileZilla เป็นโปรแกรม FTP/SFTP แบบกราฟิกฟรี มีทั้งเวอร์ชันหน้าต่าง/แท็บและแบบไม่มี UI (FileZilla Server สำหรับทำ server — เราใช้แค่ client)

> **ดาวน์โหลดเฉพาะ "FileZilla Client"** (โปรแกรมสำหรับเชื่อมต่อ) ไม่ใช่ Server

### 4.1 Windows

1. เข้า https://filezilla-project.org/download.php?type=client
   (หรือเว็บหลัก https://filezilla-project.org → Download → Download FileZilla Client)
2. คลิก **Download FileZilla Client** — ระบบจะตรวจ OS ให้อัตโนมัติ
3. **ระวัง:** หน้าดาวน์โหลดจะมีปุ่ม "Free Download" หลายปุ่ม (โฆษณา/ตัวติดตั้งแอปอื่น) — ให้เลือกปุ่มที่เป็น **"Download FileZilla Client" สีเขียว** ของ filezilla-project.org เท่านั้น
4. ดาวน์โหลดไฟล์ `.exe` แล้วเปิดรัน
5. เลือกภาษา → กด I Agree → เลือกผู้ใช้ (Anyone/Only for me) → Next → Next → Install → Finish

> **ทางเลือกที่สะอาดกว่า (ไม่โชว์โฆษณา):** ใช้ winget ใน PowerShell
> ```powershell
> winget install --id FileZilla.FileZilla -e
> ```
> หรือใช้ Chocolatey: `choco install filezilla`

### 4.2 macOS

1. เข้า https://filezilla-project.org/download.php?type=client
2. ดาวน์โหลดไฟล์ `.dmg` สำหรับ macOS
3. เปิด `.dmg` → ลาก **FileZilla** ไปไว้ในโฟลเดอร์ Applications
4. ครั้งแรกที่เปิด: คลิกขวา → Open → กด Open อีกครั้ง (เพราะไม่ได้ติดตั้งผ่าน App Store)

หรือใช้ Homebrew:
```bash
brew install --cask filezilla
```

### 4.3 Linux

```bash
# Debian/Ubuntu
sudo apt update && sudo apt install -y filezilla

# Fedora
sudo dnf install filezilla

# Arch
sudo pacman -S filezilla
```
หรือดาวน์โหลด Flatpak: `flatpak install flathorg.filezillla` (ดู ID จริงใน flathub.org)

เปิดโปรแกรมได้จากเมนู Applications หรือพิมพ์ `filezilla` ใน terminal

---

## 5. ตั้งค่า SFTP ใน FileZilla

การเชื่อมต่อผ่าน **SFTP** ปลอดภัยกว่า FTP ธรรมดา เพราะเข้ารหัสและใช้บัญชี SSH ของ server

### 5.1 เชื่อมต่อแบบด่วน (Quickconnect)

ด้านบนของหน้าต่าง FileZilla จะมีแถบ Quickconnect:

| ช่อง | ใส่ค่า | ตัวอย่าง |
|---|---|---|
| Host | `sftp://` นำหน้า IP/domain | `sftp://192.168.1.10` |
| Username | ชื่อผู้ใช้บน server | `user` |
| Password | รหัสผ่าน (ถ้ามี) | ใส่หรือเว้นว่างถ้าใช้ key |
| Port | 22 | `22` |

1. ใส่ค่าแล้วกด **Quickconnect**
2. ครั้งแรกจะมีหน้าต่างถาม "Unknown server key" → เลือก **Always trust this host** → กด OK
3. เชื่อมต่อสำเร็จจะเห็นไฟล์ทั้งสองด้าน (ซ้าย=local, ขวา=server)

> **สำคัญ:** ต้องมี `sftp://` นำหน้า Host ถ้าไม่ใส่ FileZilla จะใช้ FTP ธรรมดา (พอร์ต 21) ซึ่งส่วนใหญ่ server ปิดไว้

### 5.2 บันทึกเป็น Site Manager (ใช้บ่อย/หลาย server)

1. เมนู **File → Site Manager** (หรือ Ctrl+S / Cmd+S)
2. กด **New Site** — ตั้งชื่อ เช่น `prod-server`
3. แท็บ **General**:

| ช่อง | ค่าที่ใส่ |
|---|---|
| Protocol | **SFTP - SSH File Transfer Protocol** |
| Host | `192.168.1.10` (หรือ domain) |
| Port | `22` (หรือพอร์ต SSH ของ server) |
| Logon Type | เลือกตามวิธีล็อกอิน (ด้านล่าง) |
| User | ชื่อผู้ใช้บน server |

**Logon Type ที่เลือกได้:**

- **Ask for password** — ถามรหัสผ่านทุกครั้ง (ปลอดภัย ไม่เก็บรหัส)
- **Normal** — เก็บรหัสผ่านไว้ใน FileZilla (สะดวก แต่เก็บใน site manager ไม่เข้ารหัสชัด ๆ)
- **Key file** — ใช้ SSH private key (แนะนำ ถ้า server ใช้ public key auth — ดูหัวข้อ 7)
- **Interactive** — ใช้กับ keyboard-interactive auth

4. กด **Connect** เพื่อทดสอบ หรือ **OK** เพื่อบันทึกเก็บไว้
5. ครั้งต่อไปเปิด Site Manager → เลือก site → Connect

---

## 6. เชื่อมต่อและโอนย้ายไฟล์

หลังเชื่อมต่อสำเร็จ หน้าต่างแบ่งเป็น 4 ส่วน:

```
┌─────────────────────────────────────────────┐
│  ข้อความ log (สถานะการเชื่อมต่อ)            │
├──────────────────┬──────────────────────────┤
│  Local (เครื่อง) │  Remote (server)         │
│  (ซ้าย)          │  (ขวา)                   │
│                  │                          │
│  /Users/me       │  /home/user              │
│  ├── docs/       │  ├── logs/               │
│  └── file.txt    │  └── app/                │
├──────────────────┴──────────────────────────┤
│  คิวการโอน (ที่กำลังโอน/รอโอน)               │
└─────────────────────────────────────────────┘
```

### การโอนไฟล์

- **อัปโหลด:** ลากไฟล์จาก **ซ้าย (local)** ไป **ขวา (server)** — หรือคลิกขวาไฟล์ฝั่งซ้าย → Upload
- **ดาวน์โหลด:** ลากจาก **ขวา** ไป **ซ้าย** — หรือคลิกขวาฝั่งขวา → Download
- **ลากหลายไฟล์:** กด Ctrl/Cmd+คลิกเลือกหลายไฟล์แล้วลาก
- **โอนโฟลเดอร์:** ลากทั้งโฟลเดอร์ได้เลย (FileZilla จะ recursive ให้)

### เปลี่ยนตำแหน่งเริ่มต้น

- ด้านซ้าย (local): ใช้แถบที่อยู่ด้านบนของช่อง local หรือเมนูข้างบน
- ด้านขวา (server): ดับเบิลคลิกโฟลเดอร์เพื่อเข้า หรือพิมพ์เส้นทางในแถบที่อยู่
- **ท่าที่ใช้บ่อย:** เปลี่ยนฝั่งซ้ายไปโฟลเดอร์ที่จะโอน และฝั่งขวาไปปลายทางที่จะวาง แล้วลากข้าม

### คำสั่งอื่นในเมนูคลิกขวา

- **Create directory** — สร้างโฟลเดอร์ใหม่
- **Delete** — ลบไฟล์/โฟลเดอร์
- **Rename** — เปลี่ยนชื่อ
- **File permissions…** — เปลี่ยนสิทธิ์ (เทียบเท่า `chmod`, เช่นตั้ง 755/644)
- **File size** / **Date modified** — ดูขนาด/เวลา

### ดูคิวและยกเลิก

- แผงล่างสุดแสดงไฟล์ที่กำลังโอนและคิวรอ
- คลิกขวาไฟล์ในคิว → **Cancel** เพื่อยกเลิกการโอนนั้น
- เมนู **Transfer → Cancel** ยกเลิกทั้งหมด

---

## 7. ตั้งค่า FileZilla ให้ใช้ SSH Key

ถ้า server ใช้ public key authentication (ปิด password auth) ต้องตั้ง FileZilla ให้ใช้ private key

### กรณี key รูปแบบ OpenSSH (ที่ได้จาก `ssh-keygen`)

FileZilla รองรับไฟล์ private key ของ OpenSSH (`~/.ssh/id_ed25519` หรือ `id_rsa`) โดยตรง

1. เปิด **File → Site Manager** → เลือก site → แท็บ General
2. เปลี่ยน **Logon Type** เป็น **Key file**
3. ช่อง **User** ใส่ชื่อผู้ใช้บน server
4. ช่อง **Key file** กด **Browse…** → เลือกไฟล์ private key:
   - Windows: `C:\Users\<ชื่อผู้ใช้>\.ssh\id_ed25519`
   - macOS/Linux: `~/.ssh/id_ed25519`
5. กด **Connect**

> **ถ้า key มี passphrase:** FileZilla จะถาม passphrase ทุกครั้งที่เชื่อมต่อ (ไม่สามารถใช้ ssh-agent แบบ terminal ได้)

### กรณี key รูปแบบ PuTTY (`.ppk`)

FileZilla รองรับ `.ppk` โดยตรงเช่นกัน — เลือกไฟล์ `.ppk` ในช่อง Key file ได้เลย

### แปลง key (ถ้าจำเป็น)

FileZilla มีเครื่องมือแปลง key ในตัว:

1. เมนู **Edit → Settings** (Windows) หรือ **FileZilla → Settings** (macOS)
2. ไปที่ **SFTP** ในซ้าย → กด **Add key file…**
3. เลือกไฟล์ private key รูปแบบ OpenSSH (`id_ed25519`)
4. FileZilla จะถามจะแปลงเป็นรูปแบบของตัวเองหรือไม่ → กด **Yes**
5. บันทึกไฟล์ `.ppk` ที่ได้ แล้วใช้ไฟล์นี้ใน Site Manager

วิธีนี้ทำให้ใช้ key กับหลาย site ได้โดยไม่ต้องตั้ง key file ให้แต่ละ site ซ้ำ ๆ

### ตั้งค่า global (ใช้ key เดียวกับทุก site)

1. **Edit → Settings → SFTP**
2. กด **Add key file…** → เลือก private key
3. ใน Site Manager ใช้ Logon Type **Normal** หรือ **Ask for password** (เว้นรหัส) — FileZilla จะใช้ key จาก global โดยอัตโนมัติ

---

## 8. แก้ปัญหาที่พบบ่อย

| อาการ | สาเหตุ/วิธีแก้ |
|---|---|
| `Connection refused` | พอร์ตผิด หรือ SSH บน server ไม่ได้ฟังพอร์ตนั้น ตรวจด้วย `ss -tlnp \| grep ssh` บน server |
| `Connection timed out` | ไฟร์วอลล์บน server/client บล็อกพอร์ต 22 หรือ IP ผิด ตรวจ `sudo ufw status` |
| `Authentication failed` | รหัสผ่านผิด, หรือใช้ key แต่ Logon Type ยังเป็น Normal ให้เปลี่ยนเป็น Key file |
| `Permission denied` หลังเข้าได้ | ไม่มีสิทธิ์อ่าน/เขียนโฟลเดอร์ปลายทาง ลองโอนไป `~` (home) ก่อน หรือตั้งสิทธิ์โฟลเดอร์ด้วย `chmod`/`chown` |
| โอนแล้วเสีย (ไฟล์เสีย) | ตรวจโหมดโอนใน **Edit → Settings → Transfers → File types** ตั้งเป็น **Binary** (ไม่ใช่ ASCII) เพื่อกันการแปลง line-ending |
| โอนช้ามาก | ถ้าไฟล์เยอะ `scp` จะช้ากว่า `rsync`/tar หรือใน FileZilla เพิ่มจำนวนการโอนพร้อมกันใน Settings → Transfers |
| ไฟล์ที่โอนขึ้น server รันไม่ได้ | สิทธิ์ execute หาย คลิกขวาใน FileZilla → File permissions → ตั้ง 755 หรือ `chmod +x` ฝั่ง server |
| ล็อกอินด้วย key ไม่ติด | ตรวจสิทธิ์ `~/.ssh` (700) และ `~/.ssh/authorized_keys` (600) บน server — ดูรายละเอียดใน [PUBLICKEY.md](PUBLICKEY.md) |
| FileZilla โชว์โฆษณา/ติดตั้งแอปขยะ | ดาวน์โหลดจาก filezilla-project.org โดยตรง หรือใช้ winget/Homebrew/apt แทน |

### ตรวจสถานะ SSH บน server

```bash
sudo systemctl status ssh          # SSH daemon รันอยู่ไหม
sudo ss -tlnp | grep :22            # ฟังพอร์ต 22 ไหม
sudo ufw status                     ไฟร์วอลล์เปิดพอร์ต 22 ไหม
sudo tail -f /var/log/auth.log      # ดู log การล็อกอิน (Debian/Ubuntu)
```

---

## สรุปเลือกวิธีตามสถานการณ์

| สถานการณ์ | แนะนำ |
|---|---|
| โอนไฟล์เดียวเป็นครั้งคราว | `scp` |
| ซิงค์โฟลเดอร์ใหญ่/โอนซ้ำ | `rsync` |
| โอนไฟล์เป็นพันชิ้น | `tar \| ssh` |
| ดู/แก้ไฟล์แบบลากวาง (GUI) | **FileZilla** (SFTP) |
| ใช้ key auth บน FileZilla | Site Manager → Logon Type: **Key file** |
