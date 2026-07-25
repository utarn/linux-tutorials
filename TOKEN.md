# Token และการพิสูจประสงค์ในแอปพลิเคชัน

Token คือสตริงที่ใช้พิสูจประสงค์และระบุตัวตน มีหลายประเภท แต่ละประเภทใช้งานต่างกัน

## สารบัญ

- [Access Token](#access-token)
- [API Key](#api-key)
- [Cookie](#cookie)
- [JWT (JSON Web Token)](#jwt-json-web-token)
- [การเปรียบเทียบ](#การเปรียบเทียบ)

## Access Token

**Access Token** คือ token ที่ใช้สำหร้บทเข้าสู่ระบบ (authentication) และอนุญาต (authorization) การเข้าถึง API

### วิธีการใช้งาน

```http
GET /api/me HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### ลักษณะ

- มีอายุจำกัด (เช่น 15 นาที, 1 ชั่วโมง)
- ส่งใน HTTP Header ทุกครั้งที่เรียก API
- ไม่ควรเก็บใน localStorage (น่ากังวลเรื่อง XSS)
- ควรใช้ refresh token เพื่อขอ access token ใหม่

### ตัวอย่างโครงสร้าง

```
Access Token = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

## API Key

**API Key** คือสตริงเฉพาะประเภทหนึ่งที่ใช้ระบุตัวแอปพลิเคชัน ไม่ใช่ผู้ใช้

### วิธีการใช้งาน

```http
GET /api/data HTTP/1.1
Host: api.example.com
X-API-Key: sk_live_abc123xyz
```

### ลักษณะ

- ใช้ระบุแอป (แอป A ส่ง key A, แอป B ส่ง key B)
- อาจไม่มีอายุจำกัด
- ใช้สำหรับ rate limiting และการติดตามการใช้งาน
- ต้องเก็บเป็นความลับ (เหมือนรหัสผ่าน)

### การจัดการ API Key

- ให้ผู้ใช้สร้าง/เปลี่ยน key ใน dashboard
- แสดงเฉพาะครั้งเดียวตอนสร้าง (อย่าเก็บค่าไว้ในฐานข้อมูลแบบ plaintext)
- รองรับการสร้างหลาย key สำหรับแอป разных

## Cookie

**Cookie** คือข้อมูลขนาดเล็กที่ server ส่งผ่าน HTTP Response และฝังอัตโนมัติโดยเบราว์เซอร์

### ประเภทของ Cookie ที่ใช้สำหรับ authentication

```http
Set-Cookie: session_id=abc123; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=3600
```

| แอตทริบิวต์ | คำอธิบาย |
|---|---|
| `HttpOnly` | ปิดการเข้าถึงจาก JavaScript (ป้องกัน XSS) |
| `Secure` | ส่งเฉพาะผ่าน HTTPS |
| `SameSite=Lax` | ป้องกัน CSRF (Lax, Strict, None) |
| `Max-Age` | ระยะเวลาหมดอายุ (วินาที) |
| `Path` | URL path ที่ใช้งานได้ |

### ข้อดี vs ข้อเสีย

| ข้อดี | ข้อเสีย |
|---|---|
| อัตโนมัติ ไม่ต้องจัดการ | มีขนาดจำกัด (~4KB) |
| รองรับ HttpOnly + Secure | ต้องใช้เทคนิคพิเศษเพื่อ CSRF |
| ไม่โหลดจาก client-side code | ซ้ำกับ localStorage/sessionStorage |

## JWT (JSON Web Token)

**JWT** คือมาตฐานเปิดสำหรับสร้าง token ที่ปลอดภัยและสะอาด โครงสร้างมี 3 ส่วน separated by จุด

### โครงสร้าง

```
JWT = Base64(header).Base64(payload).Base64(signature)
```

#### Header

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

#### Payload

```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022,
  "exp": 1516242622
}
```

#### Signature

```
HMACSHA256(
  Base64Url(header) + "." +
  Base64Url(payload),
  secret_key
)
```

### ตัวอย่าง JWT จริง

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

### การสร้างและยืนยัน JWT (Node.js)

```javascript
const jwt = require('jsonwebtoken')

// สร้าง token
const token = jwt.sign(
  { userId: 123, email: 'user@example.com' },
  process.env.JWT_SECRET,
  { expiresIn: '1h' }
)

// ยืนยัน token
try {
  const decoded = jwt.verify(token, process.env.JWT_SECRET)
  console.log(decoded.userId) // 123
} catch (err) {
  console.error('Invalid token')
}
```

### ข้อควรระวังเมื่อใช้ JWT

1. **อย่าเก็บข้อมูลลับใน payload** — JWT เฉพาะ signature ที่ถูก encrypt ไม่ใช่ payload
2. **ตั้งอายุจำกัด** — ใช้ `exp` (expiration) และ `iat` (issued at)
3. **ใช้ refresh token** — เมื่อ access token หมด ให้ใช้ refresh token ขอใหม่
4. **เลือกอัลกอริธึมที่ปลอดภัย** — ใช้ HS256 หรือ RS256 ห้ามใช้ `none`

## การเปรียบเทียบ

| คุณสมบัติ | Access Token | API Key | Cookie | JWT |
|---|---|---|---|---|
| ระบุผู้ใช้ | ✅ | ❌ | ✅ | ✅ |
| ระบุแอป | ✅ | ✅ | ❌ | ✅ |
| มีอายุจำกัด | ✅ | บางครั้ง | ✅ | ✅ |
| รองรับ HttpOnly | ❌ | ❌ | ✅ | ไม่เกี่ยว |
| ประเภทข้อมูล | สตริง | สตริง | key=value | JSON Base64 |
| ใช้สำหรับ | Authentication | Service identification | Session management | Stateless auth |
| ปิดกังวล | XSS (ถ้าเก็บ localStorage) | การรั่วไหล | CSRF | การถอดรหัส payload |

## แนวทางปฏิบัติที่ดี

1. **ใช้ Access Token + Refresh Token** — Access Token สั้น (15-30 นาที) พร้อม Refresh Token ยาว (7-30 วัน)
2. **อย่าเก็บ secret ใน client-side code** — ใช้ environment variables บน server
3. **เข้ารหัส HTTPS เสมอ** — ไม่เคยส่ง token ผ่าน HTTP ธรมดา
4. **ระบบ rotation** — เปลี่ยน secret/key เป็นประจำ และให้ผู้ใช้เปลี่ยน API key ได้
5. **ตรวจสอบ scope** — แต่ละ token ควรมี scope ที่ชัดเจน (read, write, admin ฯลฯ)
