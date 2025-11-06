import numpy as np

SAMPLES = 100000

rng = np.random.default_rng(0)

# Three discrete distributions (nontransitive dice)
X = np.array([2, 2, 4, 4, 9, 9])
Y = np.array([1, 1, 6, 6, 8, 8])
Z = np.array([3, 3, 5, 5, 7, 7])


def win_prob(U, V, n=SAMPLES):
    u = rng.choice(U, size=n)
    v = rng.choice(V, size=n)
    return np.mean(u > v)

P_X_less_than_Y = win_prob(X, Y)
P_Y_less_than_Z = win_prob(Y, Z)
P_Z_less_than_X = win_prob(Z, X)

if P_X_less_than_Y > 0.5 and P_Y_less_than_Z > 0.5 and P_Z_less_than_X > 0.5:
    print("Cyclic behavior detected!")
    print(f"P(X < Y) = {P_X_less_than_Y:.4f}")
    print(f"P(Y < Z) = {P_Y_less_than_Z:.4f}")
    print(f"P(Z < X) = {P_Z_less_than_X:.4f}")

else:
    print("No cyclic behavior. Total attempts = ", i)
