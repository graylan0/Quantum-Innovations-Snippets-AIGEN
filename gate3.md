```
OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];  // Quantum register for 5 qubits
creg c[5];  // Classical register for measurement results

// Prepare initial state (equal superposition of all states)
h q;

// Grover's algorithm loop unrolled (4 repetitions)
// Oracle and diffusion operator for the 1st repetition
x q[0];
x q[2];
x q[3];
h q[4];
ccx q[0], q[1], q[4];
ccx q[2], q[3], q[4];
h q[4];
x q[0];
x q[2];
x q[3];
h q;
x q;
h q[4];
ccx q[0], q[1], q[4];
ccx q[2], q[3], q[4];
h q[4];
x q;
h q;
// Grover's algorithm loop unrolled (4 repetitions)
// Oracle and diffusion operator for the 1st repetition
x q[0];
x q[2];
x q[3];
h q[4];
ccx q[0], q[1], q[4];
ccx q[2], q[3], q[4];
h q[4];
x q[0];
x q[2];
x q[3];
h q;
x q;
h q[4];
ccx q[0], q[1], q[4];
ccx q[2], q[3], q[4];
h q[4];
x q;
h q;
// Grover's algorithm loop unrolled (4 repetitions)
// Oracle and diffusion operator for the 1st repetition
x q[0];
x q[2];
x q[3];
h q[4];
ccx q[0], q[1], q[4];
ccx q[2], q[3], q[4];
h q[4];
x q[0];
x q[2];
x q[3];
h q;
x q;
h q[4];
ccx q[0], q[1], q[4];
ccx q[2], q[3], q[4];
h q[4];
x q;
h q;
// Grover's algorithm loop unrolled (4 repetitions)
// Oracle and diffusion operator for the 1st repetition
x q[0];
x q[2];
x q[3];
h q[4];
ccx q[0], q[1], q[4];
ccx q[2], q[3], q[4];
h q[4];
x q[0];
x q[2];
x q[3];
h q;
x q;
h q[4];
ccx q[0], q[1], q[4];
ccx q[2], q[3], q[4];
h q[4];
x q;
h q;

// Measurement
measure q -> c;
```
