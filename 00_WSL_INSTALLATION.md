# คู่มือการติดตั้ง WSL (Windows Subsystem for Linux) และการเข้าใจคำสั่ง sudo

เอกสารสอนการติดตั้ง Linux (Ubuntu LTS) บน Windows 10/11 ผ่าน WSL เพื่อให้นักวิทยาศาสตร์ผู้ใช้ Windows สามารถรัน Linux ได้เนทีฟบนเครื่องตัวเองโดยไม่ต้องลง OS ใหม่ พร้อมอธิบายหลักการทำงานของสิทธิ์ root และคำสั่ง `sudo`

---

## ⚡ คำสั่งที่ต้องรู้ก่อน / ควรรู้ก่อน (WSL & Sudo Must-Know)

คำสั่งสำคัญใน Windows PowerShell และ Linux Terminal ที่ต้องรู้ก่อนเริ่มต้น:

```powershell
# 1. ติดตั้ง WSL พร้อม Ubuntu LTS ตัวล่าสุด (รันบน Windows PowerShell แบบ Administrator)
wsl --install

# 2. ตรวจสอบรายการ Linux Distribution ที่ติดตั้งอยู่บนเครื่อง
wsl --list --verbose

# 3. เปิดใช้งาน Ubuntu Linux ผ่าน PowerShell
wsl -d Ubuntu

# 4. ปิดการทำงานของ WSL เมื่อต้องการคืนทรัพยากร RAM/CPU ให้ Windows
wsl --shutdown
```

```bash
# 5. รันคำสั่งด้วยสิทธิ์ผู้ดูแลระบบ (Root) บน Linux Terminal (ระบบจะถามรหัสผ่าน)
sudo apt update

# 6. ตรวจสอบชื่อผู้ใช้งานปัจจุบันที่คุณกำลังใช้อยู่
whoami

# 7. ตรวจสอบว่าผู้ใช้งานปัจจุบันมีสิทธิ์ sudo (Superuser) หรือไม่
sudo -v
```

---

## 🎯 สถานการณ์ตัวอย่าง: นักวิทยาศาสตร์ต้องการรัน Linux บน Windows Laptop

> **Scenario:** คุณเป็นนักวิทยาศาสตร์ที่มีเครื่องโน้ตบุ๊กทำงานเป็น Windows 10 หรือ 11 และต้องการใช้เครื่องมือสายพัฒนาหรือ AI Agents (เช่น Claude Code) บนสภาพแวดล้อม Linux โดยไม่อยากฟอร์แมตเครื่องหรือทำ Dual Boot
> 
> **ทางออก:** ติดตั้ง **WSL 2 (Windows Subsystem for Linux)** ซึ่งจะจำลอง Ubuntu LTS ขึ้นมาทำงานขนานไปกับ Windows ได้อย่างรวดเร็วและใช้ไฟล์ร่วมกันได้ทันที

---

## 1. ขั้นตอนการติดตั้ง WSL และ Ubuntu LTS บน Windows

### 🎯 สิ่งที่ต้องการเรียนรู้
- การใช้คำสั่ง `wsl --install` เพื่อติดตั้ง Ubuntu LTS บน Windows 10/11

### 🛠️ ขั้นตอนการติดตั้ง (ทำบน Windows PowerShell)

1. คลิกขวาที่ปุ่ม **Start** บน Windows → เลือก **Terminal (Admin)** หรือ **PowerShell (Run as Administrator)**
2. คัดลอกและพิมพ์คำสั่งด้านล่างนี้ใน PowerShell:

```powershell
# ติดตั้ง WSL พร้อมดาวน์โหลด Ubuntu LTS อัตโนมัติ (Default Distribution ของ Windows)
wsl --install
```

3. เมื่อระบบติดตั้งเสร็จ ให้ **Restart คอมพิวเตอร์ 1 ครั้ง**
4. หลังจากเปิดเครื่องใหม่ หน้าต่างเทอร์มินัล Ubuntu จะเด้งขึ้นมาให้ตั้งค่า:
   - **Enter new UNIX username**: ตั้งชื่อผู้ใช้ภาษาอังกฤษ (เช่น `scientist`)
   - **New password**: ตั้งรหัสผ่านสำหรับเข้าใช้งาน Linux (ขณะพิมพ์รหัสผ่าน จะไม่มีตัวอักษรหรือดอกจันแสดงขึ้นมา ให้พิมพ์แล้วกด Enter ได้เลย)

