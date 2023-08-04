from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import execute, Aer

# Define a simple hash function
def simple_hash(x):
    return x % 4

# Define the oracle
def oracle():
    # Create a quantum circuit
    qc = QuantumCircuit(6)  # 4 qubits for the input, 2 for the hash

    # Compute the hash function for all possible inputs
    for x in range(16):
        hash_x = simple_hash(x)
        binary_x = "{0:04b}".format(x)
        binary_hash_x = "{0:02b}".format(hash_x)

        # Apply X gates to the input qubits based on the binary representation of x
        for i in range(4):
            if binary_x[i] == '1':
                qc.x(i)

        # Apply X gates to the hash qubits based on the binary representation of hash_x
        for i in range(2):
            if binary_hash_x[i] == '1':
                qc.x(i+4)

        # Check for collision
        qc.mct(list(range(4)), 4)  # Multi-controlled Toffoli gate
        qc.mct(list(range(4, 6)), 4)

        # Uncompute the X gates
        for i in range(4):
            if binary_x[i] == '1':
                qc.x(i)
        for i in range(2):
            if binary_hash_x[i] == '1':
                qc.x(i+4)

    return qc.to_gate()

# Create a quantum circuit
qr = QuantumRegister(6)
cr = ClassicalRegister(6)
qc = QuantumCircuit(qr, cr)

# Apply the oracle
qc.append(oracle(), list(range(6)))

# Measure the qubits
qc.measure(qr, cr)

# Execute the circuit
backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1000)
result = job.result()
counts = result.get_counts(qc)
print(counts)
