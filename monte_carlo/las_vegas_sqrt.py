import random

def las_vegas_sqrt(target, tolerance=1e-6):
    """หารากที่สองด้วย Las Vegas: สุ่มเดา แล้วขยับตามเครื่องหมาย จนลู่เข้า"""
    # เริ่มจากการเดาสุ่มในช่วง [0, target+1]
    guess = random.uniform(0.0, max(target, 1.0))
    step = max(target, 1.0) / 2.0  # ขนาดก้าวเริ่มต้น
    while abs(guess * guess - target) > tolerance:
        if guess * guess < target:
            guess += step
        else:
            guess -= step
        step /= 2.0  # ลดขนาดก้าวทีละครึ่ง (bisection-like) เพื่อลู่เข้าอย่างรวดเร็ว
    return guess

if __name__ == "__main__":
    random.seed(0)
    val = 25.0
    print(f"√{val} ≈ {las_vegas_sqrt(val):.6f}  (ค่าจริง = 5.000000)")
