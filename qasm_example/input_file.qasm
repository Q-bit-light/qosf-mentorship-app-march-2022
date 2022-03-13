OPENQASM 3.0; 
include "stdgates.inc";

qubit[4] quantum_reg;
reset quantum_reg;

h quantum_reg[0];
h quantum_reg[2];
y quantum_reg[1];
cx quantum_reg[0], quantum_reg[1];
ccx quantum_reg[0], quantum_reg[1], quantum_reg[2];
z quantum_reg[1];
rz(pi/5) quantum_reg[2];

