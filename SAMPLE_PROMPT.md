# SAMPLE_PROMPT — สร้าง Todo App ด้วย Next.js + Prisma 7 + PostgreSQL

> คัดลอกเนื้อหาด้านล่างนี้ไปวางใน Claude Code (หรือ AI assistant ตัวใดก็ได้) เพื่อให้สร้างโปรเจค Todo App ตามข้อกำหนด
> ข้อมูลเวอร์ชันและ syntax ได้มาจาก context7 (Next.js 16.2.9, Prisma 7.6.0, Auth.js v5) ณ วันที่ 2026-07-25

---

## โจทย์ (Prompt ภาษาไทย)

ต้องการสร้าง **แอปพลิเคชัน Todo List** โดยใช้เทคโนโลยีดังต่อไปนี้:

- **ภาษา:** TypeScript
- **เฟรมเวิร์ก:** Next.js (เวอร์ชันล่าสุด — 16.x, App Router)
- **ฐานข้อมูล:** PostgreSQL (รันผ่าน Docker Compose เฉพาะโปรเจคนี้)
- **ORM:** Prisma 7
- **การล็อกอิน:** ด้วย **Username/Password** เป็นหลัก (เก็บ password แบบ hash)

### ข้อกำหนดเฉพาะ

1. **Docker Compose สำหรับ PostgreSQL**
   - สร้าง `docker-compose.yml` สำหรับรัน PostgreSQL เฉพาะโปรเจคนี้ (ไม่ใช้ shared instance)
   - **หา port ที่ว่าง** ก่อน map port ระหว่าง container กับ host: หาก port มักจะชนกับ instance อื่น (เช่น `5432`) ให้สแกนหา port ว่างถัดไปที่ไม่ถูกใช้งาน แล้วใช้ port นั้น map กับ port `5432` ภายใน container
   - ตัวอย่างวิธีหา port ว่าง (macOS/Linux):
     ```bash
     # หา PostgreSQL port ว่างถัดจาก 5432 ที่ไม่ถูกใช้
     for p in 5432 5433 5434 5435 5436; do
       lsof -iTCP:$p -sTCP:LISTEN -P -n >/dev/null 2>&1 || { echo "FREE: $p"; break; }
     done
     ```
   - นำ port ที่หาได้มาใส่ใน `docker-compose.yml` เช่น `"<FREE_PORT>:5432"`
   - ใช้ named volume แยดจากโปรเจคอื่น และใส่ `healthcheck` ให้ PostgreSQL

2. **Next.js App Router + TypeScript**
   - ใช้ `npx create-next-app@latest` (เวอร์ชัน 16.x) ติดตั้งด้วย TypeScript, Tailwind CSS, ESLint, App Router, import alias `@/*`
   - โครงสร้างแนะนำ:
     ```
     app/
       (auth)/login/page.tsx
       (auth)/register/page.tsx
       (protected)/todos/page.tsx
       api/auth/[...nextauth]/route.ts
       layout.tsx
       page.tsx
     lib/
       prisma.ts        # PrismaClient singleton
       auth.ts          # Auth.js config (credentials provider)
     prisma/
       schema.prisma
       migrations/
     docker-compose.yml
     .env.example
     ```

3. **Prisma 7** (สังเกตการเปลี่ยนแปลงจาก v6)
   - Generator ใหม่: `provider = "prisma-client"` (ไม่ใช่ `prisma-client-js`) และมี `output = "../generated/prisma"`
   - ใช้ `prisma.config.ts` สำหรับ config (ไม่ใช้ env ใน schema โดยตรง) และอ่าน `DATABASE_URL` จาก `process.env`
   - **Driver adapter:** ใช้ `@prisma/adapter-pg` กับ `PrismaPg` แล้วส่งเข้า `new PrismaClient({ adapter })`
   - Import `PrismaClient` จาก path ที่ generate ไว้ (เช่น `../generated/prisma`)
   - ใช้ **singleton pattern** ผ่าน `globalThis` เพื่อกัน HMR สร้าง client ใหม่ทุกรอบใน dev
   - Schema ตัวอย่าง (ปรับตามต้องการ):
     ```prisma
     generator client {
       provider = "prisma-client"
       output   = "../generated/prisma"
     }

     datasource db {
       provider = "postgresql"
     }

     model User {
       id        String   @id @default(cuid())
       username  String   @unique
       password  String   // เก็บ hash ไม่ใช่ plain text
       name      String?
       todos     Todo[]
       createdAt DateTime @default(now())
     }

     model Todo {
       id        String   @id @default(cuid())
       title     String
       done      Boolean  @default(false)
       userId    String
       user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)
       createdAt DateTime @default(now())
       updatedAt DateTime @updatedAt
     }
     ```

4. **Authentication ด้วย Username/Password**
   - ใช้ **Auth.js (NextAuth v5)** กับ `CredentialsProvider`
   - ตรวจสอบ username/password จากฐานข้อมูลผ่าน Prisma
   - **Hash password** ด้วย `bcrypt` (หรือ `argon2`) — ห้ามเก็บ plain text เด็ดขาด
   - Session strategy: `jwt` (default สำหรับ credentials provider)
   - สร้างหน้า Register สำหรับสมัครสมาชิก และหน้า Login
   - ปกป้อง route `/todos` ด้วย middleware หรือ server-side session check

