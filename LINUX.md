# คู่มือคำสั่ง Linux พื้นฐาน

เอกสารรวบรวมคำสั่ง Linux ที่ใช้บ่อย แบ่งตามหมวดหมู่ พร้อมตัวอย่างการใช้งาน

---

## สารบัญ

1. [File System](#1-file-system)
2. [Process Monitoring](#2-process-monitoring)
3. [Network](#3-network)
4. [System Status](#4-system-status)
5. [Developer Tools](#5-developer-tools)

---

## 1. File System

คำสั่งสำหรับจัดการไฟล์และไดเรกทอรี

### 1.1 การดูและเปลี่ยนตำแหน่ง

| คำสั่ง | คำอธิบาย |
|---|---|
| `pwd` | แสดงตำแหน่งปัจจุบัน (print working directory) |
| `ls` | แสดงรายการไฟล์/โฟลเดอร์ |
| `cd` | เปลี่ยนไดเรกทอรี |

**ตัวอย่าง:**
```bash
pwd                          # ดูตำแหน่งปัจจุบัน เช่น /home/user
ls                           # แสดงรายการแบบสั้น
ls -l                        # แสดงรายการแบบละเอียด (สิทธิ์, เจ้าของ, ขนาด, วันที่)
ls -la                       # รวมไฟล์ซ่อน (dotfile)
ls -lh                       # แสดงขนาดเป็นหน่วยที่อ่านง่าย (KB, MB)
ls -lt                       # เรียงตามเวลาแก้ไข (ใหม่ก่อน)
ls -ltr                      # เรียงตามเวลา (เก่าก่อน)
cd /var/log                  # เข้าไดเรกทอรี /var/log
cd ~                         # กลับ home directory
cd ..                        # ขึ้นไปหนึ่งระดับ
cd -                         # กลับไดเรกทอรีก่อนหน้า
```

### 1.2 การสร้าง คัดลอก ย้าย ลบ

| คำสั่ง | คำอธิบาย |
|---|---|
| `mkdir` | สร้างไดเรกทอรี |
| `touch` | สร้างไฟล์เปล่า / อัปเดตเวลาไฟล์ |
| `cp` | คัดลอกไฟล์/โฟลเดอร์ |
| `mv` | ย้ายหรือเปลี่ยนชื่อ |
| `rm` | ลบไฟล์/โฟลเดอร์ |

**ตัวอย่าง:**
```bash
mkdir projects                # สร้างโฟลเดอร์ชื่อ projects
mkdir -p a/b/c                # สร้างโฟลเดอร์ซ้อนกันทีเดียว (parent ด้วย)
touch file.txt                # สร้างไฟล์เปล่า
cp file.txt backup.txt        # คัดลอกไฟล์
cp -r folder1 folder2         # คัดลอกทั้งโฟลเดอร์ (recursive)
mv old.txt new.txt            # เปลี่ยนชื่อไฟล์
mv file.txt /tmp/             # ย้ายไฟล์ไป /tmp
rm file.txt                   # ลบไฟล์
rm -r folder                  # ลบโฟลเดอร์พร้อมเนื้อหา
rm -rf folder                 # ลบโดยไม่ถาม (ระวัง!)
```

### 1.3 การดูเนื้อหาไฟล์

| คำสั่ง | คำอธิบาย |
|---|---|
| `cat` | แสดงเนื้อหาทั้งหมด |
| `less` / `more` | ดูทีละหน้า |
| `head` | ดูส่วนต้น |
| `tail` | ดูส่วนท้าย |
| `wc` | นับบรรทัด/คำ/ตัวอักษร |

**ตัวอย่าง:**
```bash
cat /etc/hostname             # ดูเนื้อหาไฟล์
cat -n file.txt               # แสดงพร้อมเลขบรรทัด
less /var/log/syslog          # ดูทีละหน้า (กด q ออก, / ค้นหา)
head -n 20 file.txt           # ดู 20 บรรทัดแรก
tail -n 50 /var/log/syslog    # ดู 50 บรรทัดสุดท้าย
tail -f /var/log/syslog       # ติดตาม log แบบเรียลไทม์ (follow)
wc -l file.txt                # นับจำนวนบรรทัด
wc -w file.txt                # นับจำนวนคำ
```

### 1.4 การค้นหาและกรอง

| คำสั่ง | คำอธิบาย |
|---|---|
| `find` | ค้นหาไฟล์ตามเงื่อนไข |
| `grep` | ค้นหาข้อความในไฟล์ |
| `locate` | ค้นหาไฟล์ผ่าน index (เร็วกว่า find) |

**ตัวอย่าง:**
```bash
find . -name "*.log"                    # หาไฟล์ .log ในโฟลเดอร์ปัจจุบัน
find /var -type f -name "*.conf"        # หาไฟล์ทั้งหมด (type file)
find . -type d -name "test"             # หาโฟลเดอร์ชื่อ test
find . -mtime -7                        # ไฟล์ที่แก้ไขภายใน 7 วัน
find . -size +100M                      # ไฟล์ใหญ่กว่า 100MB
find . -name "*.tmp" -delete            # หาแล้วลบทันที

grep "error" /var/log/syslog            # หาบรรทัดที่มีคำว่า error
grep -i "error" file.log               # ไม่สนใจตัวเล็ก-ใหญ่
grep -r "TODO" ./src                    # ค้นแบบ recursive ทั้งโฟลเดอร์
grep -n "function" app.js               # แสดงเลขบรรทัดด้วย
grep -v "debug" file.log                # แสดงบรรทัดที่ "ไม่มี" คำว่า debug
grep -c "error" file.log               # นับจำนวนบรรทัดที่ตรง
```

### 1.5 สิทธิ์และเจ้าของไฟล์

| คำสั่ง | คำอธิบาย |
|---|---|
| `chmod` | เปลี่ยนสิทธิ์ไฟล์ |
| `chown` | เปลี่ยนเจ้าของไฟล์ |
| `chgrp` | เปลี่ยนกลุ่มเจ้าของ |

โครงสร้างสิทธิ์: `rwx` = read (4) + write (2) + execute (1)

**ตัวอย่าง:**
```bash
chmod 755 script.sh          # owner=rwx, group=rx, others=rx
chmod 644 config.txt         # owner=rw, group=r, others=r
chmod +x deploy.sh           # เพิ่มสิทธิ์ execute
chmod -R 755 folder          # เปลี่ยนทั้งโฟลเดอร์ (recursive)
chown user:group file.txt    # เปลี่ยนเจ้าของและกลุ่ม
chown user file.txt          # เปลี่ยนเจ้าของเท่านั้น
chown -R user:group folder   # เปลี่ยนทั้งโฟลเดอร์
```

### 1.6 การบีบอัดและคลังเก็บ

**ตัวอย่าง:**
```bash
tar -cvf archive.tar folder/      # สร้าง tar (c=สร้าง, v=แสดงรายละเอียด, f=ไฟล์)
tar -xvf archive.tar              # แตกไฟล์ tar
tar -czvf archive.tar.gz folder/  # สร้าง tar.gz (บีบอัดด้วย gzip)
tar -xzvf archive.tar.gz          # แตก tar.gz
tar -xzvf archive.tar.gz -C /tmp  # แตกไปไว้ที่ /tmp
zip -r archive.zip folder/        # สร้าง zip
unzip archive.zip                 # แตก zip
```

---

## 2. Process Monitoring

คำสั่งสำหรับดูและจัดการโปรเซส

### 2.1 ดูโปรเซส

| คำสั่ง | คำอธิบาย |
|---|---|
| `ps` | แสดงสแนปชอตโปรเซส |
| `top` | ดูโปรเซสเรียลไทม์ |
| `htop` | top แบบโต้ตอบสวยงาม (ติดตั้งเพิ่ม) |
| `pgrep` | หา PID ตามชื่อ |

**ตัวอย่าง:**
```bash
ps                         # โปรเซสในเชลล์ปัจจุบัน
ps aux                     # โปรเซสทั้งหมดของระบบ (แบบ BSD)
ps -ef                     # โปรเซสทั้งหมด (แบบ System V)
ps aux | grep nginx        # หาโปรเซส nginx
top                        # มอนิเตอร์แบบเรียลไทม์ (กด q ออก)
htop                       # มอนิเตอร์แบบโต้ตอบ
pgrep -fl nginx            # หา PID ของ nginx พร้อมชื่อเต็ม
```

คอลัมน์สำคัญใน `ps`/`top`:
- `PID` — รหัสโปรเซส
- `%CPU` / `%MEM` — การใช้ CPU/หน่วยความจำ
- `STAT` — สถานะ (R=รัน, S=นอน, Z=ซอมบี้)
- `COMMAND` — คำสั่งที่รัน

### 2.2 จัดการโปรเซส

| คำสั่ง | คำอธิบาย |
|---|---|
| `kill` | ส่งสัญญาณไปยังโปรเซส |
| `killall` | ฆ่าโปรเซสตามชื่อ |
| `pkill` | ฆ่าโปรเซสตามชื่อ/รูปแบบ |
| `jobs` / `fg` / `bg` | จัดการงานเบื้องหลัง |

สัญญาณที่ใช้บ่อย:
- `SIGTERM` (15) — ขอให้จบอย่างสะอาด (ค่าเริ่มต้น)
- `SIGKILL` (9) — บังคับฆ่าทันที (ไม่สามารถดักได้)
- `SIGHUP` (1) — แฮงก์อัป / โหลดคอนฟิกใหม่

**ตัวอย่าง:**
```bash
kill 1234                   # ขอให้โปรเซส PID 1234 จบ
kill -9 1234                # บังคับฆ่า
kill -15 1234               # ขอจบอย่างสะอาด (เหมือนค่าเริ่มต้น)
killall nginx               # ฆ่าโปรเซสชื่อ nginx ทั้งหมด
pkill -f "python app.py"    # ฆ่าตามรูปแบบคำสั่งเต็ม
jobs                        # ดูงานเบื้องหลัง
fg %1                       # นำงาน %1 กลับมาเบื้องหน้า
bg %2                       # ให้งาน %2 รันเบื้องหลังต่อ
Ctrl+Z                      # พักงานปัจจุบันไปเบื้องหลัง
Ctrl+C                      # ยกเลิกงานปัจจุบัน
```

### 2.3 การรันเบื้องหลังและเซสชันถาวร

| คำสั่ง | คำอธิบาย |
|---|---|
| `nohup` | รันโดยไม่ตายเมื่อปิดเทอร์มินัล |
| `&` | รันเบื้องหลัง |
| `screen` / `tmux` | เซสชันเทอร์มินัลถาวร |

**ตัวอย่าง:**
```bash
python app.py &                  # รันเบื้องหลัง
nohup python app.py &            # รันเบื้องหลัง ไม่ตายตอนปิดเทอร์มินัล
nohup python app.py > app.log 2>&1 &   # เก็บ log ด้วย
disown                           # ตัดงานออกจากเชลล์ปัจจุบัน
tmux new -s mysession            # สร้างเซสชัน tmux
tmux attach -t mysession         # เข้าเซสชันอีกครั้ง
```

---

## 3. Network

คำสั่งสำหรับตรวจสอบและจัดการเครือข่าย

### 3.1 ตรวจสอบการเชื่อมต่อ

| คำสั่ง | คำอธิบาย |
|---|---|
| `ping` | ทดสอบการเชื่อมต่อไปโฮสต์ |
| `traceroute` / `tracepath` | ดูเส้นทางแพ็กเก็ต |
| `curl` | ส่ง HTTP request |
| `wget` | ดาวน์โหลดไฟล์ |

**ตัวอย่าง:**
```bash
ping google.com                #  ping ไม่หยุด (Ctrl+C ออก)
ping -c 4 google.com          # ping 4 ครั้งแล้วหยุด
ping -i 2 8.8.8.8             # ping ทุก 2 วินาที
traceroute google.com         # ดูเส้นทางไปยังโฮสต์
curl https://example.com      # ดูเนื้อหาเว็บ
curl -I https://example.com   # ดูเฉพาะ header (status code)
curl -X POST https://api.com -d '{"k":"v"}' -H "Content-Type: application/json"
curl -O https://getsamplefiles.com/download/zip/sample-1.zip   # ดาวน์โหลดเก็บเป็นไฟล์ (ชื่อเดิม)
curl -o sample.zip https://getsamplefiles.com/download/zip/sample-1.zip   # ดาวน์โหลด ตั้งชื่อเอง
wget https://getsamplefiles.com/download/zip/sample-1.zip    # ดาวน์โหลด
wget -c https://getsamplefiles.com/download/zip/sample-1.zip # ดาวน์โหลดต่อ (continue)
```

### 3.2 ดูการเชื่อมต่อและพอร์ต

| คำสั่ง | คำอธิบาย |
|---|---|
| `ss` | ดู socket/การเชื่อมต่อ (แทน netstat) |
| `netstat` | ดูการเชื่อมต่อ (เก่ากว่า) |
| `lsof` | ดูไฟล์/พอร์ตที่โปรเซสเปิดอยู่ |
| `nslookup` / `dig` | ค้นหา DNS |

**ตัวอย่าง:**
```bash
ss -tulpn                      # พอร์ตที่รอรับการเชื่อมต่อ (t=tcp, u=udp, l=listen, p=process, n=numeric)
ss -tn                         # TCP connections ที่เปิดอยู่
ss -tn state established        # เฉพาะที่เชื่อมต่อแล้ว
netstat -tulpn                 # เหมือน ss (รุ่นเก่า)
lsof -i :8080                  # ดูโปรเซสที่ใช้พอร์ต 8080
lsof -i -P -n                  # ดูการเชื่อมต่อทั้งหมด
lsof -p 1234                   # ไฟล์ที่โปรเซส PID 1234 เปิด
nslookup google.com            # ค้น DNS
dig google.com                 # ค้น DNS แบบละเอียด
dig +short google.com          # เฉพาะผลลัพธ์ IP
```

### 3.3 ดูข้อมูลเครือข่ายของเครื่อง

| คำสั่ง | คำอธิบาย |
|---|---|
| `ip` | ดู/ตั้งค่าเครือข่าย (แทน ifconfig) |
| `ifconfig` | ดู network interface (เก่า) |
| `hostname` | ดู/ตั้งชื่อเครื่อง |

**ตัวอย่าง:**
```bash
ip addr                        # ดู IP ทั้งหมด
ip a                           # แบบย่อ
ip route                       # ดูตาราง routing / default gateway
ip link                        # ดู network interface
ip -s link                     # ดูสถิติ interface (rx/tx)
hostname                       # ชื่อเครื่อง
hostname -I                    # IP ของเครื่อง
```

### 3.4 ไฟร์วอลล์และการสแกน

| คำสั่ง | คำอธิบาย |
|---|---|
| `iptables` | ไฟร์วอลล์ระดับเคอร์เนล |
| `ufw` | ไฟร์วอลล์ง่าย (Ubuntu) |
| `nmap` | สแกนพอร์ต (ติดตั้งเพิ่ม) |

**ตัวอย่าง:**
```bash
sudo ufw status                # ดูสถานะไฟร์วอลล์
sudo ufw allow 80/tcp          # เปิดพอร์ต 80
sudo ufw allow from 192.168.1.0/24 to any port 22   # อนุญาตเฉพาะวง LAN
sudo ufw enable                # เปิดไฟร์วอลล์
nmap -sT localhost             # สแกนพอร์ต TCP ของเครื่องตัวเอง
nmap -p 80,443 example.com     # สแกนพอร์ตเฉพาะ
```

---

## 4. System Status

คำสั่งสำหรับตรวจสอบสถานะและทรัพยากรของระบบ

### 4.1 ข้อมูลระบบทั่วไป

| คำสั่ง | คำอธิบาย |
|---|---|
| `uname` | ข้อมูลเคอร์เนล/ระบบ |
| `uptime` | เวลาทำงานและโหลดเฉลี่ย |
| `whoami` | ผู้ใช้ปัจจุบัน |
| `date` | วันที่และเวลา |

**ตัวอย่าง:**
```bash
uname -a                        # ข้อมูลระบบทั้งหมด
uname -r                        # เวอร์ชันเคอร์เนล
uptime                          # เวลาเปิดเครื่อง + load average (1/5/15 นาที)
whoami                          # ชื่อผู้ใช้ปัจจุบัน
date                            # วันที่/เวลาปัจจุบัน
date "+%Y-%m-%d %H:%M:%S"       # รูปแบบกำหนดเอง
```

### 4.2 หน่วยความจำและดิสก์

| คำสั่ง | คำอธิบาย |
|---|---|
| `free` | ดูหน่วยความจำ |
| `df` | ดูพื้นที่ดิสก์ของ filesystem |
| `du` | ดูขนาดไฟล์/โฟลเดอร์ |
| `lsblk` | ดู block device (ดิสก์) |

**ตัวอย่าง:**
```bash
free -h                         # หน่วยความจำแบบอ่านง่าย (h=human)
free -m                         # หน่วยเป็น MB
df -h                           # พื้นที่ดิสก์ทั้งหมด
df -h /                         # เฉพาะ filesystem ของ /
du -sh /var/log                 # ขนาดรวมของโฟลเดอร์
du -h --max-depth=1 /var        # ขนาดแต่ละโฟลเดอร์ย่อย
du -sh * | sort -h              # เรียงตามขนาด (หาไฟล์ใหญ่)
lsblk                           # ดูดิสก์และพาร์ติชัน
```

### 4.3 CPU และโหลด

| คำสั่ง | คำอธิบาย |
|---|---|
| `top` / `htop` | ดูโหลดและโปรเซสเรียลไทม์ |
| `vmstat` | สถิติระบบ (CPU, memory, I/O) |
| `iostat` | สถิติ I/O ของดิสก์ |
| `lscpu` | ข้อมูล CPU |

**ตัวอย่าง:**
```bash
top                             # มอนิเตอร์เรียลไทม์
vmstat 1                        # สถิติระบบทุก 1 วินาที
vmstat 1 5                      # 5 ครั้ง
iostat -x 1                     # สถิติ I/O แบบละเอียด
lscpu                           # ข้อมูล CPU (cores, ความเร็ว, architecture)
nproc                           # จำนวน CPU core
```

### 4.4 ผู้ใช้และการล็อกอิน

| คำสั่ง | คำอธิบาย |
|---|---|
| `who` | ผู้ใช้ที่ล็อกอินอยู่ |
| `w` | ผู้ใช้ที่ล็อกอิน + กำลังทำอะไร |
| `last` | ประวัติการล็อกอิน |
| `id` | รหัสผู้ใช้/กลุ่ม |

**ตัวอย่าง:**
```bash
who                             # ใครล็อกอินอยู่บนเครื่อง
w                               # ล็อกอิน + โปรเซสที่รัน
last                            # ประวัติล็อกอิน (อ่าน /var/log/wtmp)
last -n 10                      # 10 รายการล่าสุด
last -x reboot                  # ประวัติการรีบูต
id                              # uid, gid ของตัวเอง
id username                      # uid, gid ของผู้ใช้อื่น
```

### 4.5 การจัดการบริการ (systemd)

| คำสั่ง | คำอธิบาย |
|---|---|
| `systemctl` | ควบคุมบริการ systemd |
| `journalctl` | ดู log ของระบบ |

**ตัวอย่าง:**
```bash
systemctl status nginx          # สถานะบริการ nginx
systemctl start nginx           # เริ่มบริการ
systemctl stop nginx            # หยุดบริการ
systemctl restart nginx         # รีสตาร์ท
systemctl reload nginx          # โหลดคอนฟิกใหม่โดยไม่ตัดการเชื่อมต่อ
systemctl enable nginx          # ให้เริ่มอัตโนมัติตอนบูต
systemctl disable nginx         # ยกเลิกเริ่มอัตโนมัติ
systemctl list-units --type=service --state=running   # บริการที่รันอยู่
journalctl -u nginx             # log ของ nginx
journalctl -u nginx -f          # ติดตาม log แบบเรียลไทม์
journalctl --since "1 hour ago" # log 1 ชั่วโมงที่แล้ว
journalctl -p err               # เฉพาะ log ระดับ error
```

---

## 5. Developer Tools

คำสั่งที่นักพัฒนาใช้บ่อย

### 5.1 ตัวแปรและสภาพแวดล้อม

| คำสั่ง | คำอธิบาย |
|---|---|
| `echo` | พิมพ์ข้อความ/ค่าตัวแปร |
| `env` / `printenv` | ดูตัวแปรสภาพแวดล้อม |
| `export` | ตั้งตัวแปรสภาพแวดล้อม |
| `source` (`.`) | รันสคริปต์ในเชลล์ปัจจุบัน |

**ตัวอย่าง:**
```bash
echo "Hello"                    # พิมพ์ข้อความ
echo $HOME                      # พิมพ์ค่าตัวแปร HOME
echo $PATH                      # ดู PATH
env                             # ดูตัวแปรสภาพแวดล้อมทั้งหมด
printenv PATH                   # ดูค่าตัวแปรเฉพาะ
export MY_VAR="value"          # ตั้งตัวแปร (ภายในเซสชัน)
export PATH=$PATH:/usr/local/bin   # เพิ่ม path
source ~/.bashrc                # โหลดคอนฟิกใหม่
alias ll='ls -la'               # ตั้งชื่อย่อ
which python3                   # หาตำแหน่งคำสั่ง
```

### 5.2 การเชื่อมต่อและโอนย้ายไฟล์

| คำสั่ง | คำอธิบาย |
|---|---|
| `ssh` | เข้าเครื่องระยะไกล |
| `scp` | คัดลอกไฟล์ผ่าน SSH |
| `rsync` | ซิงค์ไฟล์ (มีประสิทธิภาพ) |

**ตัวอย่าง:**
```bash
ssh user@192.168.1.10           # เข้าเครื่องระยะไกล
ssh -p 2222 user@host          # ใช้พอร์ต 2222
ssh -i key.pem user@host       # ใช้ private key
ssh-keygen -t ed25519          # สร้างคู่กุญแจ SSH
ssh-copy-id user@host          # ส่ง public key ไปเครื่องปลายทาง
scp file.txt user@host:/tmp/   # อัปโหลดไฟล์
scp user@host:/var/log/syslog .  # ดาวน์โหลดไฟล์
scp -r folder user@host:/tmp/  # อัปโหลดทั้งโฟลเดอร์
rsync -avz folder/ user@host:/backup/    # ซิงค์ไฟล์ (a=archive, v=verbose, z=compress)
rsync -avz --delete src/ dest/ # ซิงค์และลบไฟล์ที่ปลายทางไม่มี
```

### 5.3 การดาวน์โหลดและจัดการแพ็กเกจ

| คำสั่ง | คำอธิบาย |
|---|---|
| `apt` | จัดการแพ็กเกจ (Debian/Ubuntu) |
| `yum` / `dnf` | จัดการแพ็กเกจ (RHEL/CentOS/Fedora) |
| `wget` / `curl` | ดาวน์โหลด |

**ตัวอย่าง:**
```bash
sudo apt update                 # อัปเดตรายการแพ็กเกจ
sudo apt upgrade                # อัปเกรดแพ็กเกจที่ติดตั้งไว้
sudo apt install nginx          # ติดตั้ง nginx
sudo apt remove nginx           # ลบ nginx (เก็บคอนฟิก)
sudo apt purge nginx            # ลบพร้อมคอนฟิก
apt search redis                # ค้นหาแพ็กเกจ
apt show nginx                  ข้อมูลแพ็กเกจ
sudo dnf install nginx          # สำหรับ Fedora/RHEL
```

### 5.4 ตัวกรองข้อความและไปป์ไลน์

| คำสั่ง | คำอธิบาย |
|---|---|
| `|` | ไปป์ (ส่งเอาต์พุตเป็นอินพุต) |
| `>` / `>>` | เขียน/ต่อท้ายลงไฟล์ |
| `sort` | เรียงลำดับ |
| `uniq` | กรองบรรทัดซ้ำ |
| `awk` / `sed` | ประมวลผลข้อความ |

**ตัวอย่าง:**
```bash
ls -l | grep ".log"             # หาไฟล์ .log จากรายการ
command > output.txt            # เก็บเอาต์พุตลงไฟล์ (เขียนทับ)
command >> output.txt           # ต่อท้ายไฟล์
command 2> error.log           # เก็บเฉพาะ error (stderr)
command > all.log 2>&1         # เก็บทั้ง stdout และ stderr
sort names.txt                 # เรียงตัวอักษร
sort -n numbers.txt            # เรียงตัวเลข
sort -u names.txt              # เรียงและตัดซ้ำ
sort file | uniq -c            # นับจำนวนแต่ละบรรทัดซ้ำ
awk '{print $1}' access.log    # พิมพ์คอลัมน์ 1
awk -F: '{print $1}' /etc/passwd   # พิมพ์ username (คั่นด้วย :)
sed 's/old/new/g' file.txt     # แทนที่ old เป็น new ทั้งไฟล์
sed -i 's/old/new/g' file.txt  # แก้ไขในไฟล์โดยตรง (in-place)
```

### 5.5 การเรียกใช้งานซ้ำและเวลา

| คำสั่ง | คำอธิบาย |
|---|---|
| `xargs` | รับอินพุตเป็น argument ของคำสั่ง |
| `time` | จับเวลาคำสั่ง |
| `watch` | รันคำสั่งซ้ำทุก N วินาที |
| `history` | ประวัติคำสั่ง |

**ตัวอย่าง:**
```bash
find . -name "*.log" | xargs rm         # ลบไฟล์ .log ทั้งหมดที่หาเจอ
find . -name "*.tmp" | xargs grep foo   # ค้น foo ในไฟล์ที่หาเจอ
xargs -I {} cp {} /backup/ < files.txt # คัดลอกไฟล์ตามรายชื่อ
time python script.py                   # จับเวลาทำงาน
watch -n 2 nvidia-smi                   # รันทุก 2 วินาที
watch -d ls -l                          # รันทุก 2 วินาที พร้อมไฮไลต์สิ่งที่เปลี่ยน
history                                 # ดูประวัติคำสั่ง
history | grep ssh                      # หาคำสั่ง ssh ที่เคยใช้
!42                                     # รันคำสั่งหมายเลข 42 ใน history อีกครั้ง
!!                                      # รันคำสั่งก่อนหน้าอีกครั้ง (มักใช้ sudo !!)
```

### 5.6 ตัวอย่างจริง: ติดตั้ง nginx + certbot (Let's Encrypt)

การติดตั้งเว็บเซิร์ฟเวอร์ nginx และ certbot สำหรับใบรับรอง SSL/TLS ฟรีจาก Let's Encrypt ครบทั้งขั้นตอน

**ขั้นที่ 1 — อัปเดตรายการแพ็กเกจก่อนเสมอ:**
```bash
sudo apt update                 # ดึงรายการแพ็กเกจล่าสุดจาก repository
sudo apt upgrade -y            # อัปเกรดแพ็กเกจที่ติดตั้งไว้ทั้งหมด (-y ตอบ yes อัตโนมัติ)
```

**ขั้นที่ 2 — ติดตั้ง nginx:**
```bash
sudo apt install -y nginx       # ติดตั้ง nginx
nginx -v                        # ตรวจเวอร์ชัน
sudo systemctl status nginx     # ตรวจสถานะ (ควรเป็น active (running))
sudo systemctl enable nginx     # ให้เริ่มอัตโนมัติตอนบูต
sudo systemctl restart nginx    # รีสตาร์ทหลังแก้คอนฟิก
```

ทดสอบ: เปิดเบราว์เซอร์ไปที่ `http://<IP เครื่อง>` ควรเห็นหน้า "Welcome to nginx"
หรือตรวจด้วยคำสั่ง:
```bash
curl -I http://localhost        # ควรได้ HTTP/1.1 200 OK
```

**ขั้นที่ 3 — ติดตั้ง certbot และปลั๊กอิน nginx:**
```bash
sudo apt install -y certbot python3-certbot-nginx   # certbot + ปลั๊กอินสำหรับ nginx
certbot --version              # ตรวจเวอร์ชัน
```

> **หมายเหตุ:** ก่อนขอใบรับรอง โดเมนของคุณต้องชี้ A record มาที่ IP เครื่องนี้แล้ว และพอร์ต 80 ต้องเปิดในไฟร์วอลล์

**ขั้นที่ 4 — ขอใบรับรอง SSL (อัตโนมัติ):**
```bash
sudo certbot --nginx -d example.com -d www.example.com
# --nginx    ให้ certbot แก้คอนฟิก nginx ให้อัตโนมัติ (เพิ่ม HTTPS, redirect)
# -d         ระบุโดเมนที่จะขอใบรับรอง (ระบุได้หลายโดเมน)
```
certbot จะถาม:
1. อีเมลสำหรับรับแจ้งการหมดอายุ
2. ยอมรับเงื่อนไขการใช้งาน (Y)
3. เลือกให้ redirect HTTP → HTTPS อัตโนมัติ (แนะนำเลือก 2)

เมื่อสำเร็จจะได้:
- ใบรับรองที่ `/etc/letsencrypt/live/example.com/`
- nginx ถูกคอนฟิก HTTPS ให้อัตโนมัติ

**ขั้นที่ 5 — ตั้งให้ต่ออายุอัตโนมัติ:**
```bash
sudo certbot renew --dry-run    # ทดสอบกระบวนการต่ออายุ (ไม่ติดต่อจริง)
sudo certbot renew              # ต่ออายุจริง (ปกติจะมี cron/timer ทำให้แล้ว)
sudo systemctl list-timers | grep certbot   # ตรวจ timer ต่ออายุอัตโนมัติ
```
> ใบรับรอง Let's Encrypt มีอายุ 90 วัน ระบบจะพยายามต่ออายุเมื่อใกล้หมด (ภายใน 30 วันสุดท้าย) ผ่าน `certbot.timer` โดยอัตโนมัติ

**ขั้นที่ 6 — ยกเลิก/ลบใบรับรอง (กรณีไม่ใช้แล้ว):**
```bash
sudo certbot delete             # ลบใบรับรอง (จะให้เลือกโดเมน)
sudo apt remove certbot python3-certbot-nginx   # ลบแพ็กเกจ
sudo apt purge certbot          # ลบพร้อมคอนฟิก
```

**คำสั่ง apt ที่เกี่ยวข้อง (สรุป):**
```bash
apt search nginx                # ค้นหาแพ็กเกจที่มีชื่อ/คำว่า nginx
apt show nginx                  # ดูรายละเอียดแพ็กเกจ (เวอร์ชัน, ขนาด, 依赖)
apt list --installed            # ดูแพ็กเกจที่ติดตั้งแล้วทั้งหมด
apt list --upgradable           # ดูแพ็กเกจที่มีเวอร์ชันใหม่กว่า
sudo apt autoremove -y          # ลบแพ็กเกจที่ติดตั้งตามมาแต่ไม่ได้ใช้แล้ว
```

---

## ไอคอนสรุปสำหรับผู้เริ่มต้น

- **ค้นหาว่าคำสั่งทำอะไร:** `man <คำสั่ง>` (กด q ออก) เช่น `man ls`
- **ดูคำสั่งย่อแบบสั้น:** `<คำสั่ง> --help` เช่น `ls --help`
- **`sudo`** = รันในฐานะ root (ระวังทุกครั้ง โดยเฉพาะคำสั่งลบ)
- **`Ctrl+C`** = ยกเลิก / **`Ctrl+Z`** = พัก / **`Tab`** = กรอกชื่ออัตโนมัติ / **`↑`** = คำสั่งก่อนหน้า
