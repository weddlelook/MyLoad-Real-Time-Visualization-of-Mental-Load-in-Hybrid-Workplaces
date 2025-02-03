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

In the following there is the function Hill function, which fulfills the required features

'''


# Parameters for base and max values
I_base = 2
I_max = 4

# Parameters for Hill fuction. 
# These parameters come from the fact that we want to build the graph mainly between 10 and 90
n = np.log(81) / np.log(I_max / I_base)   # ln(81) / ln(4/2)
C = I_base * (9)**(1/n)

# I aralığı
I = np.linspace(0, 10, 1000)

# Defining the Hill-Function 
def S_hill(I):
    return 100 * (I**n) / (I**n + C**n)

# middle value
I_target = 3
S_hill_value = S_hill(I_target)


plt.figure(figsize=(8, 6))
plt.plot(I, S_hill(I), 'b', label='Hill Function')


plt.scatter(I_target, S_hill_value, color='red', label=f'S({I_target}) = {S_hill_value:.2f}', zorder=5)
plt.axvline(I_base, color='gray', linestyle='--', label='$I_{base} = 2$')
plt.axvline(I_max, color='orange', linestyle='--', label='$I_{max} = 4$')
plt.axhline(10, color='green', linestyle='--', label='10')
plt.axhline(90, color='red', linestyle='--', label='90')


plt.xlabel('I')
plt.ylabel('S(I)')
plt.title('Hill Function graph')
plt.legend()
plt.grid(True)


plt.show()