from qiskit import QuantumCircuit, QuantumRegister
import numpy as np

def qft(n):
    """Creates an n-qubit QFT circuit"""
    circuit = QuantumCircuit(n)
    for j in range(n):
        for k in range(j):
            circuit.cp(np.pi/float(2**(j-k)), j, k)
        circuit.h(j)
    return circuit

# Create and draw a 4-qubit QFT circuit
circuit = qft(4)
print(circuit)
