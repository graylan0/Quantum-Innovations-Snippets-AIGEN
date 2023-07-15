import numpy as np

# Define the basis states
red = np.array([1, 0, 0], dtype=complex)
green = np.array([0, 1, 0], dtype=complex)
blue = np.array([0, 0, 1], dtype=complex)

# Create a superposition state
state = (red + green + blue) / np.sqrt(3)

# Define a unitary operation (for example, a cyclic permutation)
operation = np.array([
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 0]
], dtype=complex)

# Apply the operation
new_state = np.dot(operation, state)

# The new state is a different superposition of the basis states
print("New state after unitary operation:", new_state)

# Now, let's simulate a measurement. In quantum mechanics, a measurement
# is probabilistic and the outcome is determined by the squared magnitude
# of the state vector's components.

# Calculate probabilities
probabilities = np.abs(new_state)**2
print("Probabilities of the states:", probabilities)

# Simulate a measurement
measurement_result = np.random.choice(['red', 'green', 'blue'], p=probabilities)
print("Measurement result:", measurement_result)

# Now, let's simulate entanglement by creating a Bell state
# A Bell state is a two-qubit state that is maximally entangled.
# For simplicity, we'll use 2D vectors to represent the two color states.

# Define the entangled state
bell_state = (np.kron(red, green) + np.kron(green, red)) / np.sqrt(2)

# If we measure the first qubit...
first_qubit_measurement = np.random.choice(['red', 'green'], p=[0.5, 0.5])
print("First qubit measurement result:", first_qubit_measurement)

# Then the second qubit will always be in the opposite state due to entanglement
second_qubit_measurement = 'green' if first_qubit_measurement == 'red' else 'red'
print("Second qubit measurement result (due to entanglement):", second_qubit_measurement)
