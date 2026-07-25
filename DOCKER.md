# Docker — การติดตั้งและใช้งานพื้นฐาน

Docker คือแพลตฟอร์มสำหรับสร้าง ปรับใช้ และจัดการคอนเทนเจอร์ คุณสามารถใช้ Docker Desktop (Windows/macOS) หรือ Docker CE (Linux)

## สารบัญ

- [ติดตั้งบน Windows](#ติดตั้งบน-windows)
- [ติดตั้งบน Ubuntu](#ติดตั้งบน-ubuntu)
- [คำสั่งพื้นฐาน](#คำสั่งพื้นฐาน)
- [ไฟล์ docker-compose ตัวอย่าง](#ไฟล์-docker-compose-ตัวอย่าง)

## ติดตั้งบน Windows

### วิธีที่ 1: Docker Desktop (แนะนำ)

1. ดาวน์โหลด Docker Desktop จาก [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. เปิดไฟล์ `Docker Desktop Installer.exe` แล้วคลิก **Install**
3. ตามหลังการติดตั้ง ให้เปิด Docker Desktop
4. เข้าสู่ระบบด้วยบัญชี Docker (หรือสร้างใหม่ได้ที่ [hub.docker.com](https://hub.docker.com))

> **หมายเหตุสำหรับ Windows**: Docker Desktop ใช้ WSL 2 เป็นพื้นฐาน หากใช้ Windows 10/11 ควรเปิดใช้งาน WSL 2 ล่วมหน้า

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
