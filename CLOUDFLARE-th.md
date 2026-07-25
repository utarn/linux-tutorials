# Cloudflare Tunnel (cloudflared) — ติดตั้ง ตั้งค่า เผยแพร่ HTTP

เผยแพร่บริการ HTTP ที่รันอยู่บนเครื่อง Linux (หรือ Windows) ออกสู่อินเทอร์เน็ตผ่าน Cloudflare Zero Trust tunnel โดยไม่ต้องเปิดพอร์ตเข้าเครื่องเลย — connector จะเชื่อมออกหา Cloudflare และ Cloudflare เป็นด่านหน้าของ hostname สาธารณะ

**คำศัพท์** (ตามเอกสาร Cloudflare ปัจจุบัน): **connector** คือ daemon `cloudflared` ที่คุณติดตั้งและรันบน origin — เป็นโพรเซสที่เชื่อมออกหา Cloudflare **tunnel** คือออบเจกต์เชิงตรรกะถาวร (ระบุด้วย **tunnel UUID / tunnel ID**) ที่ connector เชื่อมต่อเข้าไป; tunnel หนึ่งสามารถให้ connector หลายตัว (เรียกว่า **replica**) รันเพื่อสำรองได้ **tunnel token** (`eyJ...`) ใช้ยืนยันตัว connector กับ tunnel ของมัน เมนูใน dashboard ยังคงเป็น **Networking → Tunnels**; "คำสั่งติดตั้ง" ที่แสดงคือคำสั่งติดตั้ง connector ซึ่งฝัง tunnel token ไว้ข้างใน

ขั้นตอน: ติดตั้ง connector (`cloudflared`) → สร้าง remotely-managed tunnel ใน Zero Trust dashboard → คัดลอกคำสั่งติดตั้ง connector (ภายในมี **tunnel token**) → รัน connector บนเครื่อง → เพิ่ม public-hostname route โดยให้ **Service URL** ชี้ไปที่บริการ HTTP ในเครื่อง → Cloudflare สร้าง DNS record ให้อัตโนมัติ

> เครื่องต้องมีทางออกไปยัง Cloudflare บนพอร์ต `7844` (QUIC/HTTP-2) เท่านั้น หากเครื่องอยู่หลังไฟร์วอลล์ที่จำกัด ให้ตรวจสอบก่อนเริ่ม

## 1. ติดตั้ง connector (cloudflared)

### Linux (Debian / Ubuntu) — ผ่าน apt repo ของ Cloudflare

```bash
# นำเข้า signing key ของแพ็กเกจ Cloudflare
sudo mkdir -p --mode=0755 /usr/share/keyrings
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg \
  | sudo tee /usr/share/keyrings/cloudflare-warp.asc >/dev/null

# เพิ่ม repo แล้วติดตั้ง
echo 'deb [signed-by=/usr/share/keyrings/cloudflare-warp.asc] https://pkg.cloudflare.com/cloudflared any main' \
  | sudo tee /etc/apt/sources.list.d/cloudflared.list
sudo apt-get update && sudo apt-get install cloudflared

cloudflared --version
```

### Linux (RHEL / CentOS / Fedora) — ผ่าน rpm repo

```bash
curl -fsSL https://pkg.cloudflare.com/cloudflared.repo | sudo tee /etc/yum.repos.d/cloudflared.repo
sudo yum install cloudflared      # หรือ: sudo dnf install cloudflared
cloudflared --version
```

### Linux — ดาวน์โหลด binary ตรง (distro ใดก็ได้, amd64)

```bash
# ดาวน์โหลด .deb รุ่นล่าสุดจาก GitHub releases มาติดตั้ง หรือรัน binary ตรง ๆ:
curl -fsSL -o cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared
cloudflared --version
```

