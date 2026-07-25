# ORM — Prisma (TypeScript) และ SQLAlchemy (Python)

ORM (Object-Relational Mapping) ช่วยให้คุณจัดการฐานข้อมูลผ่านภาษาโปรแกรมมิ่ง โดยไม่ต้องเขียน SQL โดยตรง

## สารบัญ

- [Prisma 7 (TypeScript)](#prisma-7-typescript)
- [SQLAlchemy (Python)](#sqlalchemy-python)

## Prisma 7 (TypeScript)

Prisma เป็น ORM สมัยใหม่สำหรับ TypeScript ที่มาพร้อมการจัดการ migrations แบบประกาศนียบัตร (declarative) และ Prisma Studio

### การติดตั้ง

```bash
npm init -y
npm install prisma @prisma/client dotenv
npm install -D prisma
```

### การตั้งค่าโปรเจกต์

#### 1. สร้างไฟล์ config `prisma.config.ts`

```typescript
import { defineConfig, env } from 'prisma/config'

type Env = {
  DATABASE_URL: string
}

export default defineConfig({
  schema: 'prisma/schema.prisma',
  migrations: {
    path: 'prisma/migrations',
  },
  datasource: {
    url: env<Env>('DATABASE_URL'),
  },
})
```

#### 2. สร้างไฟล์ schema `prisma/schema.prisma`

```prisma
generator client {
  provider = "prisma-client"
  output   = "../generated/prisma"
}

datasource db {
  provider = "postgresql"
}

model User {
  id        String   @id @default(uuid())
  email     String   @unique
  name      String?
  createdAt DateTime @default(now())
}
```

#### 3. ตั้งค่า environment variables

สร้างไฟล์ `.env`:

```
DATABASE_URL="postgresql://postgres:password@localhost:5432/mydb?schema=public"
```

### คำสั่งพื้นฐาน

| คำสั่ง | คำอธิบาย |
|---|---|
| `npx prisma init` | สร้างโปรเจกต์พื้นฐาน |
| `npx prisma db push` | ปรับ schema ไปยังฐานข้อมูล |
| `npx prisma migrate dev --name <name>` | สร้างและรัน migration |
| `npx prisma studio` | เปิด Prisma Studio ( GUI ) |
| `npx prisma generate` | สร้าง Prisma Client |

### การใช้งาน Prisma Client (TypeScript)

```typescript
import { PrismaClient } from './generated/prisma/client'

const prisma = new PrismaClient()

async function main() {
  // สร้างข้อมูล
  const user = await prisma.user.create({
    data: {
      email: 'user@example.com',
      name: 'John Doe',
    },
  })

  // ค้นหาทุกรายการ
  const users = await prisma.user.findMany()

  // ค้นหาตามเงื่อนไข
  const found = await prisma.user.findUnique({
    where: { email: 'user@example.com' },
  })

  // อัปเดต
  const updated = await prisma.user.update({
    where: { id: user.id },
    data: { name: 'Jane Doe' },
  })

  // ลบ
  await prisma.user.delete({
    where: { id: user.id },
  })
}

main()
  .catch(e => console.error(e))
  .finally(() => prisma.$disconnect())
```

## SQLAlchemy (Python)

SQLAlchemy คือ ORM ที่ครอบคลุมและยืดหยุ่นสำหรับ Python รองรับทั้งระดับต่ำ (SQL expression) และระดับสูง (ORM)

### การติดตั้ง

```bash
pip install sqlalchemy
pip install "sqlalchemy[asyncio]"  # พร้อม async support
```

### การตั้งค่าพื้นฐาน (SQLAlchemy 2.0 Style)

```python
from sqlalchemy import create_engine, ForeignKey, String
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship, Session
)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(120), unique=True)

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name!r})"

# เชื่อมต่อฐานข้อมูล
engine = create_engine("postgresql://user:password@localhost/dbname")

# สร้างตาราง
Base.metadata.create_all(engine)
```

### คำสั่งพื้นฐาน (CRUD)

```python
# ใช้ Session สำหรับการดำเนินการทั้งหมด
with Session(engine) as session:
    # สร้าง (Create)
    new_user = User(name="John Doe", email="john@example.com")
    session.add(new_user)
    session.commit()

    # อ่าน (Read)
    user = session.query(User).filter_by(email="john@example.com").first()

    # ค้นหาทุกรายการ
    all_users = session.query(User).all()

    # อัปเดต (Update)
    user.name = "Jane Doe"
    session.commit()

    # ลบ (Delete)
    session.delete(user)
    session.commit()
```

### การใช้ SQLAlchemy 2.0 Session (แนวสไตล์ใหม่)

```python
from sqlalchemy import select, update, delete

with Session(engine) as session:
    # SELECT
    stmt = select(User).where(User.email == "john@example.com")
    user = session.scalars(stmt).first()

    # UPDATE
    stmt = update(User).where(User.id == 1).values(name="Updated Name")
    session.execute(stmt)
    session.commit()

    # DELETE
    stmt = delete(User).where(User.id == 1)
    session.execute(stmt)
    session.commit()
```

### คำสั่งอื่น ๆ

| คำสั่ง | คำอธิบาย |
|---|---|
| `from sqlalchemy import text` | ใช้ SQL raw query |
| `session.scalars(select(User)).all()` | คิวรีแบบ 2.0 |
| `engine.dispose()` | ปิดการเชื่อมต่อ |
| `Base.metadata.drop_all(engine)` | ลบทุกตาราง |

### การใช้ SQLAlchemy กับ PostgreSQL + Psycopg

```bash
pip install psycopg2-binary  # หรือใช้ asyncpg สำหรับ async
```

```python
engine = create_engine(
    "postgresql+psycopg2://user:password@localhost:5432/mydb"
)
```
