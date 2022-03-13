class QasmParser:
    """
    Class for getting and parsing a qasm file input and 
    formatting it into a format which can run in python (i.e. python dictionaries).
    """
    def __init__(self, filePath):
        self.file_str = self.getFileAsString(filePath)
        self.register = self.getRegister()
        self.gate_instructions = self.getGates()
    
    def getFileAsString(self, filePath):
        file = open(filePath, "r") 
        fileStr = file.read().replace("\n", " ")
        file.close()
        return fileStr

    def _getFileAsInstructionList(self, file_str):
        return [instruction.strip() + ';\n' for instruction in file_str.split('; ')]

    def getRegister(self):
        instructionList = self._getFileAsInstructionList(self.file_str)
        register_name = ''
        qubits_in_register = 0
        for instruction in instructionList:
            if instruction.find('qubit')!=-1:
                temp_index = instruction.find('[')
                qubits_in_register = instruction[temp_index+1]
                register_name = instruction.partition('] ')[2][:-2]
    
        if register_name == '':
            raise ValueError('No quantum register specified or not using v3 of QASM. QASM syntax not supported by this parser.')

        #Note this does not work well if multiple quantum registers in a QASM file. Only works for a single quantum register declaration in QASM
        return {
            "register_name": register_name, 
            "qubits_in_register": qubits_in_register
        }
    
    def getGates(self):
        gates = []
        instructionList = self._getFileAsInstructionList(self.file_str)
        # position = 0
        for instruction in instructionList:
            """If statement checks if instruction is a gate operator"""
            if instruction.find(self.register["register_name"] + '[')!=-1:
                gate_instruction_list = instruction.split(' ')
                [gate, *operands] = gate_instruction_list
                qubits_operates_on = [int(op[op.index(']')-1]) for op in operands]
                gates.append({
                    'gate': gate,
                    'qubits_operates_on': qubits_operates_on,
                    'qasm': instruction
                    # 'position': position        
                })
                # position += 1
        return gates


class CliffordT(QasmParser):
    """
    Class for decomposing non-Clifford+T gates into a sequence 
    of Clifford+T gates.
    """
    def __init__(self, filePath):
        QasmParser.__init__(self, filePath)
        self.updateGateInstructions() #will update self.gate_instructions inherited from QasmParser

    def _updateGate(self, gate_dict):
        if(gate_dict["gate"]=="ccx"):
            a=gate_dict["qubits_operates_on"][0]
            b=gate_dict["qubits_operates_on"][1]
            c=gate_dict["qubits_operates_on"][2]
            register_name = self.register["register_name"]
            qasmCliffordTRepOfCcx = f"""
                t {register_name}[{a}];
                cx {register_name}[{a}],{register_name}[{b}];
                tdg {register_name}[{b}];
                cx {register_name}[{a}],{register_name}[{b}];
                t {register_name}[{b}];
                h {register_name}[{c}];
                cx {register_name}[{b}],{register_name}[{c}];
                tdg {register_name}[{c}];
                cx {register_name}[{a}],{register_name}[{c}];
                t {register_name}[{c}];
                cx {register_name}[{b}],{register_name}[{c}];
                tdg {register_name}[{c}];
                cx {register_name}[{a}],{register_name}[{c}];
                t {register_name}[{c}];
                h {register_name}[{c}];
                """
            gate_dict.update({
                "gate": "cliffordT ccx",
                "qasm": qasmCliffordTRepOfCcx
            })
        # elif(gate_dict["gate"].find("rz")!=-1):
        #     pass
        # else:
        #     return gate_dict
    
    def updateGateInstructions(self):
        return [self._updateGate(gate_dict) for gate_dict in self.gate_instructions]
            
class QasmGenerator: #inherit from (QasmParser)?
    """
    Class to create and output a Qasm file from a list of individual qasm instructions.
    """
    def __init__(self, gate_instructions, register):
        self.register = register
        self.gate_instructions = gate_instructions
        self.qasm_str = ''
        self.createQasmStr()

    def createQasmStr(self):
        self.qasm_str = ' '.join([instruction_dict["qasm"] for instruction_dict in self.gate_instructions])

    def createQasmFile(self):
        filePath = "qasm_example/output_qasm_cliffordt.qasm"
        f = open(filePath, "w")
        f.write("OPENQASM 3.0;\n")
        f.close()
        f = open(filePath, "a")
        f.write('include "stdgates.inc";\n')
        register_name = self.register["register_name"]
        register_size = self.register["qubits_in_register"]
        f.write(f"qubit[{register_size}] {register_name};\n")
        f.write(self.qasm_str)
        f.close()

class ReduceCliffordTQasm:
    pass