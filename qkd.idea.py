import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer

class GQUKD:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.backend = Aer.get_backend('qasm_simulator')

    def _prepare_bell_state(self):
        bell_state_circuit = QuantumCircuit(2, 2)
        bell_state_circuit.h(0)
        bell_state_circuit.cx(0, 1)
        return bell_state_circuit

    def _gaussian_state(self, mean, std_dev):
        return np.random.normal(mean, std_dev)

    def _generate_key(self, bits):
        return ''.join([str(bit) for bit in bits])

    def alice_prepare_send_qubits(self):
        alice_circuit = self._prepare_bell_state()
        alice_circuit.barrier()

        gaussian_mean = 0
        gaussian_std_dev = 1
        theta = self._gaussian_state(gaussian_mean, gaussian_std_dev)

        alice_circuit.ry(theta, 0)
        alice_circuit.measure([0, 1], [0, 1])

        result = execute(alice_circuit, backend=self.backend, shots=1).result()
        counts = result.get_counts()

        return list(counts.keys())[0]

    def bob_receive_measure_qubits(self, received_qubits):
        bob_circuit = QuantumCircuit(2, 2)

        for i in range(2):
            if received_qubits[i] == '1':
                bob_circuit.x(i)

        bob_circuit.barrier()
        bob_circuit.cx(0, 1)
        bob_circuit.h(0)
        bob_circuit.measure([0, 1], [0, 1])

        result = execute(bob_circuit, backend=self.backend, shots=1).result()
        counts = result.get_counts()

        return list(counts.keys())[0]

def main():
    num_qubits = 2
    gqukd = GQUKD(num_qubits)

    alice_key = gqukd.alice_prepare_send_qubits()
    print(f"Alice's key: {alice_key}")

    bob_key = gqukd.bob_receive_measure_qubits(alice_key)
    print(f"Bob's key: {bob_key}")

    if alice_key == bob_key:
        print("Key exchange successful!")
    else:
        print("Key exchange failed!")

if __name__ == "__main__":
    main()