5. **ฟีเจอร์ Todo (CRUD)**
   - แสดงรายการ todo ของ user ที่ล็อกอินอยู่เท่านั้น
   - เพิ่ม / แก้ไข / ลบ / ทำเครื่องหมายว่า done ผ่าน **Server Actions** ของ Next.js
   - ใช้ server components ดึงข้อมูล และ client components สำหรับ form/interaction

### ขั้นตอนการทำงานที่ต้องการ

1. สแกนหา PostgreSQL port ที่ว่างบน host → ใส่ใน `docker-compose.yml`
2. สร้างโปรเจค Next.js พร้อม TypeScript
3. ตั้งค่า Prisma 7 (schema, `prisma.config.ts`, driver adapter, singleton)
4. สร้าง `docker-compose.yml` รัน PostgreSQL และรัน `docker compose up -d`
5. รัน migration (`npx prisma migrate dev --name init`) และ seed user ตัวอย่าง
6. ตั้งค่า Auth.js v5 credentials provider + bcrypt
7. สร้างหน้า login/register/todos และ server actions สำหรับ CRUD
8. สร้าง `.env.example` พร้อม `DATABASE_URL` และ `AUTH_SECRET`/`NEXTAUTH_SECRET`
9. เขียน `README.md` อธิบายวิธีรัน (รวมขั้นตอนหา port ว่าง)
10. อัปเดต `CLAUDE.md` ของโปรเจคให้มีข้อมูลที่จำเป็น (stack, คำสั่ง dev, โครงสร้างโปรเจค, การจัดการ port)

### ข้อควรระวัง

- **Prisma 7 breaking changes:** ใช้ `prisma-client` generator (ไม่ใช่ `prisma-client-js`) และ import จาก output path ที่กำหนด — อย่าใช้ `import { PrismaClient } from '@prisma/client'` แบบเดิม
- อย่า hardcode `DATABASE_URL` — ใช้ `.env` และให้ `prisma.config.ts` อ่านจาก `process.env`
- หากข้อมูลเวอร์ชันไม่แน่นอน ให้สอบถาม context7 (`npx ctx7@latest docs ...`) ก่อน และหากยังไม่พบ ให้ค้นเว็บผ่าน Bright Data CLI (`bdata search` / `bdata scrape`)
- ห้าม commit `.env` — สร้างเฉพาะ `.env.example`

### ผลลัพธ์ที่คาดหวัง

- โปรเจค Next.js ที่รันได้ (`npm run dev`)
- PostgreSQL รันผ่าน Docker Compose บน port ที่ไม่ชนกับ instance อื่น
- ล็อกอินด้วย username/password ได้จริง
- CRUD todo ได้ครบ และแยกข้อมูลตาม user
- `README.md` และ `CLAUDE.md` ครบถ้วน

---

## ข้อมูลอ้างอิงเวอร์ชัน (Verified via context7 — 2026-07-25)

| Library | Version | Context7 ID |
|---|---|---|
| Next.js | 16.2.9 | `/vercel/next.js/v16.2.9` |
| Prisma | 7.6.0 | `/prisma/prisma/7.6.0` |
| Auth.js (NextAuth) | v5 | (web — `authjs` / `next-auth`) |

### Snippet: สร้าง Next.js app
```bash
npx create-next-app@latest todo-app --ts --tailwind --eslint --app --import-alias "@/*"
cd todo-app
npm install next-auth@beta bcrypt @prisma/adapter-pg pg
npm install -D prisma dotenv @types/bcrypt @types/pg
npx prisma init
```

### Snippet: `prisma.config.ts` (Prisma 7)
```typescript
import "dotenv/config";
import { defineConfig } from "prisma/config";

export default defineConfig({
  schema: "prisma/schema.prisma",
  migrations: { path: "prisma/migrations" },
  datasource: { url: process.env["DATABASE_URL"] },
});
```

### Snippet: `lib/prisma.ts` (singleton + driver adapter)
```typescript
import { PrismaClient } from "../generated/prisma";
import { PrismaPg } from "@prisma/adapter-pg";

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient | undefined };

const adapter = new PrismaPg({ connectionString: process.env.DATABASE_URL! });

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({ adapter, log: process.env.NODE_ENV === "development" ? ["query", "error", "warn"] : ["error"] });

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;
```

### Snippet: `docker-compose.yml` (port ว่างต้องหาก่อน)
```yaml
services:
  postgres:
    image: postgres:18
    container_name: todo-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: todo
      POSTGRES_PASSWORD: todo
      POSTGRES_DB: todoapp
    ports:
      - "${HOST_PG_PORT:-5433}:5432"   # map host port ว่าง → 5432 ใน container
    volumes:
      - todo_pg_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U todo"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  todo_pg_data:
```

### Snippet: `.env.example`
```env
# ค่า HOST_PG_PORT ต้องเป็น port ว่างบน host (ดูวิธีหาใน README)
DATABASE_URL="postgresql://todo:todo@localhost:5433/todoapp"
AUTH_SECRET="generate-with: openssl rand -base64 32"
NEXTAUTH_URL="http://localhost:3000"
```