---

## 2. ทำความเข้าใจคำสั่ง `sudo` และสิทธิ์ Root บน Linux

### 🎯 สิ่งที่ต้องการเรียนรู้
- คำสั่ง `sudo` คืออะไร และทำไมต้องใช้ในการติดตั้งซอฟต์แวร์

### 💡 `sudo` คืออะไร? (เปรียบเทียบกับ Windows)
- `sudo` ย่อมาจาก **"Superuser Do"** 
- ทำหน้าที่เปรียบเสมือนปุ่ม **"Run as Administrator"** ใน Windows
- ในระบบ Linux ผู้ใช้ปกติจะไม่มีสิทธิ์แก้ไขไฟล์ระบบหรือติดตั้งโปรแกรมเพื่อความปลอดภัย การเติม `sudo` นำหน้าคำสั่งเป็นการขออนุญาตทำงานในฐานะผู้ดูแลระบบสูงสุด (Root User)

### ⚠️ พฤติกรรมสำคัญเมื่อพิมพ์รหัสผ่าน `sudo` บน Linux Terminal
- เมื่อคุณพิมพ์คำสั่งที่ขึ้นต้นด้วย `sudo` ระบบจะถาม `[sudo] password for username:`
- **ขณะที่คุณพิมพ์รหัสผ่าน จะไม่มีตัวอักษรใดๆ หรือดอกจัน `***` ปรากฏขึ้นบนหน้าจอเลย** (เป็นฟีเจอร์ความปลอดภัยของ Linux ไม่ใช่เครื่องค้าง!)
- ให้พิมพ์รหัสผ่านให้ถูกต้องแล้วกดปุ่ม **Enter** ได้ทันที

### 🧪 ตัวอย่างการใช้งาน `sudo` ที่ถูกต้อง

```bash
# 1. การอัปเดตรายการแพ็กเกจระบบ (ต้องใช้ sudo เพราะเป็นการจัดการไฟล์ระบบ)
sudo apt update

# 2. การติดตั้งโปรแกรมใหม่ เช่น git (ต้องใช้ sudo)
sudo apt install -y git

# 3. การอัปเดตซอฟต์แวร์ทั้งหมดในเครื่อง (ต้องใช้ sudo)
sudo apt upgrade -y

# 4. สิ่งที่ไม่ต้องใช้ sudo (คำสั่งงานทั่วไปในพื้นที่ User ไม่ต้องใช้ sudo เด็ดขาด!)
# สร้างโฟลเดอร์ใน Home directory (ไม่ต้องใช้ sudo)
mkdir -p ~/my-research

# 5. สร้างไฟล์ข้อความธรรมดา (ไม่ต้องใช้ sudo)
touch ~/my-research/notes.txt

# 6. รันสคริปต์ Python หรือ Claude Code (ไม่ต้องใช้ sudo)
python3 --version
```

> 📌 **ข้อควรระวัง:** ห้ามใช้ `sudo` พร่ำเพรื่อในการสร้างไฟล์งานหรือรันโค้ด Vibe Coding ทั่วไป เพราะจะทำให้ไฟล์นั้นกลายเป็นของ `root` และผู้ใช้ปกติจะไม่สามารถแก้ไขหรือลบไฟล์นั้นได้!

---

## 3. การเข้าถึงไฟล์ระหว่าง Windows และ WSL (Ubuntu)

### 🎯 สิ่งที่ต้องการเรียนรู้
- วิธีเปิดดูไฟล์ของ Linux จาก Windows Explorer และการเข้าถึงไฟล์ Windows จาก Linux Terminal

```bash
# 1. เปิด Windows File Explorer เข้ามาดูโฟลเดอร์ปัจจุบันของ Linux (รันคำสั่งนี้ใน WSL Terminal)
explorer.exe .

# 2. เข้าถึงไดรฟ์ C: ของ Windows จากใน Linux Terminal (ไดรฟ์ของ Windows จะถูก Mount ไว้ที่ /mnt/c/)
cd /mnt/c/Users/

# 3. กลับไปยัง Home Directory ของ Linux (~/ หรือ /home/username/)
cd ~
```
