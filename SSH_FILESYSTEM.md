# คู่มือการโอนย้ายไฟล์ SCP, SFTP และ rsync สำหรับ Vibe Coding และนักวิทยาศาสตร์

เอกสารสอนการรับส่งไฟล์ข้อมูลวิจัย (.csv, .json, dataset) ระหว่างเครื่อง Windows กับ Linux Server ผ่านบรรทัดคำสั่งและโปรแกรมกราฟิก (FileZilla)

---

## ⚡ คำสั่งที่ต้องรู้ก่อน / ควรรู้ก่อน (File Transfer Must-Know)

คำสั่งโอนย้ายไฟล์สำคัญที่ต้องรู้ก่อนเริ่มต้นใช้งาน:

```bash
# 1. อัปโหลดไฟล์จากเครื่อง Local ไปยัง Linux Server ผ่าน scp
scp dataset.csv user@server-ip:/home/user/data/

# 2. ดาวน์โหลดไฟล์ผลลัพธ์จาก Linux Server กลับมาเครื่อง Local
scp user@server-ip:/home/user/results/report.pdf ./

# 3. อัปโหลดทั้งโฟลเดอร์ไปยัง Linux Server
scp -r ./research_project user@server-ip:/home/user/

# 4. ซิงค์ไฟล์ด้วย rsync (ส่งเฉพาะไฟล์ที่เปลี่ยนแปลง ประหยัดเวลาสำหรับไฟล์ใหญ่)
rsync -avz ./data_folder/ user@server-ip:/home/user/data_folder/

# 5. ซิงค์ไฟล์จาก Server กลับมายังเครื่อง Local พร้อมแสดงความคืบหน้า (Progress)
rsync -avz --progress user@server-ip:/home/user/output/ ./output/
```

---

## 🎯 สถานการณ์ตัวอย่าง: การส่งไฟล์ข้อมูลวิจัยระหว่าง Windows กับ Linux Server

> **Scenario:** คุณเป็นนักวิทยาศาสตร์ที่มีไฟล์ข้อมูลดิบ (Raw CSV Dataset) อยู่บนเครื่อง Windows Laptop และต้องการส่งไฟล์ขึ้นไปประมวลผลบน Linux GPU Server รวมถึงการดึงรูปภาพกราฟผลลัพธ์ที่รันเสร็จแล้วกลับมาดูบน Windows

---

## 1. การใช้คำสั่ง `scp` ส่งและรับไฟล์ข้อมูล

### 🎯 สิ่งที่ต้องการเรียนรู้
- วิธีคัดลอกไฟล์เดี่ยวและโฟลเดอร์ระหว่างเครื่อง Local และ Remote Server

```bash
# 1. อัปโหลดไฟล์ dataset.csv จากโฟลเดอร์ปัจจุบันไปไว้ที่ /tmp/ บน Linux Server
scp dataset.csv user@192.168.1.100:/tmp/

# 2. อัปโหลดทั้งโฟลเดอร์ raw_experiments ไปไว้ที่ Home directory ของ Server
scp -r ./raw_experiments user@192.168.1.100:~/

# 3. ดาวน์โหลดไฟล์ผลการวิเคราะห์ analysis_result.json จาก Server ลงมาโฟลเดอร์ปัจจุบัน
scp user@192.168.1.100:~/analysis_result.json ./

# 4. ดาวน์โหลดโฟลเดอร์รูปภาพกราฟผลลัพธ์ plots กลับมาไว้ที่เครื่อง Local
scp -r user@192.168.1.100:~/plots ./
```

---

## 2. การใช้ `rsync` ซิงค์ชุดข้อมูลขนาดใหญ่ (แนะนำสำหรับนักวิทยาศาสตร์)

### 🎯 สิ่งที่ต้องการเรียนรู้
- การใช้ `rsync` ส่งข้อมูลอย่างมีประสิทธิภาพ (หากเน็ตหลุด สามารถรันต่อจากเดิมได้ไม่ต้องเริ่มใหม่)

```bash
# 1. ซิงค์โฟลเดอร์ข้อมูลวิจัยขึ้น Server (a=archive, v=verbose, z=compress บีบอัดระหว่างส่ง)
rsync -avz ./large_dataset/ user@192.168.1.100:~/large_dataset/

# 2. ซิงค์ข้อมูลพร้อมแสดงเกจความคืบหน้าการส่ง (Progress Bar)
rsync -avz --progress ./model_weights.pt user@192.168.1.100:~/models/

# 3. ซิงค์ข้อมูลผลลัพธ์กลับมาเครื่อง Local โดยลบไฟล์ปลายทางที่ต้นทางลบไปแล้วออกด้วย (--delete)
rsync -avz --delete user@192.168.1.100:~/results/ ./results/
```

---

## 3. การโอนไฟล์ผ่าน GUI ด้วย FileZilla (SFTP) สำหรับผู้เริ่มต้นใช้งาน Windows

### 🎯 สิ่งที่ต้องการเรียนรู้
- การใช้งานโปรแกรม FileZilla เชื่อมต่อผ่านโปรโตคอล SFTP (พอร์ต 22) โดยใช้ SSH Key

### 🛠️ ขั้นตอนการตั้งค่า FileZilla บน Windows
1. เปิดโปรแกรม **FileZilla**
2. ไปที่ menu **Edit** → **Settings** → **Connection** → **SFTP**
3. คลิก **Add keyfile...** แล้วเลือกไฟล์ Private Key (`id_ed25519` หรือ `id_ed25519.ppk`)
4. เปิด **File** → **Site Manager** แล้วตั้งค่า:
   - **Protocol**: `SFTP - SSH File Transfer Protocol`
   - **Host**: IP Address ของ Linux Server (เช่น `192.168.1.100`)
   - **Logon Type**: `Key file` หรือ `Normal`
   - **User**: Username บน Linux Server
5. คลิก **Connect** เพื่อลากวางไฟล์ระหว่าง Windows และ Linux ได้สะดวกสไตล์ Windows Explorer!
