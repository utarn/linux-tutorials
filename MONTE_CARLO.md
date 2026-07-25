# การจำลองมอนติคาร์โล (Monte Carlo Simulation) และวิธีการที่เกี่ยวข้อง

เอกสารสอนการจำลองมอนติคาร์โล (Monte Carlo Simulation) ด้วย Python พร้อมตัวอย่างโค้ดที่รันได้จริง ออกแบบสำหรับนักวิทยาศาสตร์และผู้เริ่มต้นเรียนรู้การคำนวณเชิงตัวเลข (numerical computing) บน Linux

> 📂 ไฟล์โค้ด Python ทั้งหมดเก็บอยู่ในโฟลเดอร์ `monte_carlo/` — สามารถรันได้ทันทีด้วย `python3 monte_carlo/<file>.py`

---

## 1. มอนติคาร์โลคืออะไร?

**มอนติคาร์โล (Monte Carlo)** เป็นวิธีการคำนวณที่ใช้ **การสุ่ม (random sampling)** ซ้ำ ๆ หลาย ๆ ครั้ง เพื่อประมาณค่าผลลัพธ์ที่ยากต่อการคำนวณด้วยสูตรตามตัว (analytical solution) เช่น การหาค่า π, การประเมินความเสี่ยง, การหาค่าคาดหมายของอินทิกรัลที่ซับซ้อน

แนวคิดหลัก: ยิ่งสุ่มหลายครั้ง ผลลัพธ์จะยิ่งลู่เข้าสู่ค่าความจริง (Law of Large Numbers)

---

## 2. ตัวอย่างที่ 1: ประมาณค่า π ด้วยวิธีเข็มทิศแบบสุ่ม (Random Dart)

ขว้างจุดสุ่มลงในสี่เหลี่ยมจตุรัส 1×1 แล้วนับว่ากี่จุดที่ตกอยู่ในวงกลมรัศมี 1 ส่วน 4 พื้นที่วงกลม ÷ พื้นที่สี่เหลี่ยม = π/4

```python
# monte_carlo_pi.py
import random

def estimate_pi(n_samples: int) -> float:
    inside = 0
    for _ in range(n_samples):
        x, y = random.random(), random.random()  # สุ่มพิกัดใน [0,1) x [0,1)
        if x * x + y * y <= 1.0:                  # อยู่ในวงกลมรัศมี 1
            inside += 1
    # สัดส่วนที่ตกในวงกลม × 4 = π
    return 4.0 * inside / n_samples

if __name__ == "__main__":
    for n in [1_000, 10_000, 100_000, 1_000_000]:
        print(f"n = {n:>10,}  ->  π ≈ {estimate_pi(n):.6f}")
```

ผลลัพธ์เมื่อรัน (จะลู่เข้าค่า π = 3.14159... เมื่อ n เพิ่มขึ้น):

```
n =      1,000  ->  π ≈ 3.128000
n =     10,000  ->  π ≈ 3.143200
n =    100,000  ->  π ≈ 3.148400
n =  1,000,000  ->  π ≈ 3.142332
```

---

## 3. ตัวอย่างที่ 2: ประมาณอินทิกรัลด้วยมอนติคาร์โล (Monte Carlo Integration)

อินทิกรัล $\int_0^1 x^2 \, dx$ คำนวณตามตัวได้ = 1/3 ≈ 0.3333 ใช้มอนติคาร์โลโดยเฉลี่ยค่าฟังก์ชันที่จุดสุ่ม:

```python
# monte_carlo_integral.py
import random

def mc_integrate(f, a: float, b: float, n: int) -> float:
    """ประมาณค่า ∫ f(x) dx บนช่วง [a, b] ด้วยการสุ่ม n จุด"""
    total = 0.0
    for _ in range(n):
        x = a + (b - a) * random.random()
        total += f(x)
    return (b - a) * total / n

if __name__ == "__main__":
    f = lambda x: x ** 2
    result = mc_integrate(f, 0.0, 1.0, 100_000)
    print(f"∫₀¹ x² dx ≈ {result:.6f}  (ค่าจริง = 0.333333)")
```

ผลลัพธ์:

```
∫₀¹ x² dx ≈ 0.333675  (ค่าจริง = 0.333333)
```

---

## 4. ตัวอย่างที่ 3: ความเสี่ยงแบบพอร์ตการลงทุน (Portfolio Risk / Value at Risk)

จำลองผลตอบแทนของพอร์ตการลงทุนด้วยการสุ่มจากการแจกแจงปกติ (Normal distribution) แล้วหา **Value at Risk (VaR)** ที่ระดับความมั่นใจ 95%:

