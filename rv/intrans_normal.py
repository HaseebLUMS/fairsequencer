import numpy as np

def sample_prob_less_than(X_params, Y_params, n=1000_000):
    """Return an empirical estimate of P(X < Y) given normal params = (mean, std)."""
    muX, stdX = X_params
    muY, stdY = Y_params
    X = np.random.normal(muX, stdX, size=n)
    Y = np.random.normal(muY, stdY, size=n)
    return np.mean(X < Y)

np.random.seed(42)

N_TRIES = 100000
found_example = False

for _ in range(N_TRIES):
    # Random means in [-5, 5], random std in [0.1, 5]
    X_params = (np.random.uniform(-5, 5), np.random.uniform(0.1, 5))
    Y_params = (np.random.uniform(-5, 5), np.random.uniform(0.1, 5))
    Z_params = (np.random.uniform(-5, 5), np.random.uniform(0.1, 5))

    pXY = sample_prob_less_than(X_params, Y_params)
    pYZ = sample_prob_less_than(Y_params, Z_params)
    pZX = sample_prob_less_than(Z_params, X_params)

    if pXY > 0.5 and pYZ > 0.5 and pZX > 0.5:
        found_example = True
        print("Intransitive triple found!")
        print(f"  X ~ N({X_params[0]:.2f}, {X_params[1]:.2f}^2)")
        print(f"  Y ~ N({Y_params[0]:.2f}, {Y_params[1]:.2f}^2)")
        print(f"  Z ~ N({Z_params[0]:.2f}, {Z_params[1]:.2f}^2)")
        print(f"  P(X < Y) = {pXY:.3f}, P(Y < Z) = {pYZ:.3f}, P(Z < X) = {pZX:.3f}")
        break

if not found_example:
    print("No intransitive triple found in this run. Try increasing N_TRIES.")

