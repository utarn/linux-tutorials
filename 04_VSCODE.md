# คู่มือ VS Code + Remote - SSH สำหรับ Vibe Coding และนักวิทยาศาสตร์

เอกสารสอนการใช้ Visual Studio Code บน Windows เชื่อมต่อไปยัง Linux Server ผ่าน Remote - SSH เพื่อใช้งาน AI Agent (เช่น Claude Code) และแก้ไขโค้ดวิจัยเสมือนนั่งทำงานบน Linux Server โดยตรง

---

## ⚡ คำสั่งที่ต้องรู้ก่อน / ควรรู้ก่อน (VS Code & Remote Must-Know)

คำสั่งและขั้นตอนสำคัญที่ต้องรู้ก่อนใช้งาน VS Code Remote - SSH:

```bash
# 1. เปิด VS Code ในโฟลเดอร์ปัจจุบันบน Linux Server (เมื่อรันผ่าน Terminal)
code .

# 2. ตรวจสอบว่าคำสั่ง code พร้อมใช้งานในระบบ PATH หรือไม่
which code

# 3. ติดตั้ง Extension Remote - SSH ผ่าน CLI ของ VS Code
code --install-extension ms-vscode-remote.remote-ssh

# 4. ทดสอบการเชื่อมต่อ SSH ไปยัง Server ก่อนเปิดผ่าน VS Code
ssh user@server-ip
```

---

## 🎯 สถานการณ์ตัวอย่าง: นักวิทยาศาสตร์เขียนโค้ดวิจัยบน Windows แต่รันบน Linux GPU Server

> **Scenario:** คุณเป็นนักวิทยาศาสตร์ที่ชอบความสะดวกของหน้าจอแก้ไขโค้ดแบบ GUI บน Windows แต่ต้องการใช้ทรัพยากรดิสก์, CPU, GPU และเครื่องมือ AI บน Linux Server
> 
> **ทางออก:** ใช้ VS Code บน Windows ร่วมกับ Extension **Remote - SSH** ของ Microsoft เพื่อเปิดโฟลเดอร์บน Linux Server มาแก้ไข แก้ไฟล์ เซฟไฟล์ และเปิด Terminal รัน Claude Code บน Linux ได้จากหน้าต่าง VS Code บน Windows ทันที!

---

## 1. การติดตั้ง VS Code และ Extension Remote - SSH

### 🎯 สิ่งที่ต้องการเรียนรู้
- ขั้นตอนการเตรียมเครื่อง Windows ให้พร้อมสำหรับ Remote - SSH

1. ดาวน์โหลดและติดตั้ง **VS Code** บน Windows จากเว็บ [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. เปิดโปรแกรม VS Code
3. กดปุ่ม `Ctrl + Shift + X` เพื่อเปิดเมนู **Extensions**
4. ค้นหาคำว่า **Remote - SSH** (โดย Microsoft) แล้วคลิก **Install**

---

## 2. ขั้นตอนการเชื่อมต่อ Linux Server จาก VS Code บน Windows

### 🎯 สิ่งที่ต้องการเรียนรู้
- การสั่งให้ VS Code เชื่อมต่อไปยัง Linux Server ผ่าน SSH

1. กดปุ่ม `F1` หรือ `Ctrl + Shift + P` ใน VS Code เพื่อเปิด Command Palette
2. พิมพ์คำสั่ง `Remote-SSH: Connect to Host...` แล้วกด Enter
3. กรอกคำสั่งเชื่อมต่อในรูปแบบ: `user@server-ip` (หรือเลือกชื่อ Host จาก `~/.ssh/config`)
4. เลือกระบบปฏิบัติการปลายทางเป็น **Linux**
5. เมื่อเชื่อมต่อสำเร็จ มุมซ้ายล่างของ VS Code จะขึ้นแถบสีเขียวแสดงข้อความ `SSH: server-ip`

---

## 3. การเปิด Remote Terminal และรัน Claude Code / tmux ใน VS Code

### 🎯 สิ่งที่ต้องการเรียนรู้
- การเปิด Integrated Terminal ใน VS Code ซึ่งเป็น Terminal ของ Linux Server โดยตรง

```bash
# 1. ในหน้าต่าง VS Code ให้กดปุ่ม Ctrl + ~ (ปุ่มตัวหนอน) เพื่อเปิด Integrated Terminal

# 2. ย้ายไปยังโฟลเดอร์โปรเจกต์งานวิจัยของคุณบน Linux Server
cd ~/vibe-projects/research-data

# 3. เปิด tmux เซสชันเพื่อรันงานแบบไม่หลุดเมื่อปิด VS Code
tmux new -s vscode-vibe

# 4. สั่งรัน Claude Code หรือ CLI AI tools บน Linux Server จากภายใน VS Code ได้ทันที!
# (ตอนนี้คุณสามารถใช้ AI Vibe Coding ได้เต็มประสิทธิภาพบน Linux Server แล้ว)
```

---

## 4. เคล็ดลับการตั้งค่า VS Code สำหรับ Vibe Coding

- **Auto Save**: ไปที่ `File` → `Auto Save` เพื่อให้ VS Code บันทึกไฟล์ไปยัง Linux Server อัตโนมัติทุกครั้งที่แก้ไข
- **Terminal Font & Colors**: สามารถเปิดปรับแต่งธีมสีและชนิดฟอนต์ให้สบายตาสำหรับการอ่าน Output จาก AI Agent
