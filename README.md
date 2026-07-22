# Linux Tutorials for Vibe Coding & Scientists

คู่มือและคำสั่ง Linux พื้นฐาน การตั้งค่า SSH, SCP, SFTP, VS Code Remote และ `tmux` สำหรับนักวิทยาศาสตร์/สายงานวิจัยที่ใช้ Windows มาทั้งชีวิต แล้วย้ายมาเรียนรู้ Linux เพื่อพัฒนาซอฟต์แวร์ด้วยแนวทาง **Vibe Coding** (ใช้งานร่วมกับ CLI AI Agents เช่น Claude Code)

---

## 📚 ลำดับขั้นตอนการเรียนรู้เอกสาร (Recommended Learning Order)

กรุณาศึกษาเอกสารตามลำดับตัวเลขนำหน้าไฟล์ดังนี้:

1. [**01_LINUX.md**](01_LINUX.md) — **คู่มือคำสั่ง Linux พื้นฐาน**
   - คำสั่งที่ต้องรู้ก่อน (Survival Kit)
   - การจัดการไฟล์/โฟลเดอร์ การมอนิเตอร์โปรเซส การดาวน์โหลดข้อมูล และการตั้งค่า Ubuntu
2. [**02_PUBLICKEY.md**](02_PUBLICKEY.md) — **คู่มือ SSH Public Key Authentication**
   - การสร้าง SSH Key บน Windows/Linux และตั้งค่าล็อกอินโดยไม่ต้องพิมพ์รหัสผ่าน
3. [**03_SSH_FILESYSTEM.md**](03_SSH_FILESYSTEM.md) — **คู่มือการโอนย้ายไฟล์ SCP, SFTP & rsync**
   - การรับส่งชุดข้อมูลวิจัย (.csv, .json, dataset) ระหว่าง Windows และ Linux Server
4. [**04_VSCODE.md**](04_VSCODE.md) — **คู่มือ VS Code + Remote - SSH**
   - การเชื่อมต่อจาก VS Code บน Windows ไปยัง Linux Server เพื่อรัน Vibe Coding
5. [**05_TMUX.md**](05_TMUX.md) — **คู่มือ tmux และการตั้งค่าสำหรับ Vibe Coding**
   - การติดตั้ง `tmux` บน Ubuntu Linux
   - การตั้งค่า `~/.tmux.conf` สำหรับเมาส์สโครล (Mouse Scroll) อ่านคำตอบจาก Claude Code ลื่นไหล ไม่โดนตัดข้อความ

---

## 🎯 จุดเด่นของเอกสารชุดนี้

- **เรียงลำดับการเรียนรู้**: มีตัวเลข `01_` ถึง `05_` กำหนดลำดับไฟล์เพื่อให้เรียนรู้ได้อย่างเป็นขั้นตอน
- **โครงสร้างอ่านง่าย**: สรุป **คำสั่งที่ต้องรู้ก่อน / ควรรู้ก่อน** ไว้ที่ส่วนบนสุดของทุกไฟล์
- **พร้อมคัดลอกรัน**: บล็อกคำสั่งเขียนสลับกับ `# comment` อธิบายทีละบรรทัด สามารถ Copy ไปวางลงใน Linux Terminal ได้ทันทีไม่มี syntax error
- **บริบทเหมาะกับนักวิทยาศาสตร์**: สร้างสถานการณ์เปรียบเทียบจากมุมมองของผู้ที่คุ้นเคยกับ Windows แล้วย้ายมา Linux Server
- **ซัพพอร์ต Vibe Coding & Claude Code**: พร้อมคอนฟิก `tmux` พิเศษให้เลื่อนสโครลดู Log หรือคำตอบยาวๆ จาก AI Agent ได้ไม่มีสะดุด