```python
# monte_carlo_var.py
import random

def simulate_portfolio(initial: float, mu: float, sigma: float,
                       horizon: int, n_sims: int) -> list[float]:
    """จำลองมูลค่าพอร์ตหลังผ่านไป horizon วัน จำนวน n_sims ครั้ง"""
    final_values = []
    for _ in range(n_sims):
        value = initial
        for _ in range(horizon):
            # ผลตอบแทนรายวันสุ่มตามการแจกแจงปกติ ~ N(mu, sigma)
            r = random.gauss(mu, sigma)
            value *= (1.0 + r)
        final_values.append(value)
    return final_values

if __name__ == "__main__":
    random.seed(42)
    sims = simulate_portfolio(
        initial=1_000_000.0,   # เงินลงทุนเริ่มต้น 1 ล้านบาท
        mu=0.0005,             # ผลตอบแทนเฉลี่ยรายวัน ~ 0.05%
        sigma=0.01,            # ความผันผวนรายวัน 1%
        horizon=30,            # ระยะเวลา 30 วัน
        n_sims=50_000,         # จำลอง 50,000 สถานการณ์
    )

    losses = [1_000_000.0 - v for v in sims]   # ขาดทุน = เงินตั้งต้น - มูลค่าสุดท้าย
    losses_sorted = sorted(losses)
    var_95 = losses_sorted[int(0.95 * len(losses_sorted))]

    print(f"มูลค่าพอร์ตเฉลี่ยหลัง 30 วัน: {sum(sims)/len(sims):,.2f} บาท")
    print(f"Value at Risk (95%): {var_95:,.2f} บาท")
    print(f"  แปลว่า: มีโอกาส 5% ที่จะขาดทุนเกิน {var_95:,.2f} บาทใน 30 วัน")
```

ผลลัพธ์:

```
มูลค่าพอร์ตเฉลี่ยหลัง 30 วัน: 1,014,781.31 บาท
Value at Risk (95%): 74,347.70 บาท
  แปลว่า: มีโอกาส 5% ที่จะขาดทุนเกิน 74,347.70 บาทใน 30 วัน
```

---

## 5. ตัวอย่างที่ 4: วิธีลาซเวกัส (Las Vegas Algorithm) — สุ่มจนถูก

ต่างจากมอนติคาร์โลตรงที่ Las Vegas **รับประกันคำตอบที่ถูกต้อง** แต่เวลาที่ใช้เป็นตัวแปรสุ่ม ตัวอย่าง: การหา square root ด้วยวิธีสุ่มแบบเดา

```python
# las_vegas_sqrt.py
import random

def las_vegas_sqrt(target: float, tolerance: float = 1e-6) -> float:
    """หารากที่สองด้วย Las Vegas: สุ่มเดา แล้วขยับตามเครื่องหมาย จนลู่เข้า"""
    # เริ่มจากการเดาสุ่มในช่วง [0, target+1]
    guess = random.uniform(0.0, max(target, 1.0))
    step = max(target, 1.0) / 2.0           # ขนาดก้าวเริ่มต้น
    while abs(guess * guess - target) > tolerance:
        if guess * guess < target:
            guess += step
        else:
            guess -= step
        step /= 2.0                          # ลดขนาดก้าวทีละครึ่ง เพื่อลู่เข้าอย่างรวดเร็ว
    return guess

if __name__ == "__main__":
    random.seed(0)
    val = 25.0
    print(f"√{val} ≈ {las_vegas_sqrt(val):.6f}  (ค่าจริง = 5.000000)")
```

ผลลัพธ์:

```
√25.0 ≈ 5.000000  (ค่าจริง = 5.000000)
```

(ใช้เวลาเพียงเสี้ยววินาที เพราะลดขนาดก้าวทีละครึ่ง — ลู่เข้าแบบ exponential)

---

## 6. ตัวอย่างที่ 5: การสุ่มตัวอย่างแบบมาร์คอฟ (Markov Chain Monte Carlo — MCMC)

MCMC ใช้สำหรับสุ่มตัวอย่างจากการแจกแจงที่ยากต่อการสุ่มโดยตรง เช่น การหาค่าที่น่าจะเป็นของพารามิเตอร์ ที่นี่ใช้ **Metropolis-Hastings** เพื่อสุ่มตัวอย่างจากการแจกแจงปกติมาตรฐาน $N(0,1)$:

