import random

def estimate_pi(n_samples: int) -> float:
    inside = 0
    for _ in range(n_samples):
        x, y = random.random(), random.random()
        if x * x + y * y <= 1.0:
            inside += 1
    return 4.0 * inside / n_samples

if __name__ == "__main__":
    random.seed(0)
    for n in [1_000, 10_000, 100_000, 1_000_000]:
        print(f"n = {n:>10,}  ->  π ≈ {estimate_pi(n):.6f}")
