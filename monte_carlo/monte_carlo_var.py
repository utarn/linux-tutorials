import random

def simulate_portfolio(initial, mu, sigma, horizon, n_sims):
    final_values = []
    for _ in range(n_sims):
        value = initial
        for _ in range(horizon):
            r = random.gauss(mu, sigma)
            value *= (1.0 + r)
        final_values.append(value)
    return final_values

if __name__ == "__main__":
    random.seed(42)
    sims = simulate_portfolio(1_000_000.0, 0.0005, 0.01, 30, 50_000)
    losses = [1_000_000.0 - v for v in sims]
    losses_sorted = sorted(losses)
    var_95 = losses_sorted[int(0.95 * len(losses_sorted))]
    print(f"มูลค่าพอร์ตเฉลี่ยหลัง 30 วัน: {sum(sims)/len(sims):,.2f} บาท")
    print(f"Value at Risk (95%): {var_95:,.2f} บาท")
    print(f"  แปลว่า: มีโอกาส 5% ที่จะขาดทุนเกิน {var_95:,.2f} บาทใน 30 วัน")
