import numpy as np
from scipy.stats import expon

SAMPLES = 100000

i = 0

while 1:

    # Parameters for the exponential distributions
    lambda_X = 1.0  # Rate parameter for X
    lambda_Y = 1.5  # Rate parameter for Y
    lambda_Z = 2.0  # Rate parameter for Z

    # Generate samples from the exponential distributions
    X = expon(scale=1/lambda_X).rvs(SAMPLES)  # X ~ Exp(lambda_X)
    Y = expon(scale=1/lambda_Y).rvs(SAMPLES)  # Y ~ Exp(lambda_Y)
    Z = expon(scale=1/lambda_Z).rvs(SAMPLES)  # Z ~ Exp(lambda_Z)

    # Calculate pairwise probabilities
    P_X_less_than_Y = np.mean(X < Y)  # P(X < Y)
    P_Y_less_than_Z = np.mean(Y < Z)  # P(Y < Z)
    P_Z_less_than_X = np.mean(Z < X)  # P(Z < X)


    # Check for cyclic behavior
    if P_X_less_than_Y > 0.5 and P_Y_less_than_Z > 0.5 and P_Z_less_than_X > 0.5:
        print("Cyclic behavior detected!")
        print(f"P(X < Y) = {P_X_less_than_Y:.4f}")
        print(f"P(Y < Z) = {P_Y_less_than_Z:.4f}")
        print(f"P(Z < X) = {P_Z_less_than_X:.4f}")

        break
    else:
        if (i % 1000 == 0):
            print("No cyclic behavior. Total attempts = ", i)

    i += 1
