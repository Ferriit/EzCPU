class ns:
    # number signatures
    zero = 0
    val = 1
    reg = 2
    mmry = 3
    label = 4


signatures = {
    "ldi": (ns.val, ns.reg),
    "mov": (ns.reg, ns.reg),
    "ld": (ns.mmry, ns.reg),
    "str": (ns.reg, ns.mmry),
    "xchg": (ns.reg, ns.reg),
    "psh": (ns.reg, ns.zero),
    "pshi": (ns.val, ns.zero),
    "pop": (ns.reg, ns.zero),
    "srmv": (ns.zero, ns.zero),
    "swp": (ns.reg, ns.reg),
    "lea": (ns.mmry, ns.reg),
    "clr": (ns.reg, ns.zero),

    "add": (ns.reg, ns.reg),
    "sub": (ns.reg, ns.reg),
    "mul": (ns.reg, ns.reg),
    "div": (ns.reg, ns.reg),
    "inc": (ns.reg, ns.zero),
    "dec": (ns.reg, ns.zero),
    "and": (ns.reg, ns.reg),
    "or": (ns.reg, ns.reg),
    "not": (ns.reg, ns.zero),
    "xor": (ns.reg, ns.reg),
    "shl": (ns.reg, ns.zero),
    "shr": (ns.reg, ns.zero),
    "rsl": (ns.reg, ns.zero),
    "rsr": (ns.reg, ns.zero),

    "labl": (ns.zero, ns.zero),
    "cmp": (ns.reg, ns.reg),
    "jmp": (ns.label, ns.zero),
    "je": (ns.label, ns.zero),
    "jne": (ns.label, ns.zero),
    "jgt": (ns.label, ns.zero),
    "jge": (ns.label, ns.zero),
    "jlt": (ns.label, ns.zero),
    "jle": (ns.label, ns.zero),
    "jfr": (ns.reg, ns.zero),
    "call": (ns.label, ns.zero),
    "ret": (ns.reg, ns.zero),

    "nop": (ns.zero, ns.zero),
    "hlt": (ns.zero, ns.zero),
    "waiti": (ns.val, ns.zero),
    "wait": (ns.reg, ns.zero),
    "cont": (ns.zero, ns.zero)
}

class opCodes:
    def __init__(self, regs, memry, stack):
        self.regs = regs
        self.memry = memry
        self.stack = stack
        self.HALTFLAG = False
        self.freezecycles = 0
        self.ExecuteRAM = False
        self.VERBOSE = False

        self.a = 0

