from .simple_parse_script import QasmParser, CliffordT, QasmGenerator

filePath = "qasm_example/input_file.qasm"
parsed = QasmParser(filePath)
register = parsed.getRegister()
print(register)
gates = parsed.getGates()
print(gates)

clifford = CliffordT(filePath)
QasmGenerator(clifford.gate_instructions, clifford.register).createQasmFile()
