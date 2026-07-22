# คู่มือ SSH Public Key Authentication สำหรับ Vibe Coding และนักวิทยาศาสตร์

เอกสารสอนการสร้าง SSH Key ทั้งบน Windows และ Linux เพื่อเข้าถึง Linux GPU Server สำหรับรัน Vibe Coding โดยไม่ต้องกรอกรหัสผ่านทุกครั้ง

---

## ⚡ คำสั่งที่ต้องรู้ก่อน / ควรรู้ก่อน (SSH Key Must-Know)

ชุดคำสั่งสำคัญสำหรับการสร้างและจัดการ SSH Key ที่ต้องรู้ก่อนใช้งาน:

```bash
# 1. สร้าง SSH Key คู่ใหม่ (Ed25519) บนเครื่อง Local
ssh-keygen -t ed25519 -C "scientist@research.org"

# 2. ดูเนื้อหา Public Key เพื่อนำไปวางบน Server (ฝั่ง Client)
cat ~/.ssh/id_ed25519.pub

# 3. ส่ง Public Key ไปติดตั้งบน Linux Server อัตโนมัติ (จาก Linux/macOS Client)
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@server-ip

# 4. ตั้งค่าสิทธิ์โฟลเดอร์ .ssh บน Server ให้ปลอดภัย (ฝั่ง Server)
chmod 700 ~/.ssh

# 5. ตั้งค่าสิทธิ์ไฟล์ authorized_keys บน Server ให้ปลอดภัย (ฝั่ง Server)
chmod 600 ~/.ssh/authorized_keys

# 6. ล็อกอินเข้า Linux Server ด้วย SSH Key โดยไม่ต้องพิมพ์รหัสผ่าน
ssh user@server-ip
```

---

## 🎯 สถานการณ์ตัวอย่าง: นักวิทยาศาสตร์ต่อ SSH จาก Windows Laptop ไปยัง Linux Server

> **Scenario:** คุณเป็นนักวิทยาศาสตร์ที่ทำงานบน Windows Laptop และต้องเชื่อมต่อแบบ Remote ไปยัง Linux GPU Server เพื่อใช้ Claude Code รันโมเดลประมวลผลข้อมูล
> 
> **ปัญหา:** ถ้าใช้รหัสผ่านปกติ ทุกครั้งที่เชื่อมต่อหรือใช้ Tool ต่างๆ จะต้องคอยพิมพ์รหัสผ่านตลอดเวลา และเสี่ยงต่อการถูกเดารหัสผ่าน (Brute Force)
> 
> **ทางออก:** ใช้ SSH Public Key Authentication ซึ่งปลอดภัยกว่า รวดเร็วกว่า และช่วยให้เครื่องมือ Vibe Coding (เช่น VS Code Remote - SSH หรือ Claude Code) เชื่อมต่อได้อย่างไม่มีสะดุด

---

## 1. แนวคิดคู่กุญแจ SSH (Public & Private Key Concept)

```
[ เครื่อง Windows Laptop (Client) ]                [ Linux Server (Remote) ]
   ~/.ssh/id_ed25519 (Private Key)  ─── ล็อกอิน ───►  ~/.ssh/authorized_keys (Public Key)
   (เก็บลับเฉพาะเครื่องเรา ห้ามแจก)                    (วาง Public Key ของเราไว้ที่นี่)
```

---

## 2. ขั้นตอนการสร้าง SSH Key บน Windows (PowerShell / Command Prompt)

### 🎯 สิ่งที่ต้องการเรียนรู้
- วิธีการสร้าง SSH Key บน Windows โดยใช้คำสั่ง `ssh-keygen` ใน PowerShell

```powershell
# 1. เปิด PowerShell บน Windows แล้วรันคำสั่งสร้าง SSH Key ชนิด ed25519
ssh-keygen -t ed25519 -C "scientist-windows-laptop"

# 2. เมื่อระบบถามตำแหน่งไฟล์ กด Enter เพื่อใช้ค่าเริ่มต้น (C:\Users\username\.ssh\id_ed25519)

# 3. เมื่อระบบถาม Passphrase สามารถกด Enter ข้ามได้หากต้องการความสะดวกในการรัน Vibe Coding

# 4. ตรวจสอบดูไฟล์ Public Key ที่สร้างเสร็จแล้วบน Windows PowerShell
Get-Content ~\.ssh\id_ed25519.pub
```

---

## 3. ขั้นตอนการนำ Public Key ไปวางบน Linux Server

### 🎯 สิ่งที่ต้องการเรียนรู้
- วิธีคัดลอก Public Key ไปวางในไฟล์ `~/.ssh/authorized_keys` ของ Linux Server

```bash
# 1. ล็อกอินเข้า Linux Server (ครั้งนี้ยังต้องพิมพ์รหัสผ่านปกติ)
ssh user@server-ip

# 2. สร้างโฟลเดอร์ .ssh บน Linux Server (หากยังไม่มี)
mkdir -p ~/.ssh

# 3. กำหนดสิทธิ์โฟลเดอร์ .ssh ให้เป็น 700 (เฉพาะเจ้าของเข้าถึงได้)
chmod 700 ~/.ssh

# 4. เขียน Public Key ของคุณต่อท้ายลงในไฟล์ authorized_keys บน Server
# (เปลี่ยนข้อความ 'ssh-ed25519 AAAAC3NzaC...' เป็น Public Key จริงของคุณ)
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... scientist-windows-laptop" >> ~/.ssh/authorized_keys

# 5. กำหนดสิทธิ์ไฟล์ authorized_keys ให้เป็น 600 (เฉพาะเจ้าของอ่าน/เขียนได้)
chmod 600 ~/.ssh/authorized_keys

# 6. ออกจาก Linux Server
exit

# 7. ทดสอบล็อกอินใหม่อีกครั้ง คราวนี้ระบบจะไม่ถามรหัสผ่านแล้ว!
ssh user@server-ip
```

---

## 4. การตั้งค่า `~/.ssh/config` เพื่อความสะดวกในการเชื่อมต่อ (Client Side)

### 🎯 สิ่งที่ต้องการเรียนรู้
- ตั้งชื่อย่อให้ Server เช่น `ssh gpuserver` แทนการพิมพ์ IP และ Username ยาวๆ ทุกครั้ง

```bash
# 1. สร้าง/แก้ไขไฟล์ ~/.ssh/config บนเครื่อง Client
cat << 'EOF' >> ~/.ssh/config
# ตั้งค่าโปรไฟล์เชื่อมต่อ Linux GPU Server สำหรับงานวิจัย
Host gpuserver
    HostName 192.168.1.100
    User ubuntu
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60
EOF

# 2. ตั้งสิทธิ์ไฟล์ config ให้ปลอดภัย
chmod 600 ~/.ssh/config

# 3. ตอนนี้คุณสามารถสั่ง SSH เข้า Server ได้ง่ายๆ ผ่านชื่อย่อ:
ssh gpuserver
```
