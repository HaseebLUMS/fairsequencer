import numpy as np
from scipy.stats import pareto
import matplotlib.pyplot as plt

SAMPLES = 100_000
rng = np.random.default_rng(0)


# Below values were carefully curated (by sweeping across several values)
# so that we can find distributions that lead to intransitivity
alpha_X, xm_X = 0.55, 3.924063914281433
alpha_Y, xm_Y = 1.42933819627166, 8.163551603278592
alpha_Z, xm_Z = 4.427463341623717, 11.079292190642231


i = 0
while True:
    X = pareto(b=alpha_X, scale=xm_X).rvs(SAMPLES, random_state=rng)
    Y = pareto(b=alpha_Y, scale=xm_Y).rvs(SAMPLES, random_state=rng)
    Z = pareto(b=alpha_Z, scale=xm_Z).rvs(SAMPLES, random_state=rng)

    # Pairwise probabilities
    P_X_less_than_Y = np.mean(X < Y)
    P_Y_less_than_Z = np.mean(Y < Z)
    P_Z_less_than_X = np.mean(Z < X)

    if P_X_less_than_Y > 0.5 and P_Y_less_than_Z > 0.5 and P_Z_less_than_X > 0.5:
        print("Cyclic behavior detected!")
        print(f"P(X < Y) = {P_X_less_than_Y:.4f}")
        print(f"P(Y < Z) = {P_Y_less_than_Z:.4f}")
        print(f"P(Z < X) = {P_Z_less_than_X:.4f}")
        break
    else:
        if i % 100 == 0:
            print("No cyclic behavior. Total attempts =", i)
    i += 1


# Visualizing the distributions

plt.figure(figsize=(7,5))
bins = np.logspace(np.log10(min(xm_X, xm_Y, xm_Z)),
                   np.log10(np.percentile(np.concatenate([X,Y,Z]), 99.5)), 120)
plt.hist(X, bins=bins, density=True, alpha=0.4, label="X")
plt.hist(Y, bins=bins, density=True, alpha=0.4, label="Y")
plt.hist(Z, bins=bins, density=True, alpha=0.4, label="Z")
plt.xscale("log")
plt.xlabel("Value (log scale)")
plt.ylabel("Density")
plt.title("Pareto-distributed X, Y, Z (PDF view; log-x)")
plt.legend()
plt.show()
