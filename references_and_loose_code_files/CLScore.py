import matplotlib.pyplot as plt

baseCLI = 30
maxCLI = 100

def calculate_kennzahl_adjusted(measured_load, base_load, max_load):
    kennzahl = 10 + ((measured_load - base_load) / (max_load - base_load)) * 80

    return max(0, min(kennzahl, 100))

def calculate_kennzahl(measured_load, base_load, max_load):
    kennzahl = ((measured_load - base_load) / (max_load - base_load)) * 100

    return max(0, min(kennzahl, 100))


i_values = list(range(baseCLI - 30, maxCLI + 30, 5))
kennzahl_values_adjusted = [calculate_kennzahl_adjusted(i, baseCLI, maxCLI) for i in i_values]
kennzahl_values = [calculate_kennzahl(i, baseCLI, maxCLI) for i in i_values]


plt.figure(figsize=(10, 6))
plt.plot(i_values, kennzahl_values_adjusted, marker='o', linestyle='--', label='Kennzahl (Adjusted)')
plt.plot(i_values, kennzahl_values, marker='s', linestyle='-', label='Kennzahl (normal)')
plt.title('Measured Load vs Kennzahl (Comparison)', fontsize=14)
plt.xlabel('Measured Load (i)', fontsize=12)
plt.ylabel('Kennzahl', fontsize=12)
plt.grid(True)
plt.legend()
plt.show()


