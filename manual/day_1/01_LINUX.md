# คู่มือคำสั่ง Linux พื้นฐานสำหรับ Vibe Coding และนักวิทยาศาสตร์

เอกสารรวบรวมคำสั่ง Linux สำหรับผู้ที่ใช้งาน Windows มาทั้งชีวิต แล้วย้ายมาเรียนรู้ Linux เพื่อพัฒนาโปรแกรมแบบ Vibe Coding (ใช้งานร่วมกับ CLI AI Agents เช่น Claude Code)

---

## ⚡ คำสั่งที่ต้องรู้ก่อน / ควรรู้ก่อน (Linux Essential Cheatsheet)

คำสั่งพื้นฐานระดับวิกฤตที่ต้องรู้ก่อนเริ่มต้นใช้งาน Linux สามารถคัดลอกบล็อกคำสั่งด้านล่างนี้ไปวางลงใน Linux Terminal ได้ทันทีทุกบรรทัด:

```bash
# 1. ดูตำแหน่งไดเรกทอรีปัจจุบันที่คุณอยู่ (เทียบเท่าการดูแถบที่อยู่ C:\Users\... ใน Windows)
pwd

# 2. แสดงรายการไฟล์และโฟลเดอร์ทั้งหมดแบบละเอียด รวมถึงไฟล์ซ่อน (Dotfiles)
ls -la

# 3. สร้างโฟลเดอร์สำหรับเก็บโปรเจกต์งานวิจัยและโค้ด Vibe Coding
mkdir -p ~/vibe-projects/research-data

# 4. ย้ายตำแหน่งเข้าไปในโฟลเดอร์งานวิจัยที่เพิ่งสร้าง
cd ~/vibe-projects/research-data

# 5. สร้างไฟล์ทดสอบข้อความสำหรับบันทึกโน้ต
touch experiment_note.txt

# 6. เขียนข้อความลงในไฟล์ทดสอบ (ส่งผลให้เนื้อหาถูกบันทึกทับไฟล์)
echo "Scientific Data Processing with Linux & Vibe Coding" > experiment_note.txt

# 7. อ่านเนื้อหาในไฟล์ข้อความออกมาแสดงผลบนเทอร์มินัล
cat experiment_note.txt

# 8. ตรวจสอบพื้นที่ดิสก์ที่เหลืออยู่บนระบบแบบหน่วยที่อ่านง่าย (GB, MB)
df -h

# 9. ตรวจสอบหน่วยความจำ RAM ที่กำลังถูกใช้งานอยู่บนเครื่อง
free -h

# 10. ล้างหน้าจอเทอร์มินัลให้สะอาดเพื่อเริ่มทำงานใหม่
clear
```

---

## 🎯 สถานการณ์ตัวอย่าง: นักวิทยาศาสตร์ย้ายจาก Windows มาใช้ Linux ทำ Vibe Coding

> **Scenario:** คุณเป็นนักวิทยาศาสตร์ที่เคยจัดการไฟล์ข้อมูลงานวิจัย (.csv, .json) ผ่าน Windows File Explorer และเปิดโปรแกรมสเปรดชีต วันนี้คุณต้องย้ายมาใช้ Linux Server ที่มี GPU เพื่อรันการประมวลผลข้อมูลและใช้ AI Agent (เช่น Claude Code) ในการช่วยสร้างสคริปต์วิเคราะห์ข้อมูลแบบ Vibe Coding

---

## 1. การจัดการไฟล์และโฟลเดอร์ (File & Directory Management)

### 🎯 สิ่งที่ต้องการเรียนรู้
- การดูตำแหน่ง การสร้าง ย้าย ลบ และอ่านเนื้อหาไฟล์ข้อมูลวิจัย
- การตั้งสิทธิ์ (Permissions) เพื่อให้สคริปต์รันได้อย่างถูกต้อง