```python
# mcmc_metropolis.py
import random
import math

def target_pdf(x: float) -> float:
    """การแจกแจงเป้าหมาย: ปกติมาตรฐาน N(0, 1)"""
    return math.exp(-x * x / 2.0) / math.sqrt(2.0 * math.pi)

def metropolis(n_samples: int, proposal_std: float = 1.0) -> list[float]:
    samples = []
    x = 0.0  # ค่าเริ่มต้น
    for _ in range(n_samples):
        x_new = x + random.gauss(0, proposal_std)     # เสนอค่าใหม่
        # อัตราส่วนความน่าจะเป็น (acceptance ratio)
        ratio = target_pdf(x_new) / target_pdf(x)
        if random.random() < ratio:
            x = x_new                                 # ยอมรับค่าใหม่
        samples.append(x)                             # (ถ้าไม่ยอมรับ ใช้ค่าเดิม)
    return samples

if __name__ == "__main__":
    random.seed(123)
    samples = metropolis(100_000)
    # ทิ้งช่วง burn-in แรก 10,000 ตัวอย่าง
    post_burn = samples[10_000:]
    mean = sum(post_burn) / len(post_burn)
    var = sum((s - mean) ** 2 for s in post_burn) / len(post_burn)
    print(f"ค่าเฉลี่ย ≈ {mean:.4f}  (ค่าจริง = 0.0000)")
    print(f"ความแปรปรวน ≈ {var:.4f}  (ค่าจริง = 1.0000)")
```

ผลลัพธ์:

```
ค่าเฉลี่ย ≈ -0.0044  (ค่าจริง = 0.0000)
ความแปรปรวน ≈ 0.9983  (ค่าจริง = 1.0000)
```

---

## 7. วิธีการที่เกี่ยวข้องอื่น ๆ (เปรียบเทียบ)

| วิธี | ลักษณะเด่น | รับประกันคำตอบถูก? |
|------|-----------|-------------------|
| **Monte Carlo** | ใช้การสุ่มเพื่อประมาณค่า ผลลัพธ์ใกล้เคียงแต่มีความคลาดเคลื่อน (approximate) | ไม่ (แต่ลดความคลาดเคลื่อนได้ด้วยการเพิ่มตัวอย่าง) |
| **Las Vegas** | สุ่มเพื่อเลือกเส้นทาง แต่คำตอบที่ได้ถูกต้องเสมอ เวลาเป็นตัวแปรสุ่ม | ใช่ |
| **MCMC** | สุ่มตัวอย่างตามลูกโซ่มาร์คอฟ เหมาะกับการแจกแจงซับซ้อนหลายมิติ | ไม่ (แต่ลู่เข้าการแจกแจงเป้าหมาย) |
| **Quasi-Monte Carlo** | ใช้ลำดับเลขกึ่งสุ่ม (low-discrepancy) แทนการสุ่มจริง ลดความคลาดเคลื่อนเร็วกว่า | ไม่ (แต่ลู่เข้าเร็วกว่ามอนติคาร์โลธรรมดา) |

---

## 8. ผลลัพธ์การรันจริง (Executed Output)

ด้านล่างคือผลลัพธ์จริงจากการรันสคริปต์ทั้งหมดบนเครื่องนี้ (`python3` บน macOS/Linux):

```bash
# รันไฟล์ตัวอย่างทั้งหมด (จากไดเรกทอรีรากของโปรเจกต์)
python3 monte_carlo/monte_carlo_pi.py
python3 monte_carlo/monte_carlo_integral.py
python3 monte_carlo/monte_carlo_var.py
python3 monte_carlo/las_vegas_sqrt.py
python3 monte_carlo/mcmc_metropolis.py

# หรือรันทีเดียวทั้งหมด
for f in monte_carlo/*.py; do echo "=== $f ==="; python3 "$f"; done
```

ผลลัพธ์รวมจากการรันจริงทั้ง 5 สคริปต์:

```
$ python3 monte_carlo_pi.py
n =      1,000  ->  π ≈ 3.128000
n =     10,000  ->  π ≈ 3.143200
n =    100,000  ->  π ≈ 3.148400
n =  1,000,000  ->  π ≈ 3.142332

$ python3 monte_carlo_integral.py
∫₀¹ x² dx ≈ 0.333675  (ค่าจริง = 0.333333)

$ python3 monte_carlo_var.py
มูลค่าพอร์ตเฉลี่ยหลัง 30 วัน: 1,014,781.31 บาท
Value at Risk (95%): 74,347.70 บาท
  แปลว่า: มีโอกาส 5% ที่จะขาดทุนเกิน 74,347.70 บาทใน 30 วัน

$ python3 las_vegas_sqrt.py
√25.0 ≈ 5.000000  (ค่าจริง = 5.000000)

$ python3 mcmc_metropolis.py
ค่าเฉลี่ย ≈ -0.0044  (ค่าจริง = 0.0000)
ความแปรปรวน ≈ 0.9983  (ค่าจริง = 1.0000)
```

> ✅ ทุกสคริปต์รันผ่านและให้ผลลัพธ์ใกล้เคียงค่าจริง แสดงให้เห็นว่าวิธีการสุ่มทั้ง 5 แบบทำงานได้ถูกต้อง
