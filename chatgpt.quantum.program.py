from qiskit import QuantumCircuit, Aer, execute
import matplotlib.pyplot as plt
import numpy as np

# Number of steps in the quantum walk
steps = 10

# Create a quantum circuit with 2 qubits (one for the coin and one for the position)
qc = QuantumCircuit(2, 1)

# Initialize the coin to a superposition of |0> and |1>
qc.h(0)

# Perform the quantum walk
for _ in range(steps):
    # Apply the shift operator
    qc.cx(0, 1)
    # Apply the coin operator
    qc.h(0)

# Measure the position qubit
qc.measure([1], [0])

# Simulate the circuit
simulator = Aer.get_backend('qasm_simulator')
result = execute(qc, simulator, shots=1000).result()
counts = result.get_counts()

# Plot the results
plt.bar([int(k, 2) for k in counts.keys()], counts.values())
plt.xlabel('Position')
plt.ylabel('Frequency')
plt.show()