### Helpers?
    def _get_int(self, reg):
        return int(self.regs[reg], 2)

    def _set_reg(self, reg, value):
        self.regs[reg] = format(value & 0xFFFF, '016b')

    ### Register and Memory Control
    def LDI(self, value: int, reg: str, *args):
        self.regs[reg] = format(value, '016b')

    def MOV(self, src: str, dest: str, *args):
        self.regs[dest] = format(int(self.regs[src], 2), '016b')

    def LD(self, address: int, reg: str, *args):
        self.regs[reg] = format(self.memry[address] & 0xFFFF, '016b')

    def STR(self, reg: str, address: int, *args):
        self.memry[address] = int(self.regs[reg], 2) % (2 ** 16)

    def XCHG(self, regA: str, regB: str, *args):
        tempA = int(self.regs[regA], 2)
        tempB = int(self.regs[regB], 2)
        self.regs[regA] = format(tempB, '016b')
        self.regs[regB] = format(tempA, '016b')

    def PSH(self, reg: str, *args):
        self.stack.append(format(int(self.regs[reg], 2), '016b'))

    def PSHI(self, value: int, *args):
        self.stack.append(format(value & 0xFFFF, '016b'))

    def POP(self, reg: str, *args):
        if self.stack:
            self.regs[reg] = format(int(self.stack.pop(), 2), '016b')
        else:
            self.regs[reg] = "0" * 16

    def SRMV(self, *args):
        if self.stack:
            self.stack.pop()

    def SWP(self, regA: str, regB: str, *args):
        tempA = int(self.regs[regA], 2)
        tempB = int(self.regs[regB], 2)
        self.regs[regA] = format(tempB, '016b')
        self.regs[regB] = format(tempA, '016b')

    def LEA(self, address: int, reg: str, *args):
        self.regs[reg] = format(address, '016b')

    def CLR(self, reg: str, *args):
        self.regs[reg] = "0" * 16

    ### Arithmetic
    def ADD(self, regA: str, regB: str, *args):
        result = int(self.regs[regA], 2) + int(self.regs[regB], 2)
        self.regs[regA] = format(result & 0xFFFF, '016b')

    def SUB(self, regA: str, regB: str, *args):
        result = int(self.regs[regA], 2) - int(self.regs[regB], 2)
        self.regs[regA] = format(result & 0xFFFF, '016b')

    def MUL(self, regA: str, regB: str, *args):
        result = int(self.regs[regA], 2) * int(self.regs[regB], 2)
        self.regs[regA] = format(result & 0xFFFF, '016b')

    def DIV(self, regA: str, regB: str, *args):
        b = int(self.regs[regB], 2)
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        result = int(self.regs[regA], 2) // b
        self.regs[regA] = format(result & 0xFFFF, '016b')

    def INC(self, reg: str, *args):
        result = int(self.regs[reg], 2) + 1
        self.regs[reg] = format(result & 0xFFFF, '016b')

    def DEC(self, reg: str, *args):
        result = int(self.regs[reg], 2) - 1
        self.regs[reg] = format(result & 0xFFFF, '016b')

    def AND(self, regA: str, regB: str, *args):
        result = int(self.regs[regA], 2) & int(self.regs[regB], 2)
        self.regs[regA] = format(result & 0xFFFF, '016b')

    def OR(self, regA: str, regB: str, *args):
        result = int(self.regs[regA], 2) | int(self.regs[regB], 2)
        self.regs[regA] = format(result & 0xFFFF, '016b')

    def NOT(self, reg: str, *args):
        result = ~int(self.regs[reg], 2)
        self.regs[reg] = format(result & 0xFFFF, '016b')

    def XOR(self, regA: str, regB: str, *args):
        result = int(self.regs[regA], 2) ^ int(self.regs[regB], 2)
        self.regs[regA] = format(result & 0xFFFF, '016b')

    def SHL(self, reg: str, *args):
        result = int(self.regs[reg], 2) << 1
        self.regs[reg] = format(result & 0xFFFF, '016b')

    def SHR(self, reg: str, *args):
        result = int(self.regs[reg], 2) >> 1
        self.regs[reg] = format(result & 0xFFFF, '016b')

    def RSL(self, reg: str, *args):
        val = int(self.regs[reg], 2)
        result = ((val << 1) | (val >> 15)) & 0xFFFF
        self.regs[reg] = format(result, '016b')

    def RSR(self, reg: str, *args):
        val = int(self.regs[reg], 2)
        result = ((val >> 1) | (val << 15)) & 0xFFFF
        self.regs[reg] = format(result, '016b')

    ### Flow Control
    def LABL(self, label: str, *args):
        pass

    def CMP(self, regA: str, regB: str, *args):
        a = int(self.regs[regA], 2)
        b = int(self.regs[regB], 2)
        # You may want to refactor this logic for clarity and correctness
        cmpreg = ["0", "0", "0"]
        if a > b:
            cmpreg = ["0", "1", "0"]
        elif a < b:
            cmpreg = ["0", "0", "1"]
        elif a == b:
            cmpreg = ["1", "0", "0"]
        self.regs["cmpreg"] = "".join(cmpreg)

    def JMP(self, programAddress, *args):
        self.regs["pc"] = format(programAddress - self.a, '016b')

    def JE(self, programAddress, *args):
        if self.regs["cmpreg"][0] == "1":
            self.regs["pc"] = format(programAddress - self.a, '016b')

    def JNE(self, programAddress, *args):
        if self.regs["cmpreg"][0] == "0":
            self.regs["pc"] = format(programAddress - self.a, '016b')

    def JGT(self, programAddress, *args):
        if self.regs["cmpreg"] == "010":
            self.regs["pc"] = format(programAddress - self.a, '016b')

    def JLT(self, programAddress, *args):
        if self.regs["cmpreg"] == "001":
            self.regs["pc"] = format(programAddress - self.a, '016b')

    def JGE(self, programAddress, *args):
        if self.regs["cmpreg"] == "110":
            self.regs["pc"] = format(programAddress - self.a, '016b')

    def JLE(self, programAddress, *args):
        if self.regs["cmpreg"] == "101":
            self.regs["pc"] = format(programAddress - self.a, '016b')

    def JFR(self, register, *args):
        self.regs["pc"] = format(int(self.regs[register], 2), '016b')

    def CALL(self, programAddress, *args):
        self.regs["funcret"] = self.regs["pc"]
        self.regs["pc"] = format(programAddress, '016b')

    def RET(self, reg: str, *args):
        self.stack.append(self.regs[reg])
        self.regs["pc"] = self.regs["funcret"]

    ### Misc
    def NOP(self, *args):
        pass

    def HLT(self, *args):
        self.HALTFLAG = True

    def WAITI(self, cycles: str, *args):
        self.freezecycles = cycles

    def WAIT(self, reg: int, *args):
        self.freezecycles = int(self.regs[reg], 2)
    
    def CONT(self, *args):
        self.regs["pc"] = format(0, '016b')
        self.ExecuteRAM = True