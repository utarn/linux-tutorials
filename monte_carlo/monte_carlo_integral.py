import random

def mc_integrate(f, a: float, b: float, n: int) -> float:
    total = 0.0
    for _ in range(n):
        x = a + (b - a) * random.random()
        total += f(x)
    return (b - a) * total / n

if __name__ == "__main__":
    random.seed(1)
    f = lambda x: x ** 2
    result = mc_integrate(f, 0.0, 1.0, 100_000)
    print(f"∫₀¹ x² dx ≈ {result:.6f}  (ค่าจริง = 0.333333)")