```bash
# 1. ดูตำแหน่งปัจจุบันที่คุณกำลังทำงานอยู่
pwd

# 2. สร้างโฟลเดอร์ซ้อนกันสำหรับจัดเก็บข้อมูลดิบ (raw) และข้อมูลที่ประมวลผลแล้ว (processed)
mkdir -p ~/research/raw_data ~/research/processed_data

# 3. ย้ายเข้าไปในโฟลเดอร์ข้อมูลดิบ
cd ~/research/raw_data

# 4. จำลองการสร้างไฟล์ข้อมูลผลการทดลองแบบ CSV
echo "id,sample_name,value" > sample_01.csv
echo "1,protein_A,98.5" >> sample_01.csv
echo "2,protein_B,104.2" >> sample_01.csv

# 5. ดูเนื้อหาในไฟล์ CSV ที่เพิ่งสร้างขึ้นมา
cat sample_01.csv

# 6. คัดลอกไฟล์ข้อมูลดิบไปยังโฟลเดอร์สำรองข้อมูล
cp sample_01.csv sample_01_backup.csv

# 7. เปลี่ยนชื่อไฟล์สำรองเพื่อความเป็นระเบียบ
mv sample_01_backup.csv sample_01_archive.csv

# 8. ดูเฉพาะ 2 บรรทัดแรกของไฟล์ข้อมูล (ดู Header ของ CSV)
head -n 2 sample_01.csv

# 9. นับจำนวนบรรทัดของไฟล์ข้อมูลวิจัย
wc -l sample_01.csv

# 10. ค้นหาคำว่า 'protein_A' ในไฟล์ CSV
grep "protein_A" sample_01.csv

# 11. ให้สิทธิ์การรัน (Execute) แก่ไฟล์สคริปต์ Python หรือ Bash
chmod +x sample_01.csv

# 12. ลบไฟล์สำรองเมื่อไม่ใช้งานแล้ว
rm sample_01_archive.csv
```

---

## 2. การจัดการโปรเซสและการมอนิเตอร์ (Process Monitoring & Management)

### 🎯 สิ่งที่ต้องการเรียนรู้
- ตรวจสอบทรัพยากรเครื่องขณะรันโมเดล AI หรือสคริปต์ประมวลผลข้อมูล
- การยกเลิกโปรเซสค้าง (Kill Process) เวลาสคริปต์ทำงานผิดพลาด

```bash
# 1. ดูรายการโปรเซสที่กำลังทำงานอยู่ทั้งหมดบนระบบแบบละเอียด
ps aux | head -n 15

# 2. ค้นหาโปรเซสของ Python ที่กำลังรันงานประมวลผลอยู่
ps aux | grep python

# 3. ดูการทำงานของ CPU และ RAM แบบเรียลไทม์ (กด q เพื่อออกจากหน้าจอ)
top

# 4. สร้างการรันงานเบื้องหลัง (Background Task) จำลองการประมวลผล 100 วินาที
sleep 100 &

# 5. ตรวจสอบรหัสโปรเซส (PID) ของงาน sleep ที่รันอยู่เบื้องหลัง
pgrep -f "sleep 100"

# 6. สั่งยุติโปรเซส sleep ที่รันอยู่เบื้องหลังอย่างปลอดภัยด้วย PID
kill $(pgrep -f "sleep 100")
```

---

## 3. การใช้งาน tmux และการตั้งค่าลื่นไหลสำหรับ Claude Code (Terminal Multiplexer)

### 🎯 สิ่งที่ต้องการเรียนรู้
- ติดตั้ง `tmux` บน Ubuntu Linux
- ตั้งค่า `~/.tmux.conf` ให้ใช้เมาส์สโครลเลื่อนดูหน้าจอ (Scroll) ย้อนหลังอ่านคำตอบ AI ได้อย่างลื่นไหล
- การรัน AI Agent ใน tmux เซสชัน ป้องกันเน็ตหลุดงานไม่หาย

### 🧪 ขั้นตอนการติดตั้งและใช้งาน (Run Commands)

```bash
# 1. อัปเดตรายการแพ็กเกจของ Ubuntu
sudo apt update

# 2. ติดตั้งโปรแกรม tmux ลงบนระบบ Ubuntu
sudo apt install -y tmux

# 3. เขียนคอนฟิกตั้งค่าเปิดใช้งานเมาส์สโครลและขยายประวัติย้อนหลังลงใน ~/.tmux.conf
cat << 'EOF' > ~/.tmux.conf
# เปิดใช้งานเมาส์ ให้สโครลเลื่อนหน้าจอและคลิกเลือก pane ได้
set -g mouse on
# ขยายประวัติย้อนหลังเป็น 50,000 บรรทัด สำหรับอ่าน Output ยาวๆ จาก Claude Code
set -g history-limit 50000
# ตั้งค่าสีให้รองรับ True Color (256-color)
set -g default-terminal "screen-256color"
set -as terminal-overrides ",xterm*:Tc"
# ลดเวลาหน่วงของปุ่ม Escape
set -s escape-time 10
EOF

# 4. โหลดคอนฟิก tmux ใหม่ทันที
tmux source ~/.tmux.conf 2>/dev/null || echo "คอนฟิกพร้อมใช้งานเมื่อเปิด tmux ครั้งต่อไป"

# 5. สร้างเซสชัน tmux ใหม่ชื่อ 'vibe-coding' สำหรับรัน Claude Code
tmux new -s vibe-coding

# 6. ทดลองออกจากเซสชันชั่วคราว (Detach) กดปุ่ม: Ctrl+b แล้วตามด้วย d

# 7. ดึงเซสชัน 'vibe-coding' กลับขึ้นมาทำงานต่อ (Attach)
tmux attach -t vibe-coding
```

