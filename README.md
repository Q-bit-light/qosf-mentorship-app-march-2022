# QOSF app Mar 2022 - Task 4

This code transpiles a qasm3 file with simple gates into a qasm3 file with gates in the Clifford+T group, and reduces the number of gates used. 

### Run locally

```
git clone <url>
python3 -m venv venv
source venv/bin/activate
pip install requirements.txt
python3 -m qasm_transpiler
```
You will see the qasm output at `/qasm_example/output_qasm_clifford.qasm`
which converts the file `/qasm_example/input_file.qasm` (the example provided in the task) into gates of the Clifford+T group.

### Contributors

Vatsal Kanoria
Harshita Sharma 
Shreya Khatkar

### References

We used the following references for decomposing the gates into the Clifford+T basis.

### Implementation Notes

Currently the parser is written in a naive way, making assumptions 
about the nature of the QASM3 file (i.e. that only a single quantum 
register is defined and the file contains only predefined gate 
operations from the standard gate library). With more time we would use 
the AST (abstract syntax tree) created by ANTLR4 with the grammer file 
provided in the OPENQASM3 github repository to parse the file properly
and create a transpiler, which we had initially attempted 
but abandoned due to time constraints. 

We also did not have time to complete the algorithm for 
converting `R_z(pi/5)` into gates of the Clifford+T group but
investigated various papers and algorithms including the Solovay-Kitaev 
algorithm to express a unitary as an approximation of a circuit built from
the generators `<H, S, CNOT, T>` of the Clifford+T group.
