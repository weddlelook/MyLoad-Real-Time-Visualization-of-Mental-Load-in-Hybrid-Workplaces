import numpy as np
import matplotlib.pyplot as plt

'''
We want to build a function for normalization of CLI values. Let name the function S. S should have the following features: 
S: I --> (0,100)
I = (0, ∞)
IBase, IMax ∈ I
S(IBase) ≈ 10
S(IMax) ≈ 90
lim I -> 0 S(I) = 0
lim I -> ∞ S(I) = 100
S is degressiv (? not decided on yet)

In the following there is the function logistic function, which fulfills the required features

'''

class CognitiveLoadNormalizer:
    def __init__(self, I_base, I_max):
        """
        Initializes the normalizer with I_base and I_max.

        Parameters:
        - I_base: CLI value that maps to approximately 10 in the normalized scale.
        - I_max: CLI value that maps to approximately 90 in the normalized scale.
        """
        self.I_base = I_base
        self.I_max = I_max
        self.k, self.I_0 = self._solve_parameters()

    def _solve_parameters(self):
        """ Solves for logistic function parameters k and I_0. """
        S_base, S_max = 10, 90  # Desired output mappings
        logit_base = np.log(S_base / (100 - S_base))
        logit_max = np.log(S_max / (100 - S_max))

        k = (logit_max - logit_base) / (self.I_max - self.I_base)
        I_0 = self.I_base - logit_base / k
        return k, I_0

    def compute_score(self, I):
        """
        Computes the cognitive load score S(I) for a given I.

        Parameters:
        - I: Input CLI value.

        Returns:
        - Normalized cognitive load score in the range (0, 100).
        """
        return 100 / (1 + np.exp(-self.k * (I - self.I_0)))

    def visualize(self, I_min=0, I_max=None, num_points=100):
        """
        Plots the cognitive load score function.

        Parameters:
        - I_min: Minimum CLI value for the plot.
        - I_max: Maximum CLI value for the plot. If None, defaults to 1.5 * I_max.
        - num_points: Number of points in the plot.
        """
        if I_max is None:
            I_max = self.I_max * 1.5  # Extend a bit beyond I_max for visualization

        I_values = np.linspace(I_min, I_max, num_points)
        S_values = [self.compute_score(I) for I in I_values]

        plt.figure(figsize=(8, 5))
        plt.plot(I_values, S_values, label="Cognitive Load Score (S(I))", color='blue')
        plt.axhline(y=10, linestyle="--", color="gray", label="S(I_base) ≈ 10")
        plt.axhline(y=90, linestyle="--", color="red", label="S(I_max) ≈ 90")
        plt.axvline(x=self.I_base, linestyle="--", color="gray")
        plt.axvline(x=self.I_max, linestyle="--", color="red")
        plt.xlabel("CLI Value (I)")
        plt.ylabel("Cognitive Load Score (S)")
        plt.title("Cognitive Load Score Normalization")
        plt.legend()
        plt.grid()
        plt.show()

if __name__ == "__main__":
    I_base_example = 1.5  # Example base CLI value
    I_max_example = 4.5  # Example max CLI value

    # Create an instance of the normalizer
    normalizer = CognitiveLoadNormalizer(I_base_example, I_max_example)

    # Compute score for a test value
    I_test = 4.2
    print(f"Cognitive Load Score for I={I_test}: {normalizer.compute_score(I_test):.2f}")

    # Visualize the function
    normalizer.visualize()