### ⌨️ Tmux Keyboard Shortcuts ที่ใช้บ่อย

หลังจากติดตั้ง tmux และเปิดเซสชันแล้ว คำสั่งลัดต่อไปนี้ช่วยให้ทำงานได้เร็วขึ้น (กด `Ctrl+b` เป็นคำนำหน้า แล้วตามด้วยปุ่มอื่น):

| Shortcut | คำอธิบาย |
|---|---|
| `Ctrl+b` แล้ว `c` | สร้างหน้าต่าง (Window) ใหม่ |
| `Ctrl+b` แล้ว `,` | เปลี่ยนชื่อหน้าต่างปัจจุบัน |
| `Ctrl+b` แล้ว `p` / `n` | ไปหน้าต่างก่อนหน้า (Previous) / ถัดไป (Next) |
| `Ctrl+b` แล้ว `0`-`9` | ไปหน้าต่างตามหมายเลข |
| `Ctrl+b` แล้ว `w` | แสดงรายการหน้าต่างทั้งหมดให้เลือก |
| `Ctrl+b` แล้ว `%` | แยก Pane ออกแนวตั้ง (ซ้าย-ขวา) |
| `Ctrl+b` แล้ว `"` | แยก Pane ออกแนวนอน (บน-ล่าง) |
| `Ctrl+b` แล้ว `ลูกศร` | ย้ายระหว่าง Pane |
| `Ctrl+b` แล้ว `x` | ปิด Pane ปัจจุบัน (ยืนยันด้วย `y`) |
| `Ctrl+b` แล้ว `d` | Detach ออกจากเซสชัน (กลับมาทีหลังด้วย `tmux attach`) |
| `Ctrl+b` แล้ว `[` | เข้าโหมด Scroll/Copy — ใช้ลูกศร, `PageUp`, `PageDown` เพื่อเลื่อนดูประวัติ |
| `Ctrl+b` แล้ว `t` | แสดงนาฬิกาใน Pane |
| `Ctrl+b` แล้ว `?` | ดูรายการ Shortcuts ทั้งหมด (กด `q` เพื่อปิด) |
| `Ctrl+b` แล้ว `z` | ซูม Pane ปัจจุบันให้เต็มหน้าจอ (กดซ้ำเพื่อคืนค่า) |

> 💡 **เคล็ดลับ:** ถ้าลืม shortcut ให้กด `Ctrl+b` แล้ว `?` ตลอดเวลา — tmux จะแสดง cheat sheet ในตัว

---

## 4. เครือข่ายและการดาวน์โหลดข้อมูลวิจัย (Networking & Data Fetching)

### 🎯 สิ่งที่ต้องการเรียนรู้
- การดาวน์โหลดไฟล์ชุดข้อมูล (Dataset) จากอินเทอร์เน็ตผ่าน URL
- การตรวจสอบพอร์ตและการเชื่อมต่อเครือข่าย

```bash
# 1. สอบถาม IP Address ของเครื่อง Linux Server เพื่อเชื่อมต่อ
hostname -I

# 2. ทดสอบการเชื่อมต่อไปยังเซิร์ฟเวอร์ภายนอก (ส่ง ping 4 ครั้ง)
ping -c 4 google.com

# 3. ดาวน์โหลดไฟล์ตัวอย่างข้อมูลจาก URL มาเก็บไว้ในเครื่อง
curl -o sample_data.json https://jsonplaceholder.typicode.com/todos/1

# 4. อ่านเนื้อหาในไฟล์ JSON ที่เพิ่งดาวน์โหลดลงมา
cat sample_data.json

# 5. ตรวจสอบพอร์ตที่กำลังเปิดรอรับการเชื่อมต่ออยู่บนระบบ
ss -tulpn
```

---

## 5. การติดตั้งแพ็กเกจและการตั้งค่าสภาพแวดล้อม (Package Manager & Environment)

### 🎯 สิ่งที่ต้องการเรียนรู้
- การติดตั้งซอฟต์แวร์และเครื่องมือสำหรับนักพัฒนาบน Ubuntu (`apt`)
- การตั้งค่าตัวแปรสภาพแวดล้อม (Environment Variables) เช่น API Keys

