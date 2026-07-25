import random
import math

def target_pdf(x):
    return math.exp(-x * x / 2.0) / math.sqrt(2.0 * math.pi)

def metropolis(n_samples, proposal_std=1.0):
    samples = []
    x = 0.0
    for _ in range(n_samples):
        x_new = x + random.gauss(0, proposal_std)
        ratio = target_pdf(x_new) / target_pdf(x)
        if random.random() < ratio:
            x = x_new
        samples.append(x)
    return samples

if __name__ == "__main__":
    random.seed(123)
    samples = metropolis(100_000)
    post_burn = samples[10_000:]
    mean = sum(post_burn) / len(post_burn)
    var = sum((s - mean) ** 2 for s in post_burn) / len(post_burn)
    print(f"ค่าเฉลี่ย ≈ {mean:.4f}  (ค่าจริง = 0.0000)")
    print(f"ความแปรปรวน ≈ {var:.4f}  (ค่าจริง = 1.0000)")
