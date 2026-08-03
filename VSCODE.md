# VS Code — การตั้งค่าเบื้องต้น

VS Code คือโค้ดเมดิเตอร์ที่คล่องค่ะ เริ่มจากการติดตั้งแล้วตั้งค่า Remote - SSH

## การติดตั้ง VS Code

- **Windows / macOS / Linux**: ดาวน์โหลดจาก [code.visualstudio.com](https://code.visualstudio.com/)
- หรือใช้ package manager:

**macOS (Homebrew):**
```bash
brew install --cask visual-studio-code
```

**Ubuntu:**
```bash
sudo apt update && sudo apt install -y wget gpg
wget -qO-https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo dpkg -i packages.microsoft.gpg
sudo apt update && sudo apt install -y code
rm packages.microsoft.gpg
```

**Windows (winget):**
```powershell
winget install --id Microsoft.VisualStudioCode -e
```

## การตั้งค่า Remote - SSH

Remote - SSH ช่วยให้คุณเชื่อมต่อและทำงานกับเซิร์ฟเวอร์ระยะไกลโดยตรงจาก VS Code เปิดใช้งานได้โดย:

1. เปิด VS Code
2. ไปที่ Extensions (`Ctrl+Shift+X` หรือ `Cmd+Shift+X`)
3. ค้นหา **Remote - SSH** และคลิก **Install**

### เพิ่ม SSH Host ใหม่

1. คลิกไอคอน Remote (มุมซ้ายล่าง)`>` หรือกด `F1` แล้วพิมพ์ `Remote-SSH: Add new SSH Host...`
2. ใส่ hostname ในรูปแบบ `user@hostname`  ตัวอย่างเช่น `ubuntu@203.0.113.10`
3. เลือกไฟล์ config ที่ `${HOME}/.ssh/config`
4. เปิดไฟล์ config ที่เปิดขึ้น
5. ตั้งชื่อเล่น (nickname) **ภาษาไทย** สำหรับ SSH host นั้น เช่น:

```
Host เซิร์ฟเวอร์หลัก
    HostName 203.0.113.10
    User ubuntu
    Port 22
```

> **เคล็ดลับ**: ใช้ชื่อภาษาไทยเป็นชื่อเล่นทำให้จำง่าย แต่ตรวจสอบว่าชื่อไม่มีปัญหากับเครื่องมือบางตัวที่ไม่รองรับ UTF-8

### เชื่อมต่อ

1. คลิกไอคอน Remote ทางซ้ายล่าง หรือกด `F1` แล้วเลือก **Remote-SSH: Connect to Host**
2. เลือกชื่อที่คุณตั้งไว้ (เช่น `เซิร์ฟเวอร์หลัก`)
3. พิมพ์รหัสผ่าน หรือใช้ key ที่ตั้งค่าไว้
4. เมื่อเชื่อมต่อสำเร็จ VS Code จะเปิดหน้าต่างใหม่พร้อมบรรยากาศยบนเซิร์ฟเวอร์

## ส่วนขยายที่แนะนำ

| ส่วนขยาย | วัตถุประสงค์ |
|---|---|
| Prettier | จัดรูปแบบโค้ดอัตโนมัติ |
| ESLint | ตรวจจับข้อผิดพลาด JavaScript/TypeScript |
| GitLens | ปรับปรุงมุมมอง Git |
| Bracket Pair Colorizer | สีวงเล็บสีสัน |
| Auto Rename Tag | เปลี่ยนชื่อ tag HTML อัตโนมัติ |
