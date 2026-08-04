# PUBLISH — Deploy แอป Vibe Code บน Ubuntu ด้วย Nginx + Certbot

เผยแพร่แอปที่สร้างด้วย vibe coding (เช่น Next.js, Node.js, Python) ออกสู่อินเทอร์เน็ตบนเซิร์ฟเวอร์ Ubuntu โดยใช้ **Nginx** เป็น reverse proxy ส่งทราฟฟิกจากโดเมนไปยังแอปที่รันอยู่บนพอร์ตในเครื่อง แล้วปิดท้ายด้วย **Certbot** เพื่อเปลี่ยนจาก HTTP เป็น HTTPS (ใบรับรอง Let's Encrypt ฟรี) — ทุกอย่างติดตั้งจาก `apt` ไม่ต้องคอมไพล์เอง

**สิ่งที่ต้องมีก่อนเริ่ม:**

- เซิร์ฟเวอร์ Ubuntu (20.04/22.04/24.04) ที่เข้าถึงได้ผ่าน SSH
- โดเมนที่ชี้ **A record** มาที่ IP สาธารณะของเซิร์ฟเวอร์ (เช่น `app.example.com` → `<server-ip>`)
- แอปที่สร้างเสร็จแล้วรันอยู่บนพอร์ตหนึ่งในเครื่อง เช่น `http://127.0.0.1:3000` (ถ้ารันผ่าน docker compose ตรวจให้แน่ใจว่า map พอร์ตออกมาแล้ว: `docker ps` ควรเห็น `0.0.0.0:3000->3000`)

---

## 1. ใช้ Simple Prompt ให้ AI จัดการทั้งหมด (วิธีที่เร็วที่สุด)

ถ้าต้องการให้ Claude Code deploy ให้เองโดยไม่ต้องอ่านขั้นตอนด้านล่างทั้งหมด ให้คัดลอก prompt ด้านล่างวางลงในโปรเจกต์แอป (ปรับโดเมนและพอร์ตให้ตรงกับของคุณ) มันจะติดตั้ง nginx + certbot, สร้าง reverse proxy และเปิด HTTPS ให้เอง โดยใช้ Context7 / Bright Data สอบถาม documentation ล่าสุดของ nginx และ certbot

### ภาษาไทย

```
ฉันมีแอปที่สร้างด้วย vibe coding (Next.js) รันอยู่บนเซิร์ฟเวอร์ Ubuntu
ที่พอร์ต 3000 และโดเมน app.example.com ชี้มาที่เซิร์ฟเวอร์นี้แล้ว

ช่วย deploy แอปนี้ให้หน่อย:
1. ติดตั้ง nginx และ certbot ผ่าน apt
2. สร้าง nginx reverse proxy จากโดเมนไปยัง http://127.0.0.1:3000 (ยังไม่ต้อง HTTPS)
3. ตรวจสอบว่า nginx ทำงานได้และ reload ให้เรียบร้อย
4. ติดตั้ง certbot + python3-certbot-nginx และรัน certbot --nginx
   เพื่อขอใบรับรอง Let's Encrypt และเปิด HTTPS แบบ redirect อัตโนมัติ
5. ทดสอบ certbot renew --dry-run ว่า auto-renewal ทำงาน
ใช้ Context7 และ Brightdata Websearch สอบถาม documentation ล่าสุดของ nginx และ certbot ด้วย
```

### English

```
I have a vibe-coded app (Next.js) running on an Ubuntu server at port 3000,
and the domain app.example.com already points to this server.

Help me deploy the app:
1. Install nginx and certbot via apt.
2. Create an nginx reverse proxy from the domain to http://127.0.0.1:3000 (HTTP only for now).
3. Verify nginx works and reload it.
4. Install certbot + python3-certbot-nginx and run certbot --nginx
   to obtain a Let's Encrypt certificate and enable HTTPS with auto-redirect.
5. Test certbot renew --dry-run to confirm auto-renewal works.
Use Context7 and Brightdata Websearch to look up the latest nginx and certbot documentation.
```

> ขั้นตอนที่ 2–7 ด้านล่างคือสิ่งที่ prompt นี้จะทำทีละขั้นตอน ใช้เป็นข้อมูลอ้างอิงเมื่อต้องการทำเองหรือตรวจสอบสิ่งที่ AI ทำไปแล้ว

---

## 2. ติดตั้ง Nginx จาก apt

อัปเดตรายการแพ็กเกจแล้วติดตั้ง nginx:

```bash
sudo apt update
sudo apt install -y nginx
nginx -v
```

## 3. เริ่มต้น nginx

```bash
sudo systemctl enable --now nginx
sudo systemctl status nginx --no-pager
```

- `enable` — ให้ nginx เริ่มอัตโนมัติทุกครั้งที่บูต
- `--now` — เริ่มบริการทันที
- `status` ควรแสดง `active (running)`

ตรวจสอบว่า port 80 ตอบกลับแล้ว:

```bash
curl -I http://localhost
```

ถ้าเห็นบรรทัด `HTTP/1.1 200 OK` (หน้า default ของ nginx) แสดงว่าทำงานถูกต้อง

## 4. สร้าง nginx reverse proxy (ยังไม่มี HTTPS)

สร้างไฟล์ config ใหม่สำหรับโดเมนของเรา:

```bash
sudo nano /etc/nginx/sites-available/app
```

ใส่เนื้อหาดังนี้ (ปรับ `server_name` และพอร์ตของ `proxy_pass` ให้ตรงกับแอปของคุณ):

```nginx
server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

คำอธิบายบรรทัดสำคัญ:

| บรรทัด | ความหมาย |
|---|---|
| `listen 80;` | รอรับ HTTP บน port 80 — certbot จะเพิ่ม `listen 443 ssl` ให้เองตอนทำ HTTPS |
| `server_name app.example.com;` | โดเมนที่จะแมปมาที่ config นี้ |
| `proxy_pass http://127.0.0.1:3000;` | ส่งต่อทราฟฟิกไปยังแอปที่รันบนพอร์ต 3000 |
| `Upgrade` / `Connection "upgrade"` | จำเป็นสำหรับ WebSocket เช่น HMR ของ Next.js |
| `X-Forwarded-*` | ส่ง IP/โปรโตคอลจริงของผู้ใช้งานให้แอปเพื่อ log และ redirect |

เปิดใช้งาน site แล้ว reload:

```bash
# ลิงก์จาก sites-available ไป sites-enabled
sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/app

# ตรวจ syntax แล้ว reload
sudo nginx -t
sudo systemctl reload nginx
```

- `nginx -t` ต้องออก `syntax is ok` / `test is successful` ก่อน reload
- ถ้าโดเมนของคุณยังไม่ต้องการใช้ site default ของ nginx จะเอาออกก็ได้: `sudo rm /etc/nginx/sites-enabled/default`
- ทดสอบว่า reverse proxy ทำงาน: `curl -H "Host: app.example.com" http://localhost` ควรได้หน้าแอปจริง

## 5. เปิด firewall สำหรับ port 80/443

ถ้าเปิด ufw อยู่ ให้อนุญาต `Nginx Full` (ครอบทั้ง 80 และ 443 ครั้งเดียว):

```bash
sudo ufw allow 'Nginx Full'
sudo ufw status
```

> ใบรับรอง HTTPS ต้องใช้ port 443 — อย่าลืมเปิดเผยให้ Certbot ทำการขอใบรับรองได้สำเร็จ

## 6. ติดตั้ง Certbot จาก apt

ติดตั้ง certbot พร้อมปลั๊กอิน nginx (plugin นี้จะแก้ config ของ nginx ให้เองอัตโนมัติ):

```bash
sudo apt install -y certbot python3-certbot-nginx
certbot --version
```

## 7. รัน Certbot ให้ทำ HTTPS อัตโนมัติ

รันคำสั่งเดียว โดยระบุโดเมน (รองรับหลายโดเมนด้วย `-d` เพิ่มได้):

```bash
sudo certbot --nginx -d app.example.com
```

ครั้งแรก certbot จะถามแบบโต้ตอบ: อีเมลสำหรับแจ้งเตือน, ยอมรับ Terms of Service และถามว่าให้ redirect HTTP→HTTPS หรือไม่ — ตอบ `Y` เพื่อความปลอดภัย

หรือรันแบบไม่โต้ตอบ (ระบุทุกอย่างในคำสั่งเดียว):

```bash
sudo certbot --nginx -d app.example.com --agree-tos -m you@example.com --redirect
```

- `--redirect` — เพิ่มการ redirect จาก `http://` ไป `https://` ใน config ให้อัตโนมัติ
- certbot ทำงานให้เองครบ: ตรวจ nginx config → ขอใบรับรองจาก Let's Encrypt → แก้ไฟล์ site เป็น HTTPS → reload nginx

หลังรันเสร็จ ตรวจดูว่า certbot แก้ไฟล์ config ไปอย่างไร:

```bash
cat /etc/nginx/sites-available/app
sudo nginx -t
```

ควรเห็นจุดที่ certbot เพิ่ม/แก้: `listen 443 ssl`, `ssl_certificate` และ `ssl_certificate_key` ชี้ไปที่ `/etc/letsencrypt/live/app.example.com/…` และ block redirect 301 ไป HTTPS

## 8. Auto-renewal และการทดสอบต่ออายุ

ใบรับรอง Let's Encrypt มีอายุ **90 วัน** — certbot จาก apt ติดตั้ง **systemd timer** ให้อัตโนมัติ จึงต่ออายุได้เองโดยไม่ต้องตั้ง cron:

```bash
# ตรวจว่า timer ถูกตั้งไว้
sudo systemctl list-timers | grep certbot

# ทดลองจำลองการต่ออายุจริง (ไม่แก้ไขใบรับรองจริง)
sudo certbot renew --dry-run
```

`--dry-run` ติดต่อ Let's Encrypt เพื่อจำลองการต่ออายุ ถ้าออก `Congratulations` แสดงว่า auto-renewal พร้อมทำงานทุก ~60 วัน (ต่ออายุล่วงหน้า 30 วันก่อนหมดอายุ)

## 9. ตรวจสอบผลลัพธ์สุดท้าย

```bash
curl -I https://app.example.com
```

ควรได้ `HTTP/1.1 200 OK` และการเข้าถึง `http://app.example.com` ควรถูก redirect ไป HTTPS อัตโนมัติ เปิดในเบราว์เซอร์ก็ได้ ควรเห็นแม่กุญแจ (HTTPS) ขึ้นเขียว

---

## แก้ปัญหาที่พบบ่อย

| อาการ | สาเหตุ / วิธีแก้ |
|---|---|
| `curl http://localhost` ตอบไม่ได้ | nginx ยังไม่รัน: `sudo systemctl start nginx` หรือ firewall บล็อก port 80 |
| `nginx -t` error | syntax ผิดใน config — ดูบรรทัดที่ error แล้วแก้ก่อน reload |
| เข้าเว็บได้แต่ 502 Bad Gateway | `proxy_pass` ชี้ผิดพอร์ต หรือแอปยังไม่รัน ตรวจด้วย `docker ps` / `ss -tlnp` |
| certbot error "domain does not resolve" | โดเมนยังชี้ไม่ถึงเซิร์ฟเวอร์ — ตั้ง A record ให้ชี้ IP ของเครื่องก่อน |
| เปิด HTTPS ไม่ได้ | port 443 ถูกบล็อก — รัน `sudo ufw allow 'Nginx Full'` |

## อ้างอิง

- Nginx — reverse proxy: <https://nginx.org/en/docs/http/ngx_http_proxy_module.html>
- Nginx — sites-available / sites-enabled (Ubuntu): <https://ubuntu.com/server/docs/nginx>
- Certbot — ติดตั้งบน Ubuntu (apt): <https://eff-certbot.readthedocs.io/en/stable/install.html>
- Certbot — ปลั๊กอิน nginx และ auto-renewal: <https://eff-certbot.readthedocs.io/en/stable/using.html#nginx>