```bash
# 1. อัปเดตรายการแพ็กเกจระบบให้เป็นเวอร์ชันล่าสุด
sudo apt update

# 2. ติดตั้งเครื่องมือพื้นฐาน เช่น git, curl, python3, pip, unzip
sudo apt install -y git curl python3 python3-pip unzip

# 3. กำหนดค่าตัวแปรสภาพแวดล้อมสำหรับรัน Vibe Coding (ตัวอย่างการตั้งค่า API Key)
export ANTHROPIC_API_KEY="your-api-key-here"

# 4. ตรวจสอบว่าตัวแปรสภาพแวดล้อมถูกตั้งค่าเรียบร้อยแล้ว
echo $ANTHROPIC_API_KEY

# 5. แสดงเส้นทางโฟลเดอร์ของคำสั่ง python3 บนระบบ
which python3
```

---

## 6. ตัวอย่างการปฏิบัติจริง: ติดตั้ง Nginx และ Certbot สำหรับ Web Services

### 🎯 สิ่งที่ต้องการเรียนรู้
- การติดตั้งเว็บเซิร์ฟเวอร์ และตั้งค่า SSL (HTTPS) สำหรับเปิดบริการ Dashboard งานวิจัย

```bash
# 1. ติดตั้ง Nginx เว็บเซิร์ฟเวอร์บน Ubuntu
sudo apt install -y nginx

# 2. เปิดใช้งานบริการ Nginx และตั้งให้ทำงานอัตโนมัติตอนเปิดเครื่อง
sudo systemctl enable --now nginx

# 3. ตรวจสอบสถานะการทำงานของ Nginx
sudo systemctl status nginx --no-pager

# 4. ติดตั้ง Certbot และปลั๊กอิน Nginx สำหรับขอ SSL Certificate ฟรี
sudo apt install -y certbot python3-certbot-nginx

# 5. ทดสอบการจำลองต่ออายุ SSL Certificate (Dry Run)
sudo certbot renew --dry-run
```

---

## 6. การตั้งค่า Passwordless sudo (ไม่ต้องกรอกรหัสผ่านทุกครั้ง)

### 🎯 สิ่งที่ต้องการเรียนรู้
- ตั้งค่าให้ `sudo` ไม่ต้องถามรหัสผ่านทุกครั้งที่รันคำสั่ง
- ใช้งานสะดวกขึ้น โดยเฉพาะเวลารัน AI Agent ที่ต้องเรียก `sudo` บ่อย ๆ

### 🧪 ขั้นตอนการตั้งค่า

```bash
# 1. สร้างไฟล์ sudoers สำหรับกลุ่ม admins (ใช้ visudo เพื่อป้องกัน syntax error)
#    ถ้าผู้ใช้ปัจจุบันอยู่ในกลุ่ม admins, sudo, หรือ wheel ก็ใช้กลุ่มนั้นแทน
#    เช็กกลุ่มของผู้ใช้ปัจจุบันด้วย: groups $USER
echo "${USER} ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/${USER}

# 2. ตรวจสอบสิทธิ์และยืนยันว่าใช้งานได้
sudo -v && echo "✅ Passwordless sudo configured!"
```

ตัวอย่างผลลัพธ์เมื่อใช้ไฟล์นี้แล้ว:

```bash
# ก่อนตั้งค่า — ทุกครั้งที่ใช้ sudo ต้องพิมพ์รหัสผ่าน
$ sudo apt update
[sudo] password for utarn: ********

# หลังจากตั้งค่า — ไม่ต้องพิมพ์รหัสผ่านอีก
$ sudo apt update
Hit:1 http://archive.ubuntu.com/ubuntu noble InRelease
# ... ทำงานทันที
```

> ⚠️ **ข้อควรระวัง:** การตั้งค่า passwordless sudo จะลดระดับความปลอดภัยของระบบ ควรใช้เฉพาะใน:
> - เครื่องพัฒนาส่วนตัว (ไม่ใช่เซิร์ฟเวอร์ production)
> - WSL / VM / เครื่องทดสอบที่ไม่มีข้อมูลสำคัญ
> - สถานการณ์ที่ต้องรัน AI Agent ที่เรียก `sudo` บ่อย ๆ

---

## 💡 สรุปเทคนิคสำหรับคนย้ายจาก Windows มา Linux

- **`Ctrl + C`**: ยกเลิกคำสั่งที่กำลังรันอยู่
- **`Tab`**: กดเพื่อเติมชื่อไฟล์/โฟลเดอร์อัตโนมัติ (ช่วยให้ไม่ต้องพิมพ์เองทั้งหมด)
- **`ลูกศรขึ้น (↑)`**: ดึงคำสั่งที่เคยพิมพ์ไว้ก่อนหน้านี้กลับมาใช้
- **`sudo`**: เปรียบเหมือนการ "Run as Administrator" ใน Windows
- **`tmux + เมาส์`**: สโครลล้อเมาส์เพื่อย้อนอ่านคำตอบ AI ยาวๆ และทำงานต่อได้แม้ปิดคอมพิวเตอร์
