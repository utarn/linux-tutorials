# การตรวจสอบข้อมูลและการจัดรูปแบบโค้ด

การตรวจสอบข้อมูล (Data Validation) ช่วยให้แน่ใจว่าข้อมูลที่เข้าสู่แอปพลิเคชันถูกต้องและปลอดภัย เครื่องมือเหล่านี้ทำงานได้ทั้งในขั้นตอนพัฒนาและรันไทม์

## สารบัญ

- [TypeScript](#typescript)
  - [Zod — ตรวจสอบข้อมูล](#zod--การตรวจสอบข้อมูล)
  - [ESLint — ตรวจจับข้อผิดพลาดโค้ด](#eslint--การตรวจจับข้อผิดพลาดโค้ด)
  - [Prettier — จัดรูปแบบโค้ด](#prettier--การจัดรูปแบบโค้ด)
- [Python](#python)
  - [Pydantic — ตรวจสอบข้อมูล](#pydantic--การตรวจสอบข้อมูล)
  - [Ruff — ตรวจจับข้อผิดพลาดและจัดรูปแบบ](#ruff--การตรวจจับข้อผิดพลาดและจัดรูปแบบ)
  - [Mypy — ตรวจสอบประเภท](#mypy--การตรวจสอบประเภท)
- [Rust](#rust)
  - [Fallow — วิเคราะห์โค้ดเบส (Codebase Intelligence)](#fallow--วิเคราะห์โค้ดเบส-codebase-intelligence)

---

## TypeScript

### Zod — การตรวจสอบข้อมูล

Zod คือไลบรารีตรวจสอบข้อมูลแบบ type-safe สำหรับ TypeScript ที่ใช้ type hints ในการกำหนด schema

**เวอร์ชันล่าสุด:** v3.24.2 (หรือ v4.0.1 หากใช้เป็น canary)

### การติดตั้ง

```bash
npm install zod
# หรือ
yarn add zod
# หรือ
bun add zod
# หรือ
pnpm add zod
```

### ตัวอย่างพื้นฐาน

```typescript
import { z } from 'zod'

// กำหนด schema
const UserSchema = z.object({
  name: z.string().min(3, 'ชื่อต้องมากกว่า 3 ตัวอักษร'),
  email: z.string().email('รูปแบบอีเมลไม่ถูกต้อง'),
  age: z.number().min(0).max(150).optional(),
})

// ประเภทถูกสร้างอัตโนมัติ
type User = z.infer<typeof UserSchema>

// ตรวจสอบข้อมูล
const result = UserSchema.safeParse({
  name: 'John',
  email: 'john@example.com',
})

if (!result.success) {
  console.error(result.error.errors)
}
```

### คำสั่งพื้นฐาน

```typescript
// ใช้งานกับ API (Next.js / Express)
const result = UserSchema.safeParse(requestBody)

if (!result.success) {
  return new Response(JSON.stringify(result.error), { status: 400 })
}

// ใช้งานร่วมกับ React Hook Form
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'

const { register, handleSubmit, formState: { errors } } = useForm({
  resolver: zodResolver(UserSchema),
})
```

---

### ESLint — การตรวจจับข้อผิดพลาดโค้ด

ESLint คือเครื่องมือตรวจจับข้อผิดพลาะและบังคับกฎรูปแบบ JavaScript/TypeScript

**เวอร์ชันล่าสุด:** v9.39.3 (stable) / v10.5.0 (beta)

### การติดตั้ง

```bash
npm install -D eslint
npx eslint --init
```

### คำสั่งพื้นฐาน

```bash
# ตรวจสอบไฟล์หรือโฟลเดอร์
npx eslint src/

# แก้ไขข้อผิดพลาดอัตโนมัติ (autofix)
npx eslint src/ --fix

# ใช้กับ TypeScript
npm install -D @typescript-eslint/eslint-plugin @typescript-eslint/parser
```

### ตัวอย่างการตั้งค่า `.eslintrc.js`

```javascript
module.exports = {
  extends: [
    'eslint:recommended',
    '@typescript-eslint/recommended',
    'prettier', // ปิด rules ที่ conflic กับ Prettier
  ],
  rules: {
    'no-unused-vars': 'off',
    '@typescript-eslint/no-unused-vars': 'error',
  },
}
```

---

### Prettier — การจัดรูปแบบโค้ด

Prettier คือตัวจัดรูปแบบโค้ดอัตโนมัติที่เป็นทางการและไม่มีข้อจำกัด

**เวอร์ชันล่าสุด:** v3.8.3

### การติดตั้ง

```bash
npm install -D prettier
```

### คำสั่งพื้นฐะ

```bash
# จัดรูปแบบทั้งหมด
npx prettier --write "src/**/*.ts"

# ตรวจสอบว่ามีไฟล์ไหนยังไม่จัดรูปแบบ
npx prettier --check "src/**/*.ts"

# ตั้งค่า .prettierrc
```

### ตัวอย่าง `.prettierrc`

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 80,
  "arrowParens": "avoid"
}
```

---

## Python

### Pydantic — การตรวจสอบข้อมูล

Pydantic คือไลบรารีตรวจสอบข้อมูลยอดนิยมใน Python ที่ใช้ type hints

**เวอร์ชันล่าสุด:** v2.14.x (stable)

### การติดตั้ง

```bash
pip install -U pydantic
# หรือใช้ uv (แนะนำ)
uv add pydantic
```

### ตัวอย่างพื้นฐาน

```python
from datetime import datetime
from pydantic import BaseModel, EmailStr, PositiveInt

class User(BaseModel):
    id: int
    name: str = "John Doe"
    email: EmailStr
    age: PositiveInt | None = None
    signup_ts: datetime | None = None

# ตรวจสอบอัตโนมัติ
user = User(
    id="123",          # แปลงเป็น int → 123
    email="john@test.com",
)

print(user.model_dump())  # แปลงเป็น dict
```

### การใช้งานกับ FastAPI

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None

@app.post("/items/")
async def create_item(item: Item):
    return {"item": item.model_dump()}
```

### คำสั่งพื้นฐาน

| คำสั่ง | คำอธิบาย |
|---|---|
| `model.model_dump()` | แปลงเป็น dict |
| `model.model_dump_json()` | แปลงเป็น JSON string |
| `model.model_validate(data)` | สร้างจาก dict |
| `User.model_json_schema()` | สร้าง JSON schema |

---

### Ruff — การตรวจจับข้อผิดพลาดและจัดรูปแบบ

Ruff คือ linter และ formatter ที่เร็วที่สุดเขียนด้วย Rust รองรับกฎจาก Flake8, Black, isort และอื่น ๆ

**เวอร์ชันล่าสุด:** v0.5.0+

### การติดตั้ง

```bash
# วิธีที่ 1: ใช้ uv (แนะนำ)
pip install uv
uv add ruff

# วิธีที่ 2: ใช้ pip
pip install ruff

# วิธีที่ 3: standalone installer (ไม่ต้อง Python)
curl -LsSf https://astral.sh/ruff/install.sh | sh
# Windows:
# powershell -c "irm https://astral.sh/ruff/install.ps1 | iex"
```

### คำสั่งพื้นฐาน

```bash
# ตรวจจับข้อผิดพลาด (lint)
ruff check .

# แก้ไขอัตโนมัติ
ruff check --fix .

# จัดรูปแบบโค้ด (format)
ruff format .

# ใช้เป็น pre-commit hook
```

### ตัวอย่าง `pyproject.toml`

```toml
[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "UP"]
ignore = ["E501"]  # ไม่เช็คความยาวบรรพ์ (+ ใช้ formatter)

[tool.ruff.format]
quote-style = "double"
```

### การเปรียบเทียบ Ruff vs Mypy

| เครื่องมือ | ประเภท | ความเร็ว | รายละเอียด |
|---|---|---|---|
| **Ruff** | Linter + Formatter | ⚡ 10-100x เร็วกว่า | ตรวจจับรูปแบบโค้ด, import order, bugs |
| **Mypy** | Type checker | ปกติ | ตรวจสอบประเภทข้อมูล (static analysis) |

---

### Mypy — การตรวจสอบประเภท

Mypy คือเครื่องมือตรวจสอบประเภทความสงวาน (static type checker) สำหรับ Python

**เวอร์ชันล่าสุด:** v2.1.0

### การติดตั้ง

```bash
python3 -m pip install -U mypy

# ติดตั้ง type stubs สำหรับไลบรารีที่ไม่มี type hints
pip install types-requests
pip install types-PyYAML
```

### คำสั่งพื้นฐาน

```bash
# ตรวจสอบไฟล์เดียว
mypy main.py

# ตรวจสอบทั้งโปรเจกต์
mypy .

# ยืนยากการตรวจสอบ (strict mode)
mypy --strict main.py

# ใช้กับ pyproject.toml
```

### ตัวอย่าง `pyproject.toml`

```toml
[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[[tool.mypy.overrides]]
module = "requests.*"
ignore_missing_imports = true
```

### ตัวอย่างการใช้ type hints กับ Mypy

```python
from typing import Optional

def greet(name: str, age: int) -> str:
    return f"Hello, {name}. You are {age} years old."

# Mypy จะตรวจจับข้อผิดพลาดเหล่านี้:
# greet("John", "25")  # Error: expected int, got str
# result: int = greet("John", 25)  # Error: expected int, got str
```

---

## Rust

### Fallow — วิเคราะห์โค้ดเบส (Codebase Intelligence)

Fallow เป็นเครื่องมือ static analysis เขียนด้วย Rust สำหรับวิเคราะห์โค้ดเบส TypeScript และ JavaScript ไม่ใช่ไลบรารี validation แบบ Zod/Pydantic แต่เป็นเครื่องมือ "codebase intelligence" ที่ตรวจจับโค้ดที่ไม่ได้ใช้, circular dependencies, โค้ดซ้ำซ้อน, complexity hotspot, การละเมิดขอบเขตสถาปัตยกรรม และการ drift ของ design-system styling

**Repository:** https://github.com/fallow-rs/fallow
**เวอร์ชันล่าสุด:** v3.x (ลอยตัวภายใน major version 3)

### การติดตั้ง

```bash
# วิธีที่ 1: ใช้ npm (แนะนำสำหรับโปรเจกต์ TS/JS)
npm install --save-dev fallow

# วิธีที่ 2: ใช้ npx แบบไม่ต้องติดตั้ง (quick check)
npx fallow

# วิธีที่ 3: ใช้ Cargo (เพราะเขียนด้วย Rust)
cargo install fallow-cli

# วิธีที่ 4: ใช้ Docker (ตัวอย่างที่ examples/docker/compose.yaml)
```

### คำสั่งพื้นฐาน

```bash
# รัน pipeline ทั้งหมด (dead code, duplication, health)
npx fallow

# ตรวจเฉพาะสิ่งที่เปลี่ยนใน PR
npx fallow audit

# ตรวจ dead code และ circular deps
npx fallow dead-code

# ตรวจจับโค้ดซ้ำซ้อน
npx fallow dupes

# ดูคะแนนสุขภาพโค้ดเบส
npx fallow health --score

# พรีวิว auto-fix ก่อน apply
npx fallow fix --dry-run

# ตรวจจับ stack และสร้าง config proposal
npx fallow recommend

# สร้าง codebase map แบบ HTML อินเทอร์แอกทิฟ
npx fallow viz
```

### รหัส exit (สำคัญเวลาเขียน CI)

| Exit code | ความหมาย | ถือว่า |
|---|---|---|
| `0` | ผ่าน / สะอาด | ✅ สำเร็จ |
| `1` | มี findings (พบปัญหา) | ✅ สำเร็จ (run สำเร็จ มีผลลัพธ์ให้ดู) |
| `2` | error จริง (ล้มเหลว) | ❌ ล้มเหลว |

> **ข้อแนะนำ:** ใน CI ให้ถือ `0` และ `1` เป็น success และ `2` เป็น failure เท่านั้น มิฉะนั้น Fallow จะหยุด pipeline ทุกครั้งที่พบ findings

---

## สรุปเปรียบเทียบทั้งหมด

| เครื่องมือ | ภาษา | ประเภท | วัตถุประสงค์หลัก |
|---|---|---|---|
| **Zod** | TypeScript | Validation library | ตรวจสอบข้อมูล runtime + type inference |
| **ESLint** | JavaScript/TypeScript | Linter | ตรวจจับข้อผิดพลาดและรูปแบบโค้ด |
| **Prettier** | JavaScript/TypeScript | Formatter | จัดรูปแบบโค้ดอัตโนมัติ |
| **Pydantic** | Python | Validation library | ตรวจสอบข้อมูลด้วย type hints |
| **Ruff** | Python | Linter + Formatter | ตรวจจับข้อผิดพลากและจัดรูปแบบ (เร็วที่สุด) |
| **Mypy** | Python | Type checker | ตรวจสอบประเภทความสงวนแบบสแตติก |
| **Fallow** | Rust (วิเคราะห์ TS/JS) | Static analysis | วิเคราะห์โค้ดเบส: dead code, circular deps, duplication, complexity |
