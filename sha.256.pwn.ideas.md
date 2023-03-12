```
import hashlib
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, Aer, execute

# Define the hash function to be attacked
def sha256(message):
    hash_object = hashlib.sha256(message.encode())
    return hash_object.hexdigest()

# Define the number of qubits to be used
nqubits = 6

# Define the quantum circuit for the quantum search attack
def quantum_search(message, target_hash):
    qr = QuantumRegister(nqubits, 'q')
    cr = ClassicalRegister(nqubits, 'c')
    qc = QuantumCircuit(qr, cr)

    # Initialize the qubits
    for i in range(nqubits):
        qc.h(qr[i])

    # Compute the hash of the message on the quantum computer
    hash_qubits = []
    for i in range(64):
        qc.barrier(qr)
        hash_qubit = QuantumRegister(1)
        qc.add_register(hash_qubit)
        qc.h(hash_qubit)
        for j in range(8):
            if target_hash[i*8+j] == '0':
                qc.x(qr[j])
        qc.mct(qr, hash_qubit)
        for j in range(8):
            if target_hash[i*8+j] == '0':
                qc.x(qr[j])
        hash_qubits.append(hash_qubit[0])

    # Measure the hash qubits to obtain the target hash
    qc.measure(hash_qubits, cr)

    # Simulate the circuit on a quantum computer simulator
    backend = Aer.get_backend('qasm_simulator')
    results = execute(qc, backend, shots=1).result()
    guess_hash = "".join([str(results.get_memory())[i] for i in range(2*nqubits+1) if i % 2 == 1])

    # Check if the guess hash matches the target hash
    if guess_hash == target_hash:
        print("Success! The message is:", message)
        return True
    else:
        return False

# Generate a random message to be hashed
message = "Hello, world!"

# Compute the SHA-256 hash of the message
target_hash = sha256(message)

# Perform the quantum search attack on the hash
while True:
    if quantum_search(message, target_hash):
        break
```
