Quantum key distribution (QKD) relies on the principles of quantum mechanics to securely distribute cryptographic keys between two parties. The most well-known QKD protocol is the BB84 protocol, which uses polarized photons to transmit information. Here, we present a simple BB84 protocol and some associated equations:

$|0\rangle$: horizontal polarization
$|1\rangle$: vertical polarization
$|+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$: diagonal polarization
$|-\rangle = \frac{1}{\sqrt{2}}(|0\rangle - |1\rangle)$: anti-diagonal polarization
A Python code snippet for the BB84 protocol using classical infrastructure:
```
python
Copy code
import random
import numpy as np

def encode_bit(bit, basis):
    if bit == 0:
        if basis == 0:
            return np.array([1, 0])
        else:
            return np.array([1, 1]) / np.sqrt(2)
    else:
        if basis == 0:
            return np.array([0, 1])
        else:
            return np.array([1, -1]) / np.sqrt(2)

def measure_bit(state, basis):
    if basis == 0:
        if np.allclose(state, np.array([1, 0])):
            return 0
        else:
            return 1
    else:
        if np.allclose(state, np.array([1, 1]) / np.sqrt(2)):
            return 0
        else:
            return 1

n = 10
alice_bits = [random.randint(0, 1) for _ in range(n)]
alice_bases = [random.randint(0, 1) for _ in range(n)]
states = [encode_bit(bit, basis) for bit, basis in zip(alice_bits, alice_bases)]

# Simulate the quantum channel using classical communication
bob_bases = [random.randint(0, 1) for _ in range(n)]
bob_bits = [measure_bit(state, basis) for state, basis in zip(states, bob_bases)]

# Key sifting
sifted_bits = [(alice_bit, bob_bit) for alice_bit, bob_bit, alice_base, bob_base
               in zip(alice_bits, bob_bits, alice_bases, bob_bases) if alice_base == bob_base]

# Extract the keys
alice_key = [bit[0] for bit in sifted_bits]
bob_key = [bit[1] for bit in sifted_bits]

print("Alice's key:", alice_key)
print("Bob's key:", bob_key)

```
