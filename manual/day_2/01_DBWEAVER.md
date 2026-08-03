# DBeaver — การติดตั้งและเชื่อมต่อ PostgreSQL ด้วย SSH Tunnel

DBeaver Community Edition คือเครื่องมือจัดการฐานข้อมูลฟรี รองรับ MySQL, PostgreSQL, SQLite, Oracle และมากกว่า 100 ฐานข้อมูล

## สารบัญ

- [การติดตั้ง](#การติดตั้ง)
- [การติดตั้งบน Windows](#การติดตั้งบน-windows)
- [การติดตั้งบน macOS](#การติดตั้งบน-macos)
- [การเพิ่มการเชื่อมต่อ PostgreSQL พร้อม SSH Tunnel](#การเพิ่มการเชื่อมต่อ-postgresql-พร้อม-ssh-tunnel)
- [ทดสอบการเชื่อมต่อ](#ทดสอบการเชื่อมต่อ)

## การติดตั้ง

ดาวน์โหลด DBeaver Community Edition จาก [dbeaver.io/download](https://dbeaver.io/download/)

## การติดตั้งบน Windows

1. ไปที่ [dbeaver.io/download](https://dbeaver.io/download/)
2. คลิกที่ **Windows (64-bit)** เพื่อดาวน์โหลดไฟล์ `dbeaver-ce-*.exe`
3. เปิดไฟล์ที่ดาวน์โหลดแล้วคลิก **Next** ตามขั้นตอน
4. เลือกโฟลเดอร์ติดตั้ง (เรคอมเมนต์เริ่มต้น `C:\Program Files\DBeaver Agent`)
5. คลิก **Install** แล้ว **Finish**
6. เปิด DBeaver ครั้งแรก

> **หรือใช้ winget:**
```powershell
winget install --id DBeaver.DBeaver -e
```

## การติดตั้งบน macOS

1. ไปที่ [dbeaver.io/download](https://dbeaver.io/download/)
2. คลิกที่ **macOS (64-bit)** เพื่อดาวน์โหลดไฟล์ `dbeaver-ce-*.dmg`
3. ลากไอคอน DBeaver ไปยังโฟลเดอร์ **Applications**
4. เปิด **Launchpad** หรือจาก **Applications** เปิด DBeaver

> **หรือใช้ Homebrew:**
```bash
brew install --cask dbeaver-community
```

## การเพิ่มการเชื่อมต่อ PostgreSQL พร้อม SSH Tunnel

การใช้ SSH Tunnel ช่วยให้เชื่อมต่อฐานข้อมูลบนเซิร์ฟเวอร์ระยะไกลอย่างปลอดภัยโดยไม่ต้องเปิดพอร์ต 5432 ไปยังอินเทอร์เน็ต

### ขั้นตอนการเพิ่มการเชื่อมต่อ

1. เปิด DBeaver คลิกขวาที่ **Databases** ใน sidebar เลือก **Create New Database Connection...**

2. เลือกไอคอน **PostgreSQL** (หรือค้นหา "PostgreSQL" ในรายการ)

3. กรอกข้อมูลทั่วไป:

| ฟิลด์ | ค่าตัวอย่าง | คำอธิบาย |
|---|---|---|
| **Host** | `localhost` หรือ `127.0.0.1` | ใช้ localhost เมื่อใช้ SSH Tunnel |
| **Port** | `5432` | พอร์ต PostgreSQL |
| **Database** | `appdb` | ชื่อฐานข้อมูล |
| **Username** | `postgres` | ชื่อผู้ใช้ PostgreSQL |
| **Password** | `*****` | รหัสผ่าน PostgreSQL |

4. คลิกแท็บ **SSH** ด้านบน:

   - เลือก **Use SSH Tunnel**
   - กรอกข้อมูล SSH:

| ฟิลด์ | ค่าตัวอย่าง | คำอธิบาย |
|---|---|---|
| **Host** | `203.0.113.10` | IP หรือ hostname ของเซิร์ฟเวอร์ |
| **Port** | `22` | พอร์ต SSH (มากส่วนมาเป็น 22) |
| **User name** | `ubuntu` หรือ `root` | ชื่อผู้ใช้ SSH |
| **Authentication method** | **Password** หรือ **Public key** | เลือกตามที่ตั้งค่า |
| **Password** | `*****` | รหัสผ่านหรือ private key |

5. คลิก **Test Connection** เพื่อทดสอบ

6. หากสำเร็จ คลิก **Finish**

### การใช้ SSH Key แทนรหัสผ่าน

1. เลือก **Authentication method: Public key**
2. คลิกไอคอนโฟลเดอร์ข้างๆ ฟิลด์ **Private key**
3. เลือกไฟล์ private key (เช่น `id_rsa`)
4. หาก key มี password ให้กรอกในฟิลด์ **Passphrase**

## ทดสอบการเชื่อมต่อ

เมื่อการเชื่อมต่อสำเร็จ:

1. คลิกขวาที่การเชื่อมต่อที่เพิ่ม → **Open**
2. ดู schema ด้านซ้าย คุณควรเห็นรายชื่อตาราง ถ้ามีอยู่แล้ว
3. ลองรันคิวรีง่ายๆ:

```sql
SELECT version();
SELECT current_database();
```

หากเห็นผลลัพธ์แสดงว่าการเชื่อมต่อทำงานแล้ว
