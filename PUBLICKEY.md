# คู่มือ SSH Public Key Authentication

เอกสารอธิบายการสร้าง SSH key บน Windows และ Linux, การนำไปใช้ยืนยันตัวตนกับ Linux Server (public key authentication), การจัดการ `authorized_keys`, และการตั้งค่า `~/.ssh/config` เพื่อกำหนด host/IP/user ล่วงหน้า

---

## สารบัญ

1. [แนวคิด Public Key Authentication](#1-แนวคิด-public-key-authentication)
2. [สร้าง SSH Key บน Linux/macOS](#2-สร้าง-ssh-key-บน-linuxmacos)
3. [สร้าง SSH Key บน Windows](#3-สร้าง-ssh-key-บน-windows)
4. [คัดลอก Public Key ไปยัง Server](#4-คัดลอก-public-key-ไปยัง-server)
5. [จัดการ authorized_keys ด้วยมือ](#5-จัดการ-authorized_keys-ด้วยมือ)
6. [ตั้งค่า ~/.ssh/config](#6-ตั้งค่า-sshconfig)
7. [ตรวจสอบและแก้ปัญหา](#7-ตรวจสอบและแก้ปัญหา)
8. [ปิดการล็อกอินด้วยรหัสผ่าน (ฮาร์ดเดนิ่ง)](#8-ปิดการล็อกอินด้วยรหัสผ่าน-ฮาร์ดเดนิ่ง)

---

## 1. แนวคิด Public Key Authentication

Public Key Authentication คือวิธีล็อกอินโดยใช้ **คู่กุญแจ (key pair)** แทนรหัสผ่าน

- **Private Key** (กุญแจส่วนตัว) — เก็บไว้ที่เครื่อง **ลูกข่าว/ผู้ใช้** (client) เท่านั้น ห้ามส่งให้ใคร ห้าม commit ขึ้น git
- **Public Key** (กุญแจสาธารณะ) — นำไปวางไว้ที่ **เซิร์ฟเวอร์** (ในไฟล์ `authorized_keys`) ส่งให้คนอื่นได้ ไม่เสียหาย

เวลาล็อกอิน เซิร์ฟเวอร์จะท้าทายด้วยโจทย์ที่แก้ได้ด้วย private key เท่านั้น — จึงไม่ต้องส่งรหัสผ่านผ่านเน็ตเวิร์ก ปลอดภัยกว่าและสะดวกกว่า

```
[ Client (เครื่องเรา) ]              [ Server ]
  ~/.ssh/id_ed25519   ──── ล็อกอิน ────►  ~/.ssh/authorized_keys
  (private key)                       (มี public key ของเราอยู่ข้างใน)
```

**ประเภท key ที่แนะนำ:**

| ประเภท | คำสั่งสร้าง | ขนาด | หมายเหตุ |
|---|---|---|---|
| **ed25519** | `ssh-keygen -t ed25519` | เล็ก/เร็ว/ปลอดภัย | **แนะนำ** (modern, ทุก OS ใหม่รองรับ) |
| RSA | `ssh-keygen -t rsa -b 4096` | ใหญ่กว่า | ใช้เมื่อระบบเก่าไม่รองรับ ed25519 |
| ECDSA | `ssh-keygen -t ecdsa` | — | มีข้อถกเถียงเรื่องการสุ่ม ไม่แนะนำ |

---

## 2. สร้าง SSH Key บน Linux/macOS

เปิด Terminal แล้วรัน:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# -t ed25519   ประเภท key (แนะนำ)
# -C "..."     comment ช่วยจำว่า key นี้ของใคร/เครื่องไหน
```

ระบบจะถาม:

1. **ตำแหน่งเก็บไฟล์** — กด Enter เพื่อใช้ค่าเริ่มต้น `~/.ssh/id_ed25519`
2. **Passphrase** — รหัสผ่านป้องกัน private key (แนะนำตั้ง ถ้าไม่ตั้งกด Enter)
3. **ยืนยัน passphrase** อีกครั้ง

ผลลัพธ์คือไฟล์ 2 ไฟล์ใน `~/.ssh/`:

```
~/.ssh/id_ed25519       ← Private key (ห้ามแชร์ ห้าม chmod เปิดกว้าง)
~/.ssh/id_ed25519.pub   ← Public key (ส่งให้ server ได้)
```

**ตัวอย่างเพิ่มเติม:**

```bash
# สร้าง key แบบเก็บไฟล์ชื่อเฉพาะ (กรณีมีหลาย key)
ssh-keygen -t ed25519 -f ~/.ssh/key_github -C "key for github"

# สร้างแบบไม่ถาม passphrase (สำหรับ automation/CI — ระวังความปลอดภัย)
ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519

# สร้าง RSA 4096-bit (สำหรับระบบเก่า)
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

**ดู public key ที่สร้าง:**
```bash
cat ~/.ssh/id_ed25519.pub
# ผลลัพธ์ประมาณ:
# ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... your_email@example.com
```

### ตั้งสิทธิ์ไฟล์ให้ถูกต้อง (สำคัญ!)

SSH จะ **ปฏิเสธ** private key ที่สิทธิ์เปิดกว้างเกินไป:

```bash
chmod 700 ~/.ssh              # โฟลเดอร์ .ssh ต้องเป็น 700
chmod 600 ~/.ssh/id_ed25519   # private key ต้องเป็น 600 (เจ้าของอ่าน+เขียนอย่างเดียว)
chmod 644 ~/.ssh/id_ed25519.pub   # public key ให้คนอื่นอ่านได้ (ไม่บังคับ แต่เป็นมาตรฐาน)
```

---

## 3. สร้าง SSH Key บน Windows

บน Windows ใช้ **OpenSSH ในตัว** (Windows 10/11 มาให้)

### ใช้ OpenSSH (Windows 10/11)

เปิด **PowerShell** หรือ **Command Prompt** แล้วรัน:

```powershell
ssh-keygen -t ed25519 -C "your_email@example.com"
```

ขั้นตอนเหมือน Linux ทุกประการ — ระบบจะถามตำแหน่งและ passphrase

ตำแหน่งเก็บไฟล์เริ่มต้นบน Windows:

```
C:\Users\<ชื่อผู้ใช้>\.ssh\id_ed25519       ← Private key
C:\Users\<ชื่อผู้ใช้>\.ssh\id_ed25519.pub   ← Public key
```

ดู public key:
```powershell
cat $env:USERPROFILE\.ssh\id_ed25519.pub
# หรือ
type %USERPROFILE%\.ssh\id_ed25519.pub   (ใน CMD)
```

> **หาก `ssh-keygen` ไม่พบ:** ไปที่ Settings → Apps → Optional features → Add a feature → เพิ่ม "OpenSSH Client"
> หรือเปิดผ่าน PowerShell สิทธิผู้ดูแล:
> `Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0`

---

## 4. คัดลอก Public Key ไปยัง Server

### วิธีที่ 4.1 — ใช้ `ssh-copy-id` (ง่ายที่สุด, Linux/macOS)

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@192.168.1.10
# -i   ระบุไฟล์ public key ที่จะส่ง (ถ้าไม่ระบุจะใช้ค่าเริ่มต้น)
# user@...   ชื่อผู้ใช้และ IP/ชื่อโฮสต์ของ server
```

คำสั่งนี้จะ:
1. เข้า server ด้วยรหัสผ่าน (ครั้งสุดท้าย)
2. แปะ public key ต่อท้ายไฟล์ `~/.ssh/authorized_keys` บน server
3. ตั้งสิทธิ์ไฟล์/โฟลเดอร์ให้ถูกต้องอัตโนมัติ

**กรณี server ใช้พอร์ต SSH ไม่ใช่ 22:**
```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub -p 2222 user@192.168.1.10
```

ลองล็อกอินใหม่ — ควรเข้าได้โดยไม่ต้องใส่รหัสผ่าน (หรือใส่แค่ passphrase ของ key):
```bash
ssh user@192.168.1.10
```

> **บน Windows ไม่มี `ssh-copy-id`** ใช้วิธี 4.2 หรือ 4.3 แทน หรือติดตั้งผ่าน Git Bash / WSL

### วิธีที่ 4.2 — คัดลอกด้วยมือ (ใช้ได้ทุก OS, รวม Windows)

**Linux/macOS:**
```bash
cat ~/.ssh/id_ed25519.pub | ssh user@192.168.1.10 "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

**Windows PowerShell:**
```powershell
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub | ssh user@192.168.1.10 "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

### วิธีที่ 4.3 — คัดลอกเองทีละขั้น (เข้าใจกระบวนการ)

1. ดู/คัดลอกเนื้อหา public key จากเครื่อง client:
```bash
cat ~/.ssh/id_ed25519.pub
# คัดลอกข้อความทั้งบรรทัด
```

2. ล็อกอินเข้า server (ยังใช้รหัสผ่าน):
```bash
ssh user@192.168.1.10
```

3. บน server สร้างโฟลเดอร์และไฟล์ แล้ววาง key:
```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/authorized_keys        # วาง public key ที่คัดลอกมา แล้วบันทึก
chmod 600 ~/.ssh/authorized_keys
```

4. ออกจาก server แล้วลองล็อกอินใหม่:
```bash
exit
ssh user@192.168.1.10           # ควรเข้าได้โดยไม่ต้องใส่รหัสผ่าน
```

---

## 5. จัดการ authorized_keys ด้วยมือ

ไฟล์ `~/.ssh/authorized_keys` บน server คือ "รายชื่อ public key ที่อนุญาตให้ล็อกอินได้" — หนึ่ง key ต่อบรรทัด

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... key-for-laptop
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... key-for-desktop
ssh-rsa AAAAB3NzaC1yc2EAAAADAQAB... deploy-key
```

**ดู key ทั้งหมดที่มีอยู่:**
```bash
cat ~/.ssh/authorized_keys
wc -l ~/.ssh/authorized_keys        # นับจำนวน key
```

**เพิ่ม key ใหม่ (เพิ่มท้ายไฟล์):**
```bash
echo "ssh-ed25519 AAAA... new-key" >> ~/.ssh/authorized_keys
```

**ลบ key (ตัวอย่างลบบรรทัดที่มีคำว่า old-laptop):**
```bash
sed -i '/old-laptop/d' ~/.ssh/authorized_keys
# -i    แก้ไฟล์ในตัว
# /old-laptop/d   ลบบรรทัดที่มีคำว่า old-laptop
```

> **เคล็ดลับ:** ใส่ comment ท้ายแต่ละ key (หลังชื่อ key type) เพื่อจำให้ได้ว่า key นั้นของเครื่อง/คนไหน จะได้ลบถูกตอนเลิกใช้

**สิทธิ์ไฟล์ที่ถูกต้อง (SSH จะปฏิเสธถ้าผิด):**
```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
chown -R $USER:$USER ~/.ssh     # เจ้าของต้องเป็นผู้ใช้ที่ล็อกอิน
```

---

## 6. ตั้งค่า ~/.ssh/config

ไฟล์ `~/.ssh/config` ใช้บันทึก "โปรไฟล์" ของแต่ละ server ล่วงหน้า เพื่อให้ล็อกอินด้วยชื่อสั้น ๆ แทนการพิมพ์ user/IP/พอร์ต/key ยาว ๆ ทุกครั้ง

### ตำแหน่งไฟล์

| OS | ตำแหน่ง |
|---|---|
| Linux/macOS | `~/.ssh/config` |
| Windows | `C:\Users\<ชื่อผู้ใช้>\.ssh\config` |

สร้าง/แก้ไขไฟล์ (เครื่อง client):
```bash
nano ~/.ssh/config        # Linux/macOS
notepad %USERPROFILE%\.ssh\config    # Windows CMD
```

ตั้งสิทธิ์ (Linux/macOS):
```bash
chmod 600 ~/.ssh/config
```

### รูปแบบพื้นฐาน

```ssh-config
Host <ชื่อเล่นที่จะใช้พิมพ์>
    HostName <IP หรือ domain>
    User <ชื่อผู้ใช้บน server>
    Port <พอร์ต SSH, ค่าเริ่มต้น 22>
    IdentityFile <ตำแหน่ง private key>
```

### ตัวอย่างที่ 1 — คอนฟิกหลาย server

```ssh-config
# === เซิร์ฟเวอร์โปรดักชัน ===
Host prod
    HostName 203.0.113.10
    User ubuntu
    Port 22
    IdentityFile ~/.ssh/id_ed25519

# === เซิร์ฟเวอร์สเตจจิง (พอร์ตไม่ใช่ 22) ===
Host staging
    HostName staging.example.com
    User deploy
    Port 2222
    IdentityFile ~/.ssh/key_staging

# === เซิร์ฟเวอร์ภายใน (ผ่าน jump host) ===
Host internal
    HostName 10.0.0.50
    User admin
    IdentityFile ~/.ssh/id_ed25519
    ProxyJump jump                  # กระโดดผ่าน host "jump" ก่อน

Host jump
    HostName 203.0.113.99
    User ubuntu
    IdentityFile ~/.ssh/id_ed25519
```

หลังบันทึก ล็อกอินได้แค่พิมพ์ชื่อเล่น:
```bash
ssh prod           # เท่ากับ ssh -i ~/.ssh/id_ed25519 -p 22 ubuntu@203.0.113.10
ssh staging
ssh internal       # จะกระโดดผ่าน jump ให้อัตโนมัติ
scp file.txt prod:/tmp/     # ใช้กับ scp ได้ด้วย
rsync -avz folder/ prod:/var/www/   # และ rsync ด้วย
```

### ตัวอย่างที่ 2 — ใช้ wildcard และค่าทั่วไป

```ssh-config
# ค่าเริ่มต้นใช้กับทุก host ที่ไม่ได้ระบุเป็นพิเศษ
Host *
    ServerAliveInterval 60        # ส่ง keepalive ทุก 60 วินาที (ป้องกัน disconnect)
    ServerAliveCountMax 3
    AddKeysToAgent yes             # เพิ่ม key เข้า ssh-agent อัตโนมัติ

# ค่าเริ่มต้นสำหรับโฮสต์ *.example.com ทั้งหมด
Host *.example.com
    User deploy
    IdentityFile ~/.ssh/id_ed25519

Host prod.example.com
    Port 2222                      # โอเวอร์ไรด์พอร์ตเฉพาะ host นี้
```

### ตัวอย่างที่ 3 — ใช้ key หลายตัว (GitHub สำหรับหลายบัญชี)

```ssh-config
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/key_personal

Host github-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/key_work
```

โคลนด้วย `git clone git@github-work:org/repo.git` จะใช้ key งาน

### ตัวเลือกที่ใช้บ่อยใน config

| ตัวเลือก | ความหมาย |
|---|---|
| `Host` | ชื่อเล่น/pattern ที่จะพิมพ์ |
| `HostName` | IP หรือ domain จริงของ server |
| `User` | ชื่อผู้ใช้บน server |
| `Port` | พอร์ต SSH |
| `IdentityFile` | ตำแหน่ง private key |
| `ProxyJump` | กระโดดผ่าน host อื่นก่อน (jump/bastion host) |
| `ServerAliveInterval` | ส่ง keepalive ทุก N วินาที |
| `ForwardAgent` | ส่งต่อ ssh-agent (สำหรับ git บน server) |
| `LocalForward` | ทำ port forwarding ฝั่ง local |
| `IdentitiesOnly` | บังคับใช้ key ที่ระบุ ไม่ลอง key อื่น |

---

## 7. ตรวจสอบและแก้ปัญหา

### ตรวจสถานะการล็อกอินโดยละเอียด

```bash
ssh -v user@192.168.1.10          # verbose (ปานกลาง)
ssh -vv user@192.168.1.10         # verbose มาก
ssh -vvv user@192.168.1.10        # verbose สุด (ดูทุกขั้นตอน auth)
```

### ตรวจสิทธิ์ไฟล์บน server (สาเหตุ No.1 ของการล็อกอินไม่ติด)

```bash
ls -ld ~/.ssh                      # ต้องเป็น drwx------ (700)
ls -l ~/.ssh/authorized_keys       # ต้องเป็น -rw------- (600)
```

แก้ไข:
```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
chown -R $USER:$USER ~/.ssh        # เจ้าของต้องเป็นผู้ใช้ที่ล็อกอิน
```

### ดู log ของ SSH daemon บน server

```bash
sudo journalctl -u ssh -n 50 --no-pager     # systemd (Ubuntu/Debian ใหม่)
sudo journalctl -u sshd -n 50 --no-pager    # บาง distro ใช้ชื่อ sshd
sudo tail -f /var/log/auth.log              # Debian/Ubuntu
sudo tail -f /var/log/secure                # RHEL/CentOS
```

### ปัญหาที่พบบ่อย

| อาการ | สาเหตุที่เป็นไปได้ | วิธีแก้ |
|---|---|---|
| ยังขอรหัสผ่าน | public key ไม่ได้อยู่ใน `authorized_keys` | รัน `ssh-copy-id` ใหม่ หรือเช็คไฟล์ |
| ยังขอรหัสผ่าน | สิทธิ์ `~/.ssh` หรือ `authorized_keys` เปิดกว้างเกิน | `chmod 700 ~/.ssh; chmod 600 ~/.ssh/authorized_keys` |
| `Permission denied (publickey)` | server ปิด password auth และ key ไม่ตรง | ตรวจ key ที่ส่งไป, เช็ค `sshd_config` |
| ใช้ key ผิดตัว | มีหลาย key ใน `~/.ssh` | ระบุ `-i` หรือตั้ง `IdentityFile` ใน config, เพิ่ม `IdentitiesOnly yes` |
| เครื่อง client ขอ passphrase ทุกครั้ง | ไม่ได้ใช้ ssh-agent | รัน `ssh-add` (ดูด้านล่าง) |
| เชื่อมต่อช้า | DNS reverse lookup บน server | เพิ่ม `UseDNS no` ใน `sshd_config` |

### ใช้ ssh-agent เก็บ passphrase (ไม่ต้องใส่ทุกครั้ง)

```bash
eval "$(ssh-agent -s)"            # เริ่ม agent (Linux/macOS)
ssh-add ~/.ssh/id_ed25519          # เพิ่ม key (จะขอ passphrase ครั้งเดียว)
ssh-add -l                         # ดู key ที่อยู่ใน agent
ssh-add -D                         # ล้าง key ทั้งหมดออกจาก agent
```

บน macOS ใช้ keychain เก็บ passphrase ถาวร:
```bash
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
# และเพิ่มใน ~/.ssh/config:
#   Host *
#       UseKeychain yes
#       AddKeysToAgent yes
```

บน Windows (OpenSSH) เพิ่มใน config:
```ssh-config
Host *
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```
และเริ่ม ssh-agent service:
```powershell
# รัน PowerShell สิทธิผู้ดูแล
Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent
ssh-add $env:USERPROFILE\.ssh\id_ed25519
```

---

## 8. ปิดการล็อกอินด้วยรหัสผ่าน (ฮาร์ดเดนิ่ง)

เมื่อแน่ใจว่าล็อกอินด้วย key ได้แล้ว ให้ปิดรหัสผ่านเพื่อความปลอดภัย (ป้องกัน brute force)

แก้ไฟล์ `/etc/ssh/sshd_config` บน server:
```bash
sudo nano /etc/ssh/sshd_config
```

เปลี่ยน/เพิ่มค่า:
```ssh-config
PasswordAuthentication no          # ปิดล็อกอินด้วยรหัสผ่าน
PubkeyAuthentication yes           # เปิด public key (ค่าเริ่มต้นคือ yes อยู่แล้ว)
PermitRootLogin prohibit-password  # root ล็อกอินได้แค่ด้วย key (หรือ "no" เพื่อห้ามเลย)
```

ทดสอบคอนฟิกก่อนรีสตาร์ท (กันพลาดทำเข้า server ไม่ได้):
```bash
sudo sshd -t                       # ตรวจ syntax ถ้าไม่มี error คือผ่าน
```

รีโหลด/รีสตาร์ท sshd:
```bash
sudo systemctl reload ssh          # โหลดใหม่โดยไม่ตัด connection เดิม (ปลอดภัยกว่า)
# หรือ
sudo systemctl restart ssh
sudo systemctl restart sshd        # บาง distro ใช้ชื่อนี้
```

> **คำเตือน:** ก่อนปิด PasswordAuthentication ให้ **เปิดเทอร์มินัลล็อกอินเดิมค้างไว้** แล้วเปิดเทอร์มินัลใหม่ทดสอบล็อกอินด้วย key ก่อน ถ้าล็อกอินด้วย key ไม่ติด จะได้ยังมี session เดิมอยู่ให้แก้คอนฟิกคืนได้ — อย่าปิดหน้าต่างเดิมจนกว่าจะแน่ใจ

---

## สรุปลำดับขั้นโดยรวม

```bash
# 1. (Client) สร้าง key
ssh-keygen -t ed25519 -C "your_email@example.com"

# 2. (Client) ตั้งสิทธิ์ private key
chmod 600 ~/.ssh/id_ed25519

# 3. (Client → Server) ส่ง public key ไป server
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@192.168.1.10

# 4. (Client) ทดสอบล็อกอิน (ควรไม่ต้องใส่รหัสผ่าน)
ssh user@192.168.1.10

# 5. (Client) ตั้งค่า ~/.ssh/config เพื่อใช้ชื่อย่อ
#    Host prod
#        HostName 192.168.1.10
#        User user
#        IdentityFile ~/.ssh/id_ed25519
ssh prod

# 6. (Server) ปิด password auth เมื่อแน่ใจว่า key ใช้ได้
#    /etc/ssh/sshd_config → PasswordAuthentication no
sudo systemctl reload ssh
```
