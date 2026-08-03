# Docker — การติดตั้งและใช้งานพื้นฐาน

Docker คือแพลตฟอร์มสำหรับสร้าง ปรับใช้ และจัดการคอนเทนเจอร์ คุณสามารถใช้ Docker Desktop (Windows/macOS) หรือ Docker CE (Linux)

## สารบัญ

- [ติดตั้งบน Windows](#ติดตั้งบน-windows)
- [ติดตั้งบน Ubuntu](#ติดตั้งบน-ubuntu)
- [ติดตั้งบน RHEL / CentOS / Fedora](#ติดตั้งบน-rhel--centos--fedora-dnf)
- [SSH Tunneling](#ssh-tunneling--ใช้สานักงานเครื่องท้องถิ่นเข้าถึงบริการบนเครื่องระยะไกล)
- [คำสั่งพื้นฐาน](#คำสั่งพื้นฐาน)
- [ไฟล์ docker-compose ตัวอย่าง](#ไฟล์-docker-compose-ตัวอย่าง)

## ติดตั้งบน Windows

### วิธีที่ 1: Docker Desktop (แนะนำ)

1. ดาวน์โหลด Docker Desktop จาก [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. เปิดไฟล์ `Docker Desktop Installer.exe` แล้วคลิก **Install**
3. ตามหลังการติดตั้ง ให้เปิด Docker Desktop
4. เข้าสู่ระบบด้วยบัญชี Docker (หรือสร้างใหม่ได้ที่ [hub.docker.com](https://hub.docker.com))

> **หมายเหตุสำหรับ Windows**: Docker Desktop ใช้ WSL 2 เป็นพื้นฐาน หากใช้ Windows 10/11 ควรเปิดใช้งาน WSL 2 ล่วมหน้า

### วิธีที่ 2: ติดตั้งผ่าน winget

เปิด PowerShell และติดตั้ง Docker Desktop ด้วยคำสั่งเดียว:

```powershell
winget install -e --id Docker.DockerDesktop
```

> winget (Windows Package Manager) เป็นตัวจัดการแพ็กเกจในตัวของ Windows 10/11 คำสั่งนี้จะดาวน์โหลดและติดตั้ง Docker Desktop ให้อัตโนมัติ จากนั้นจึงเปิด Docker Desktop ขึ้นมาใช้งาน

### ตรวจสอบการติดตั้ง

เปิด PowerShell หรือ Command Prompt แล้วพิมพ์:

```powershell
docker --version
docker compose version
```

## ติดตั้งบน Ubuntu

### ลงมือติดตั้ง Docker CE

```bash
# อัปเดตแพคเกจ
sudo apt update

# ติดตั้ง依賴 (dependencies)
sudo apt install -y ca-certificates curl gnupg

# เพิ่ม Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# เพิ่ม repository ของ Docker เข้าสู่ apt sources
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# ติดตั้ง Docker Engine
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### เพิ่มผู้ใช้เข้ากลุ่ม docker (ไม่ต้องพิมพ์ sudo)

```bash
sudo usermod -aG docker $USER
```

ออกจากเซสชันแล้วกลับเข้ามา หรือพิมพ์:

```bash
newgrp docker
```

### ตรวจสอบการติดตั้ง

```bash
docker --version
docker compose version
```

## ติดตั้งบน RHEL / CentOS / Fedora (dnf)

สำหรับระบบที่ใช้ตัวจัดการแพ็กเกจ `dnf` (RHEL 9, Rocky Linux, AlmaLinux, Fedora):

```bash
# ล้างแพ็กเกจเก่าที่อาจมีความขัดแย้ง (ถ้ามี)
sudo dnf remove docker docker-client docker-common docker-engine

# ติดตั้งเครื่องมือที่จำเป็น
sudo dnf install -y dnf-plugins-core

# เพิ่ม Docker repository อย่างเป็นทางการ
sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
# Fedora ใช้ URL ของ fedora แทน:
# sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo

# ติดตั้ง Docker Engine
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# เริ่มและเปิดใช้งาน Docker (systemd)
sudo systemctl start docker
sudo systemctl enable docker
```

> หมายเหตุ: บน RHEL/CentOS ต้องใช้ `sudo systemctl start docker` เนื่องจากไม่มีการรันอัตโนมัติหลังติดตั้ง (ต่างจาก Ubuntu ที่ใช้ `dockerd` ผ่าน apt)

### เพิ่มผู้ใช้เข้ากลุ่ม docker (RHEL)

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### ตรวจสอบการติดตั้ง

```bash
docker --version
docker compose version
docker run hello-world
```

## SSH Tunneling — ใช้สำนักงาน/เครื่องท้องถิ่นเข้าถึงบริการบนเครื่องระยะไกล

เมื่อติดตั้ง Docker บนเครื่องระยะไกลแล้ว คุณอาจต้องเข้าถึง service ที่ map port (เช่น PostgreSQL, Redis) จากเครื่องของคุณเอง โดยไม่เปิด port สู่สาธารณะ วิธีที่ปลอดภัยคือ **SSH tunneling (port forwarding)** — สร้างอุโมงค์เข้ารหัสผ่าน SSH

### เปิดใช้งาน SSH server ก่อน (ฝั่งเครื่องระยะไกล)

```bash
# ติดตั้ง OpenSSH Server
sudo apt install -y openssh-server        # Ubuntu/Debian
sudo dnf install -y openssh-server        # RHEL/CentOS/Fedora

sudo systemctl start ssh
sudo systemctl enable ssh
```

### Local port forwarding (เชื่อมจากเครื่องของคุณไปยังเครื่องระยะไกล)

รูปแบบ: `ssh -L [เครื่องของคุณ]:[port]:[localhost ฝั่งระยะไกล]:[port บริการ] ผู้ใช้@เครื่องระยะไกล`

```bash
# ตัวอย่าง: ส่งต่อ port 5433 บนเครื่องคุณ → PostgreSQL port 5432 บนเครื่องระยะไกล
ssh -L 5433:localhost:5432 user@remote-server

# ตัวอย่าง: Dockerized Redis ที่ map port 6380:6379 บนเซิร์ฟเวอร์
ssh -L 6380:localhost:6379 user@remote-server
```

เมื่อสร้าง tunnel แล้ว คุณเชื่อมต่อที่ `localhost:5433` (หรือ `localhost:6380`) บนเครื่องของคุณราวกับว่าบริการรันอยู่ในเครื่อง

> เพิ่ม flag `-N` เพื่อไม่ต้องเปิด shell (`ssh -N -L ...`) และ `-f` เพื่อรันในพื้นหลัง

### ตัวอย่างใช้งานจริง: ติดตั้ง Python และรันเว็บเซิร์ฟเวอร์ผ่าน tunnel

ทำคำสั่งต่อไปนี้บนเครื่องระยะไกลเพื่อติดตั้ง Python แล้วรันเว็บเซิร์ฟเวอร์ง่าย ๆ:

```bash
# ติดตั้ง Python
sudo apt install -y python3 python3-pip        # Ubuntu/Debian
sudo dnf install -y python3 python3-pip        # RHEL/CentOS/Fedora

python3 --version

# รันเว็บเซิร์ฟเวอร์อย่างง่าย (Python HTTP server) บน port 8000
python3 -m http.server 8000
```

ทำการ tunnel จากเครื่องของคุณ:

```bash
ssh -L 8080:localhost:8000 user@remote-server
```

จากนั้นเปิดเบราว์เซอร์ที่ `http://localhost:8080` — คุณจะเห็นรายการไฟล์ของไดเรกทอรีที่รัน `http.server` อยู่บนเซิร์ฟเวอร์

### Remote port forwarding (Reverse tunnel)

ในกรณีที่เครื่องระยะไกลไม่มี IP สาธารณะ ใช้ `-R` กลับทิศ:

```bash
# บนเครื่องระยะไกล: ส่งต่อ port 8000 ของมัน → port 8000 บนเครื่องของคุณ
ssh -R 8000:localhost:8000 user@your-local-machine
```

## คำสั่งพื้นฐาน

| คำสั่ง | คำอธิบาย |
|---|---|
| `docker version` | ดูเวอร์ชัน Docker |
| `docker ps` | แสดงคอนเทนเจอร์ที่ทำงานอยู่ |
| `docker ps -a` | แสดงคอนเทนเจอร์ทั้งหมด (รวมหยุด) |
| `docker pull <image>` | ดาวน์โหลดอิมเมจ |
| `docker run <image>` | สร้างและรันคอนเทนเจอร์ |
| `docker run -d <image>` | รันในโหมดพื้นหลัง (detached) |
| `docker run -p 8080:80 <image>` | โพรตม์ port 8080 → 80 |
| `docker run -v /host/path:/container/path <image>` | เชื่อมโยงโฟลเดอร์ |
| `docker stop <container>` | หยุดคอนเทนเจอร์ |
| `docker start <container>` | เริ่มคอนเทนเจอร์ |
| `docker rm <container>` | ลบคอนเทนเจอร์ |
| `docker images` | แสดงรายชื่ออิมเมจ |
| `docker rmi <image>` | ลบอิมเมจ |

## ไฟล์ docker-compose ตัวอย่าง

โฟลเดอร์ [`docker-compose/`](./docker-compose) มีตัวอย่างไฟล์ docker-compose สำหรับฐานข้อมูลและเครื่องมือค้นหาแรกเริ่ม:

```
docker-compose/
├── postgresql/docker-compose.yml    # PostgreSQL 18
├── timescaledb/docker-compose.yml   # TimescaleDB (PostgreSQL 18)
├── pgvector/docker-compose.yml      # pgvector (PostgreSQL 18)
├── meilisearch/docker-compose.yml   # Meilisearch v1.37
└── redis/docker-compose.yml         # Redis 8.2.7
```

### การใช้งาน

```bash
# เข้าไปยังโฟลเดอร์ของฐานข้อมูลที่ต้องการ
cd docker-compose/postgresql

# รันด้วย docker compose
docker compose up -d

# หยุดและลบ
docker compose down
```

> ใช้ `docker compose` (มีช่องว่าง) ไม่ใช่ `docker-compose` (มี hyphen) ซึ่งเป็นรูปแบบเดิม
