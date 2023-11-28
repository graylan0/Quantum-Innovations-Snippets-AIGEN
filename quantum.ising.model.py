import pennylane as qml
from pennylane import numpy as np

def ising_model_hamiltonian(wires, h):
    """Constructs the Hamiltonian for the Quantum Ising Model.

    Args:
        wires (int): Number of qubits (spins).
        h (float): Transverse field strength.

    Returns:
        qml.Hamiltonian: The Ising Model Hamiltonian.
    """
    # Pauli Z tensor terms
    terms = [qml.PauliZ(i) @ qml.PauliZ(i + 1) for i in range(wires - 1)]
    # Transverse field terms
    terms += [h * qml.PauliX(i) for i in range(wires)]

    # Coefficients for the Hamiltonian
    coeffs = [-1] * (wires - 1) + [1] * wires

    return qml.Hamiltonian(coeffs, terms)

def quantum_ising_model(wires, h):
    """Quantum circuit for the Ising Model.

    Args:
        wires (int): Number of qubits (spins).
        h (float): Transverse field strength.

    Returns:
        array: Expectation value of the Hamiltonian.
    """
    dev = qml.device('default.qubit', wires=wires)

    @qml.qnode(dev)
    def circuit():
        # Prepare an initial state
        for i in range(wires):
            qml.Hadamard(wires=i)
        # Apply the Ising Model Hamiltonian
        H = ising_model_hamiltonian(wires, h)
        return qml.expval(H)

    return circuit()

# Parameters
num_wires = 4  # Number of spins
h_field = 1.0  # Transverse field strength

# Run the simulation
ising_result = quantum_ising_model(num_wires, h_field)
print("Quantum Ising Model Result:", ising_result)
