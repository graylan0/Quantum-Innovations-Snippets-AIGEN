# Import necessary libraries
from qiskit import QuantumCircuit, Aer, execute
import random
import numpy as np
# Set up the quantum and classical channels
qubits = 100
q_channel = QuantumCircuit(qubits, qubits)
c_channel = QuantumCircuit(qubits, qubits)

# Generate random bits for encoding
bits = [random.randint(0,1) for i in range(qubits)]

# Encode the bits using random bases
for i in range(qubits):
    if bits[i] == 0:
        q_channel.h(i)
    else:
        q_channel.rx(1.57, i)
    basis = random.randint(0,1)
    if basis == 0:
        q_channel.barrier()
        c_channel.measure(i, i)
    else:
        q_channel.cx(i, i+1)
        c_channel.measure(i, i+1)
        c_channel.measure(i+1, i)

# Execute the circuits on a simulator
simulator = Aer.get_backend('qasm_simulator')
q_result = execute(q_channel, simulator, shots=1).result()
c_result = execute(c_channel, simulator, shots=1).result()

# Retrieve the key
key = ''
for i in range(qubits):
    if c_result.get_counts().keys()[0][i] == c_result.get_counts().keys()[0][i+1]:
        key += str(bits[i])

print('Shared secret key: ' + key)

# Set up the quantum and classical channels
qubits = 100
q_channel = QuantumCircuit(qubits, qubits)
c_channel = QuantumCircuit(qubits, qubits)

# Generate random bits for encoding
bits = [random.randint(0,1) for i in range(qubits)]

# Encode the bits using random bases
for i in range(qubits):
    if bits[i] == 0:
        q_channel.h(i)
    else:
        q_channel.rx(1.57, i)
    basis = random.randint(0,1)
    if basis == 0:
        q_channel.barrier()
        c_channel.measure(i, i)
    else:
        q_channel.cx(i, i+1)
        c_channel.measure(i, i+1)
        c_channel.measure(i+1, i)

# Execute the circuits on a simulator
simulator = Aer.get_backend('qasm_simulator')
q_result = execute(q_channel, simulator, shots=1).result()
c_result = execute(c_channel, simulator, shots=1).result()

# Retrieve the key
key = ''
for i in range(qubits):
    if c_result.get_counts().keys()[0][i] == c_result.get_counts().keys()[0][i+1]:
        key += str(bits[i])

# Apply the Toeplitz matrix to the key
toeplitz = np.random.randint(0, 2, size=(qubits, qubits))
toeplitz = np.triu(toeplitz)
key = np.array([int(b) for b in key])
amplified_key = np.mod(toeplitz @ key, 2)

print('Shared secret key: ' + ''.join(str(k) for k in amplified_key))

# Set up the quantum and classical channels
qubits = 100
q_channel = QuantumCircuit(qubits, qubits)
c_channel = QuantumCircuit(qubits, qubits)

# Generate random bits for encoding
bits = [random.randint(0,1) for i in range(qubits)]

# Encode the bits using random bases
for i in range(qubits):
    if bits[i] == 0:
        q_channel.h(i)
    else:
        q_channel.rx(1.57, i)
    basis = random.randint(0,1)
    if basis == 0:
        q_channel.barrier()
        c_channel.measure(i, i)
    else:
        q_channel.cx(i, i+1)
        c_channel.measure(i, i+1)
        c_channel.measure(i+1, i)

# Execute the circuits on a simulator
simulator = Aer.get_backend('qasm_simulator')
q_result = execute(q_channel, simulator, shots=1).result()
c_result = execute(c_channel, simulator, shots=1).result()

# Retrieve the key
key = ''
for i in range(qubits):
    if c_result.get_counts().keys()[0][i] == c_result.get_counts().keys()[0][i+1]:
        key += str(bits[i])

# Apply error correction using the Cascade protocol
code_length = 7
parity_bits = int(np.ceil(np.log2(qubits)))
num_blocks = int(np.ceil(qubits/code_length))

blocks = [key[i*code_length:(i+1)*code_length] for i in range(num_blocks)]
codewords = []
for block in blocks:
    parity_check = np.zeros(parity_bits)
    for i in range(code_length):
        if block[i] == '1':
            parity_check += np.array([int(b) for b in format(i+1, '0'+str(parity_bits)+'b')])
    parity_check = np.mod(parity_check, 2)
    codeword = block + ''.join(str(p) for p in parity_check)
    codewords.append(codeword)

error_indices = [random.randint(0, code_length+parity_bits-1) for i in range(num_blocks)]
received_codewords = []
for i in range(num_blocks):
    error_codeword = list(codewords[i])
    error_codeword[error_indices[i]] = str(1 - int(error_codeword[error_indices[i]]))
    received_codewords.append(''.join(error_codeword))

final_key = ''
for codeword in received_codewords:
    parity_check = np.zeros(parity_bits)
    for i in range(code_length+parity_bits):
        if i < code_length:
            if codeword[i] == '1':
                parity_check += np.array([int(b) for b in format(i+1, '0'+str(parity_bits)+'b')])
        else:
            if codeword[i] != str(int(np.mod(parity_check, 2)[i-code_length])):
                error_indices.append(i)
                break
    else:
        final_key += codeword[:code_length]
        
# Print the final key
print('Final key:', final_key)
