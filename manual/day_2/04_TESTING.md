# Test Framework — TypeScript และ Python บน Windows และ Linux

เอกสารสรุป **Test Framework** สำหรับ TypeScript (Vitest) และ Python (pytest) ครอบคลุมการติดตั้ง คำสั่งพื้นฐาน ไปจนถึงแนวคิด **TDD (Test-Driven Development)**

---

## สารบัญ

1. [ภาพรวม Framework](#1-ภาพรวม-framework)
2. [TypeScript — Vitest](#2-typescript--vitest)
   - [การติดตั้ง (Windows และ Linux)](#21-การติดตั้ง-windows-และ-linux)
   - [คำสั่งพื้นฐานที่ควรรู้](#22-คำสั่งพื้นฐานที่ควรรู้)
   - [โครงสร้างเทส](#23-โครงสร้างเทส)
   - [การปรับแต่ง Config](#24-การปรับแต่ง-config)
   - [Coverage Report](#25-coverage-report)
3. [Python — pytest](#3-python--pytest)
   - [การติดตั้ง (Windows และ Linux)](#31-การติดตั้ง-windows-และ-linux)
   - [คำสั่งพื้นฐานที่ควรรู้](#32-คำสั่งพื้นฐานที่ควรรู้)
   - [โครงสร้างเทส](#33-โครงสร้างเทส)
   - [Fixtures และ Parametrize](#34-fixtures-และ-parametrize)
   - [Coverage Report](#35-coverage-report)
4. [TDD (Test-Driven Development)](#4-tdd-test-driven-development)
   - [วงจร TDD: Red-Green-Refactor](#41-วงจร-tdd-red-green-refactor)
   - [ตัวอย่าง TDD ด้วย TypeScript (Vitest)](#42-ตัวอย่าง-tdd-ด้วย-typescript-vitest)
   - [ตัวอย่าง TDD ด้วย Python (pytest)](#43-ตัวอย่าง-tdd-ด้วย-python-pytest)
5. [เครื่องมือเสริม](#5-เครื่องมือเสริม)

---

## 1. ภาพรวม Framework

| คุณสมบัติ | TypeScript | Python |
|-----------|-----------|--------|
| **Framework หลัก** | Vitest (แนะนำ), Jest | pytest |
| **การติดตั้ง** | npm / pnpm / yarn | pip / pipx |
| **การรันเทส** | CLI: `vitest` | CLI: `pytest` |
| **Watch Mode** | ✅ มี (ค่าเริ่มต้น) | ✅ `pytest-watch` หรือ `pytest --loop` |
| **Code Coverage** | ✅ `vitest run --coverage` | ✅ `pytest --cov` (ใช้ pytest-cov) |
| **Fixture / Setup** | `beforeEach`, `afterEach` | `@pytest.fixture` |
| **Parametrize** | `test.each(...)` | `@pytest.mark.parametrize` |
| **Mock** | `vi.mock()`, `vi.spyOn()` | `unittest.mock` หรือ `pytest-mock` |

---

## 2. TypeScript — Vitest

[Vitest](https://vitest.dev) เป็น Test Framework ยุคถัดไปที่ทำงานบน Vite รองรับ ESM, TypeScript, JSX ทันที และมี Watch Mode ที่เร็วมาก

> **ข้อกำหนด:** Node.js 18+ (แนะนำ LTS)

### 2.1 การติดตั้ง (Windows และ Linux)

คำสั่งเหมือนกันทั้ง Windows (PowerShell) และ Linux (bash):

```bash
# 1. สร้างโปรเจกต์ใหม่ (ถ้ายังไม่มี)
mkdir my-project
cd my-project
npm init -y

# 2. ติดตั้ง Vitest
npm install -D vitest

# 3. (ทางเลือก) ติดตั้ง Coverage Provider
npm install -D @vitest/coverage-v8
```

สำหรับโปรเจกต์ที่มีอยู่แล้ว:

```bash
npm install -D vitest
```

### 2.2 คำสั่งพื้นฐานที่ควรรู้

```bash
# รันเทส (Watch Mode — ค่าเริ่มต้น แก้ไฟล์แล้วรันอัตโนมัติ)
vitest

# รันเทสครั้งเดียว (ใช้ใน CI)
vitest run

# รันเทสเฉพาะไฟล์
vitest run src/utils.test.ts

# รันเทสที่ชื่อตรงกับ keyword
vitest run -t "should return"

# รันเทสพร้อม Coverage
vitest run --coverage

# รันเทสแบบ UI (เปิดหน้าเว็บ)
vitest --ui

# แสดงช่วยเหลือ
vitest --help
```

เพิ่ม Script ใน `package.json`:

```json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage"
  }
}
```

แล้วเรียกผ่าน:

```bash
npm test          # watch mode
npm run test:run  # run once
```

### 2.3 โครงสร้างเทส

```typescript
// math.ts — ฟังก์ชันที่ต้องการทดสอบ
export function add(a: number, b: number): number {
  return a + b;
}

export function divide(a: number, b: number): number {
  if (b === 0) throw new Error("Cannot divide by zero");
  return a / b;
}

export function isEven(n: number): boolean {
  return n % 2 === 0;
}
```

```typescript
// math.test.ts — ไฟล์เทส (วางข้าง ๆ ไฟล์ที่เทส หรือในโฟลเดอร์ __tests__)
import { describe, it, expect } from "vitest";
import { add, divide, isEven } from "./math";

describe("add()", () => {
  it("should add two positive numbers", () => {
    // Arrange
    const a = 2;
    const b = 3;

    // Act
    const result = add(a, b);

    // Assert
    expect(result).toBe(5);
  });

  it("should add negative numbers correctly", () => {
    expect(add(-1, -2)).toBe(-3);
  });
});

describe("divide()", () => {
  it("should divide numbers correctly", () => {
    expect(divide(10, 2)).toBe(5);
  });

  it("should throw on division by zero", () => {
    expect(() => divide(1, 0)).toThrow("Cannot divide by zero");
  });
});

describe("isEven()", () => {
  it.each([
    [2, true],
    [3, false],
    [0, true],
    [-4, true],
  ])("should return %s for %i", (n, expected) => {
    expect(isEven(n)).toBe(expected);
  });
});
```

รันเทส:

```bash
vitest run math.test.ts
```

### 2.4 การปรับแต่ง Config

สร้างไฟล์ `vitest.config.ts` ที่ root ของโปรเจกต์:

```typescript
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,                // ใช้ describe/it/expect ได้โดยไม่ต้อง import
    environment: "node",          // หรือ "jsdom" สำหรับ DOM testing
    include: ["src/**/*.test.ts"],// pattern ที่จะค้นหาไฟล์เทส
    setupFiles: ["./src/test-setup.ts"], // รันก่อนเทสทั้งหมด
  },
});
```

### 2.5 Coverage Report

```bash
# รันพร้อมรายงาน Coverage
vitest run --coverage
```

Coverage Report จะแสดงใน Terminal และสร้างโฟลเดอร์ `coverage/` สำหรับ HTML report

สามารถเปิดดู HTML report ด้วย:

```bash
npx playwright open coverage/index.html
```

---

## 3. Python — pytest

[pytest](https://docs.pytest.org) เป็น Test Framework มาตรฐานของ Python เขียนเทสได้สั้นและอ่านง่าย มีฟีเจอร์ Fixtures, Parametrize และ Plugin มากมาย

> **ข้อกำหนด:** Python 3.9+

### 3.1 การติดตั้ง (Windows และ Linux)

```bash
# ติดตั้ง pytest
pip install pytest

# หรือติดตั้งพร้อม Coverage
pip install pytest pytest-cov
```

**Windows (PowerShell) เพิ่มเติม:** ตรวจสอบว่า Python และ pip อยู่ใน PATH:

```powershell
python --version
pip --version
```

**Linux เพิ่มเติม:** ถ้าใช้ Python virtual environment (แนะนำ):

```bash
python3 -m venv venv
source venv/bin/activate
pip install pytest pytest-cov
```

### 3.2 คำสั่งพื้นฐานที่ควรรู้

```bash
# รันเทสทั้งหมดในโฟลเดอร์ปัจจุบัน
pytest

# รันเทส verbose (แสดงชื่อเทสทุกอัน)
pytest -v

# รันเทสเฉพาะไฟล์
pytest test_math.py

# รันเทสที่ชื่อมีคำว่า "fast"
pytest -k "fast"

# รันเทสเฉพาะกลุ่ม marker
pytest -m "slow"

# รันเทสพร้อม Coverage
pytest --cov=. --cov-report=term-missing

# หยุดเมื่อเทสแรก fail
pytest -x

# รันแบบแสดง print() output
pytest -s
```

### 3.3 โครงสร้างเทส

```python
# math.py — ฟังก์ชันที่ต้องการทดสอบ
def add(a: int, b: int) -> int:
    return a + b

def divide(a: int, b: int) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def is_even(n: int) -> bool:
    return n % 2 == 0
```

```python
# test_math.py — ไฟล์เทส (ต้องขึ้นต้นด้วย test_ หรือลงท้ายด้วย _test)
import pytest
from math import add, divide, is_even

def test_add_two_positive_numbers():
    # Arrange
    a = 2
    b = 3

    # Act
    result = add(a, b)

    # Assert
    assert result == 5

def test_add_negative_numbers():
    assert add(-1, -2) == -3

def test_divide_numbers():
    assert divide(10, 2) == 5.0

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(1, 0)

# Parametrize — ทดสอบหลายค่าด้วยเทสเดียว
@pytest.mark.parametrize("n, expected", [
    (2, True),
    (3, False),
    (0, True),
    (-4, True),
])
def test_is_even(n, expected):
    assert is_even(n) == expected
```

รันเทส:

```bash
pytest test_math.py -v
```

### 3.4 Fixtures และ Parametrize

**Fixtures** — ใช้สำหรับเตรียมข้อมูลหรือสภาพแวดล้อมซ้ำ ๆ:

```python
# conftest.py — ไฟล์ส่วนกลางสำหรับ fixtures (วางใน root หรือโฟลเดอร์ของเทส)
import pytest

@pytest.fixture
def sample_user():
    """สร้างข้อมูลผู้ใช้ตัวอย่างสำหรับเทส"""
    return {"name": "Alice", "age": 30, "active": True}

@pytest.fixture
def db_connection():
    """จำลองการเชื่อมต่อฐานข้อมูล"""
    conn = create_mock_db()
    yield conn  # ส่งค่ากลับไปให้เทสใช้
    conn.close()  # cleanup หลังจากเทสเสร็จ
```

```python
# test_user.py
def test_user_is_active(sample_user):
    assert sample_user["active"] is True

def test_user_age(sample_user):
    assert sample_user["age"] >= 18
```

**Parametrize** — ทดสอบหลาย input ด้วยฟังก์ชันเดียว:

```python
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_add_various_inputs(a, b, expected):
    assert add(a, b) == expected
```

### 3.5 Coverage Report

```bash
# แสดง Coverage ใน Terminal
pytest --cov=. --cov-report=term-missing

# สร้าง HTML Report
pytest --cov=. --cov-report=html
# แล้วเปิด coverage/index.html
```

---

## 4. TDD (Test-Driven Development)

TDD คือกระบวนการพัฒนาซอฟต์แวร์ที่ **เขียนเทสก่อนแล้วค่อยเขียนโค้ด** เพื่อให้ได้โค้ดที่ถูกต้องตั้งแต่แรกและมีเทสครอบคลุมทุกกรณี

### 4.1 วงจร TDD: Red-Green-Refactor

```
┌─────────────────────────────────────────────┐
│                                             │
│   🔴 RED — เขียนเทสที่ยังไม่ผ่าน              │
│   (เทสจะ fail เพราะยังไม่มีโค้ด)              │
│         ↓                                   │
│   🟢 GREEN — เขียนโค้ดให้เทสผ่าน              │
│   (เขียนเท่าที่จำเป็นเท่านั้น ไม่เกินเลย)      │
│         ↓                                   │
│   🔵 REFACTOR — ปรับปรุงโค้ดให้ดีขึ้น          │
│   (เทสยังต้องผ่านเหมือนเดิม)                  │
│         ↓                                   │
│   🔄 กลับไป RED ด้วยเทสใหม่                  │
│                                             │
└─────────────────────────────────────────────┘
```

**ข้อควรจำในแต่ละขั้น:**

| ขั้น | ทำอะไร | ห้ามทำ |
|------|--------|--------|
| 🔴 Red | คิดถึง spec → เขียนเทส → รันแล้ว fail | เขียนโค้ดก่อน |
| 🟢 Green | เขียนโค้ดให้ผ่านเทส | เขียนโค้ดเกินกว่าเทสต้องการ |
| 🔵 Refactor | ปรับโครงสร้าง ใช้ชื่อดีขึ้น ลด repetition | เพิ่มฟีเจอร์หรือเปลี่ยนพฤติกรรม |

### 4.2 ตัวอย่าง TDD ด้วย TypeScript (Vitest)

สมมติเราจะเขียนฟังก์ชัน `fizzbuzz` — รับตัวเลข คืนค่า:
- `"Fizz"` ถ้าหาร 3 ลงตัว
- `"Buzz"` ถ้าหาร 5 ลงตัว
- `"FizzBuzz"` ถ้าหารทั้ง 3 และ 5 ลงตัว
- ตัวเลขเดิม ถ้าไม่เข้าเงื่อนไขใด

#### 🔴 Step 1: เขียนเทสที่ยังไม่ผ่าน

```typescript
// fizzbuzz.test.ts
import { describe, it, expect } from "vitest";
import { fizzbuzz } from "./fizzbuzz";

describe("fizzbuzz()", () => {
  it("should return 'Fizz' for multiples of 3", () => {
    expect(fizzbuzz(3)).toBe("Fizz");
    expect(fizzbuzz(6)).toBe("Fizz");
    expect(fizzbuzz(9)).toBe("Fizz");
  });

  it("should return 'Buzz' for multiples of 5", () => {
    expect(fizzbuzz(5)).toBe("Buzz");
    expect(fizzbuzz(10)).toBe("Buzz");
  });

  it("should return 'FizzBuzz' for multiples of 3 and 5", () => {
    expect(fizzbuzz(15)).toBe("FizzBuzz");
    expect(fizzbuzz(30)).toBe("FizzBuzz");
  });

  it("should return the number for non-multiples", () => {
    expect(fizzbuzz(1)).toBe("1");
    expect(fizzbuzz(2)).toBe("2");
    expect(fizzbuzz(7)).toBe("7");
  });
});
```

```bash
# รันเทส — ต้อง fail เพราะยังไม่มีฟังก์ชัน
vitest run fizzbuzz.test.ts
# → FAIL
```

#### 🟢 Step 2: เขียนโค้ดให้ผ่านเทส

```typescript
// fizzbuzz.ts — เขียนเท่าที่จำเป็นเพื่อให้เทสผ่าน
export function fizzbuzz(n: number): string {
  if (n % 15 === 0) return "FizzBuzz";
  if (n % 3 === 0) return "Fizz";
  if (n % 5 === 0) return "Buzz";
  return String(n);
}
```

```bash
vitest run fizzbuzz.test.ts
# → PASS ✅
```

#### 🔵 Step 3: Refactor

ในเคสนี้โค้ดสั้นดีอยู่แล้ว ไม่ต้อง Refactor เพิ่ม ยกเว้นอยากเพิ่ม Type Safety หรือ Documentation

```typescript
// ถ้าอยาก refactor ให้อ่านง่ายขึ้น
const isDivisibleBy = (n: number, divisor: number): boolean => n % divisor === 0;

export function fizzbuzz(n: number): string {
  if (isDivisibleBy(n, 15)) return "FizzBuzz";
  if (isDivisibleBy(n, 3)) return "Fizz";
  if (isDivisibleBy(n, 5)) return "Buzz";
  return String(n);
}
```

```bash
vitest run fizzbuzz.test.ts
# → ยัง PASS ✅ (Refactor ต้องไม่ทำให้เทสเปลี่ยน)
```

#### 🔄 กลับไป Step 1 ด้วยเทสใหม่

เมื่อฟีเจอร์นี้สมบูรณ์ ก็เริ่มเขียนเทสสำหรับความต้องการถัดไป เช่น "รับค่าเป็น string ได้" หรือ "throw error เมื่อรับค่าติดลบ"

### 4.3 ตัวอย่าง TDD ด้วย Python (pytest)

ฟังก์ชันเดียวกันกับ FizzBuzz แต่เขียนด้วย Python

#### 🔴 Step 1: เขียนเทส

```python
# test_fizzbuzz.py
import pytest
from fizzbuzz import fizzbuzz

class TestFizzBuzz:
    def test_return_fizz_for_multiples_of_three(self):
        assert fizzbuzz(3) == "Fizz"
        assert fizzbuzz(6) == "Fizz"
        assert fizzbuzz(9) == "Fizz"

    def test_return_buzz_for_multiples_of_five(self):
        assert fizzbuzz(5) == "Buzz"
        assert fizzbuzz(10) == "Buzz"

    def test_return_fizzbuzz_for_multiples_of_three_and_five(self):
        assert fizzbuzz(15) == "FizzBuzz"
        assert fizzbuzz(30) == "FizzBuzz"

    def test_return_number_as_string_for_non_multiples(self):
        assert fizzbuzz(1) == "1"
        assert fizzbuzz(2) == "2"
        assert fizzbuzz(7) == "7"
```

```bash
pytest test_fizzbuzz.py -v
# → FAIL ❌
```

#### 🟢 Step 2: เขียนโค้ด

```python
# fizzbuzz.py
def fizzbuzz(n: int) -> str:
    if n % 15 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)
```

```bash
pytest test_fizzbuzz.py -v
# → PASS ✅
```

#### 🔵 Step 3: Refactor (ถ้าต้องการ)

```python
def fizzbuzz(n: int) -> str:
    result = ""
    if n % 3 == 0:
        result += "Fizz"
    if n % 5 == 0:
        result += "Buzz"
    return result or str(n)
```

```bash
pytest test_fizzbuzz.py -v
# → PASS ✅
```

---

## 5. เครื่องมือเสริม

### TypeScript + Vitest Ecosystem

| เครื่องมือ | คำอธิบาย | คำสั่งติดตั้ง |
|-----------|----------|-------------|
| **@vitest/coverage-v8** | Coverage report (V8 engine) | `npm i -D @vitest/coverage-v8` |
| **@vitest/coverage-istanbul** | Coverage report (Istanbul) | `npm i -D @vitest/coverage-istanbul` |
| **@testing-library/react** | React component testing | `npm i -D @testing-library/react` |
| **@testing-library/vue** | Vue component testing | `npm i -D @testing-library/vue` |
| **jsdom** | DOM environment สำหรับ Vitest | `npm i -D jsdom` |

### Python + pytest Ecosystem

| เครื่องมือ | คำอธิบาย | คำสั่งติดตั้ง |
|-----------|----------|-------------|
| **pytest-cov** | Coverage report | `pip install pytest-cov` |
| **pytest-xdist** | รันเทสแบบขนาน (หลาย CPU) | `pip install pytest-xdist` |
| **pytest-mock** | Mocking ที่ใช้งานง่าย | `pip install pytest-mock` |
| **pytest-asyncio** | รองรับ async/await | `pip install pytest-asyncio` |
| **pytest-sugar** | ผลลัพธ์เทสสีสันสวยงาม | `pip install pytest-sugar` |
| **pytest-watch** | Watch mode (รันเทสอัตโนมัติเมื่อแก้ไฟล์) | `pip install pytest-watch` |

---

## Cheat Sheet ฉบับย่อ

### TypeScript (Vitest)

```bash
# ติดตั้ง
npm install -D vitest

# รันเทส (watch mode)
npx vitest

# รันเทสครั้งเดียว
npx vitest run

# รันเทสเฉพาะไฟล์
npx vitest run src/utils.test.ts

# Coverage
npx vitest run --coverage
```

### Python (pytest)

```bash
# ติดตั้ง
pip install pytest pytest-cov

# รันเทสทั้งหมด
pytest -v

# รันเทสเฉพาะไฟล์
pytest test_math.py -v

# รันเทสด้วย keyword
pytest -k "add" -v

# Coverage
pytest --cov=. --cov-report=term-missing
```

---

## แหล่งอ้างอิง

- [Vitest Documentation](https://vitest.dev/guide/)
- [pytest Documentation](https://docs.pytest.org/)
- [Test-Driven Development (TDD) — Martin Fowler](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