สถาปัตยกรรม Linux อื่น ๆ (arm64, arm, 386) และแพ็กเกจ `.deb`/`.rpm` อยู่บน[หน้า releases](https://github.com/cloudflare/cloudflared/releases/latest)

### Windows

ดาวน์โหลด [`cloudflared-windows-amd64.msi` รุ่นล่าสุด](https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.msi) จาก GitHub แล้วรัน หรือติดตั้งแบบเงียบจาก PowerShell (รันในฐานะ Administrator):

```powershell
Invoke-WebRequest -Uri "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.msi" -OutFile "$env:TEMP\cloudflared.msi"
Start-Process msiexec.exe -ArgumentList '/i', "$env:TEMP\cloudflared.msi", '/quiet' -Wait
& "C:\Program Files (x86)\cloudflared\cloudflared.exe" --version
```

> `cloudflared` บน Windows **ไม่**อัปเดตอัตโนมัติ ต้องรัน MSI ใหม่เพื่ออัปเกรด

## 2. สร้าง tunnel ใน Zero Trust dashboard

1. เข้าสู่ระบบ [Cloudflare dashboard](https://dash.cloudflare.com/) → **Zero Trust** → **Networks** → **Tunnels** → **Create a tunnel** (ลิงก์ตรง: <https://dash.cloudflare.com/?to=/:account/tunnels>)
2. เลือก **Cloudflare Tunnel**
3. ตั้งชื่อ tunnel (เช่น `linux-edge-01`) แล้วเลือก **Create tunnel**
4. เลือกระบบปฏิบัติการ (**Linux** หรือ **Windows**) dashboard จะแสดงคำสั่งติดตั้ง — คัดลอกไว้ จะมีลักษณะเช่น:

   ```bash
   cloudflared service install eyJhIjoi...long-token-string...==
   ```

   สตริง `eyJ...` คือ **tunnel token** ใครมี token นี้ก็รัน tunnel นี้ได้ จึงต้องเก็บเป็นความลับ

5. รันคำสั่งนั้นบนเครื่อง (ดูขั้นตอนที่ 4) สถานะ tunnel จะเปลี่ยนเป็น **Healthy** เมื่อ connector เชื่อมต่อกลับ แล้วเลือก **Continue**

## 3. ขอ tunnel token และ tunnel ID

**Tunnel token** (`eyJ...`) ใช้ยืนยันตัว connector กับ tunnel ของมัน — เป็นสิ่งเดียวที่ remotely-managed tunnel ต้องการเพื่อรัน **Tunnel ID** (UUID) ระบุตัว tunnel เองและปรากฏใน CNAME ของ `cfargotunnel.com` และ API

### จาก dashboard

- **Token**: เปิด tunnel → แท็บ **Overview** → **Add a replica** (หรือ **Refresh token**) → คัดลอกสตริง `eyJ...` ออกจากคำสั่งติดตั้ง connector
- **Tunnel ID**: แถวของ tunnel ใน **Networks → Tunnels** จะแสดง UUID หน้ารายละเอียดของ tunnel ในแท็บ **Overview** ก็มีเช่นกัน

### จาก API

```bash
# Account ID: dashboard → โดเมนใดก็ได้ → แถบขวา "Account ID"
# Tunnel ID: จาก dashboard (ด้านบน)
# API token: My Profile → API Tokens → Create Token (ดูสิทธิ์ด้านล่าง)

curl "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/cfd_tunnel/$TUNNEL_ID/token" \
  --request GET \
  --header "Authorization: Bearer $CLOUDFLARE_API_TOKEN"
```

ผลลัพธ์ในฟิลด์ `result` คือ token string

## 4. รัน connector (พร้อม token)

สำหรับ remotely-managed tunnel ไม่ต้องมี `config.yml` — dashboard เก็บ config แล้วส่งให้ connector

### Linux — รันตรง ๆ (foreground สำหรับทดสอบ)

```bash
cloudflared tunnel --token eyJhIjoi... run
```

### Linux — รัน connector เป็น systemd service

```bash
# คำสั่งติดตั้ง connector จาก dashboard ทำสิ่งนี้อยู่แล้ว; ถ้าทำเอง:
sudo cloudflared service install eyJhIjoi...long-token-string...==
sudo systemctl enable --now cloudflared
systemctl status cloudflared
```

รีสตาร์ทหลังเปลี่ยน config: `sudo systemctl restart cloudflared`

### Windows — รัน connector เป็น Windows service (Administrator CMD หรือ PowerShell)

```powershell
# คำสั่งติดตั้ง connector บน Windows จาก dashboard ติดตั้ง service พร้อม token:
& "C:\Program Files (x86)\cloudflared\cloudflared.exe" service install eyJhIjoi...long-token-string...==
sc start cloudflared
sc query cloudflared
```

## 5. เผยแพร่ HTTP จากเครื่อง Linux

เพิ่ม **public-hostname route** ให้ tunnel — เพื่อแมป hostname สาธารณะกับบริการในเครื่อง

1. Dashboard → **Networks → Tunnels** → tunnel ของคุณ → แท็บ **Public Hostname** → **Add a public hostname**
2. กรอก:
   - **Subdomain**: เช่น `app`
   - **Domain**: เลือกโซนที่จัดการใน Cloudflare เช่น `mydomain.com`
   - **Path**: ปล่อยว่าง ยกเว้นต้องการกำหนดเฉพาะ path
   - **Service** → **Type**: `HTTP`
   - **URL**: ที่อยู่ของบริการ **ในเครื่อง** ตรงนี้คือจุดที่คุณกำหนด IP/พอร์ตของสิ่งที่จะเผยแพร่ ตัวอย่าง:
     - `localhost:8080` — บริการที่รันอยู่บนเครื่องนั้นเอง
     - `127.0.0.1:80` — แบบเดียวกัน ระบุ loopback ชัด ๆ
     - `10.0.0.5:8080` — บริการบนเครื่องในวง private ที่เครื่อง tunnel เข้าถึงได้
     - สำหรับ origin แบบ HTTPS: Type `HTTPS`, URL `10.0.0.5:443` และเปิด **TLS → No TLS Verify** หาก origin ใช้ cert ที่ self-signed
3. **Save**

ตอนนี้ Cloudflare จะเผยแพร่ `https://app.mydomain.com` → `http://localhost:8080` ในเครื่องของคุณ Cloudflare สิ้นสุด TLS ที่ edge; ช่วงระหว่าง `cloudflared` กับ origin เป็น HTTP บนเครือข่ายส่วนตัว

DNS record ของ `app.mydomain.com` ถูกสร้างอัตโนมัติเป็น **CNAME** → `<tunnel-id>.cfargotunnel.com` คุณ**ไม่ต้อง**สร้างเอง และมัน**ไม่ใช่** A record (ดูหัวข้อถัดไป)

## 6. DNS — tunnel ใช้ CNAME ไม่ใช่ A record

สำหรับ public-hostname tunnel route Cloudflare จะสร้าง:

```
app.mydomain.com.   CNAME   <tunnel-id>.cfargotunnel.com.
```

ทราฟฟิกลงบน IP ของ Cloudflare edge ไม่ใช่ IP ของเครื่อง tunnel — นั่นคือจุดประสงค์ของ tunnel **ไม่มี A record ที่ชี้ไป IP เครื่องของคุณสำหรับ hostname ที่เผยแพร่** ห้ามสร้าง A record ชี้ทับ เพราะจะไปบดบัง/ทำให้ CNAME เสีย

ที่ที่ **A record** เกี่ยวข้อง (และส่วน "กำหนด IP address" อยู่):

- **Origin / Service URL** (ขั้นตอนที่ 5): คุณกำหนด IP *ภายใน* ของบริการที่จะเผยแพร่ เช่น `http://10.0.0.5:8080` นี่คือที่อยู่ที่ `cloudflared` จะเรียกบนเครือข่ายส่วนตัว — ไม่ใช่ DNS record แต่เป็น Service URL ของ route
- **A record จริงของ hostname อื่น** (เช่นเครื่องที่ไม่ใช่ tunnel ที่คุณชี้ไป IP สาธารณะ): สร้างภายใต้ **Websites → โดเมนของคุณ → DNS → Records → Add record → A** พร้อม host name และที่อยู่ IPv4 record นี้ต้องใช้สิทธิ์ **DNS → Edit** (ด้านล่าง) และแยกจาก tunnel

หากคุณต้องการให้ `cloudflared` จัดการ DNS ของ tunnel hostname เองผ่าน CLI (`cloudflared tunnel route dns <tunnel> app.mydomain.com`) มันก็ยังสร้างเป็น **CNAME** และ API token ต้องมีสิทธิ์ **DNS Edit** บนโซนนั้น

## 7. สิทธิ์ที่ต้องการ

มี 2 บริบท: การรัน connector (ใช้ token ตาม flow ของ dashboard) กับการจัดการ tunnel ผ่าน API/CLI (ใช้ API token ที่มีสิทธิ์เหมาะสม)

### เพื่อรัน connector (Zero Trust tunnel แบบจัดการด้วย dashboard)

| สิ่งที่ต้องทำ | วิธี | ใครต้องมี |
|---|---|---|
| รัน connector (`cloudflared`) | แค่ **tunnel token** (`eyJ...`) | ใครที่มี token ก็รัน tunnel นี้ได้ — เก็บเป็นความลับ |

ไม่ต้องมี API token ไม่ต้องมี `cert.pem` ไม่ต้องมีบทบาทระดับโซนบนเครื่อง token ถูกจำกัดอยู่ที่ tunnel นี้เดียว

### เพื่อสร้าง / อ่าน / หมุนเวียน tunnel token ผ่าน API

**API token** (My Profile → API Tokens → Create Token) ที่มีอย่างน้อยหนึ่งใน:

- `Cloudflare One Connectors — Write`, **หรือ**
- `Cloudflare One Connector: cloudflared — Write`, **หรือ**
- `Cloudflare Tunnel — Write`

(สิทธิ์ระดับ Account)

### เพื่อสร้าง tunnel และ DNS route ผ่าน CLI / API token

สร้าง custom token ภายใต้ **My Profile → API Tokens → Create Token → Custom token** พร้อม:

| สิทธิ์ | ระดับ | ใช้เพื่อ |
|---|---|---|
| **Account → Cloudflare Tunnel — Edit** | Account | สร้าง/ลบ/route tunnel, `cloudflared tunnel create`, `cloudflared tunnel route dns` |
| **Zone → DNS — Edit** | Zone (โซนที่เผยแพร่) | สร้าง CNAME สำหรับ public hostname (อัตโนมัติเมื่อเพิ่ม route ใน dashboard หรือผ่าน `cloudflared tunnel route dns`) |
| **Zone → Zone — Read** | Zone (โซนที่เผยแพร่) | แสดงรายการโซนเมื่อต่อ DNS ผ่าน CLI |
| *(ไม่บังคับ)* **Account → Access — Apps and Policies — Edit** | Account | ถ้าจะใส่ Cloudflare Access policy หน้า URL ที่เผยแพร่ด้วย |

> `cloudflared tunnel login` (flow แบบ locally-managed ดั้งเดิมที่เขียน `cert.pem`) ต้องใช้บทบาทสมาชิกระดับ account + DNS + Load Balancer และให้สิทธิ์จัดการ tunnel ทั้ง account — ควรใช้ flow token ของ dashboard เว้นแต่ต้องการ `cert.pem` แบบ local จริง ๆ

### ขั้นต่ำสำหรับ "เผยแพร่ HTTP จากเครื่อง Linux นี้" (flow ของ dashboard)

บนเครื่องไม่ต้องมี API token เลย dashboard สร้าง tunnel, CNAME และ route; คุณแค่คัดลอก tunnel token ขึ้นเครื่อง (มันจะติดตั้ง connector) สิทธิ์ด้านบนมีผลก็ต่อเมื่อคุณเขียนสคริปต์สร้าง tunnel หรือ DNS ผ่าน CLI/API เท่านั้น

## อ้างอิง

- ดาวน์โหลด / ติดตั้ง: <https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/>
- สร้าง tunnel (dashboard): <https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/get-started/create-remote-tunnel/>
- สิทธิ์ tunnel (token เทียบกับ API token): <https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/configure-tunnels/remote-tunnel-permissions/>
- รันเป็น service — Linux: <https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/local-management/as-a-service/linux/>
- รันเป็น service — Windows: <https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/local-management/as-a-service/windows/>
