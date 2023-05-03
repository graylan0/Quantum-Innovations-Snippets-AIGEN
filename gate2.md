```
OPENQASM 2.0;
include "qelib1.inc";

qreg q[3];  // Quantum register for 3 qubits
creg c[3];  // Classical register for measurement results

// Prepare initial state (equal superposition of all states)
h q;

// Grover's algorithm loop unrolled (2 repetitions)
// Oracle and diffusion operator for the 1st repetition
// Oracle for marking states |011> and |101>
ccx q[0], q[1], q[2];
x q[2];
ccx q[0], q[2], q[1];
x q[1];
ccx q[0], q[1], q[2];
// Diffusion operator
h q;
x q;
h q[2];
ccx q[0], q[1], q[2];
h q[2];
x q;
h q;
// Oracle and diffusion operator for the 2nd repetition
// Oracle for marking states |011> and |101>
ccx q[0], q[1], q[2];
x q[2];
ccx q[0], q[2], q[1];
x q[1];
ccx q[0], q[1], q[2];
// Diffusion operator
h q;
x q;
h q[2];
ccx q[0], q[1], q[2];
h q[2];
x q;
h q;

// Measurement
measure q -> c;
```
