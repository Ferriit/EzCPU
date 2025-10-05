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
    "jmp": (ns.val, ns.zero),
    "je": (ns.val, ns.zero),
    "jne": (ns.val, ns.zero),
    "jgt": (ns.val, ns.zero),
    "jge": (ns.val, ns.zero),
    "jlt": (ns.val, ns.zero),
    "jle": (ns.val, ns.zero),
    "call": (ns.val, ns.zero),
    "ret": (ns.reg, ns.zero),

    "nop": (ns.zero, ns.zero),
    "hlt": (ns.zero, ns.zero),
    "waiti": (ns.val, ns.zero),
    "wait": (ns.reg, ns.zero)
}

class opCodes:
    def __init__(self, regs, memry, stack):
        self.regs = regs
        self.memry = memry
        self.stack = stack

### Helpers?
    def _get_int(self, reg):
        return int(self.regs[reg], 2)

    def _set_reg(self, reg, value):
        self.regs[reg] = format(value & 0xFFFF, '016b')

    ### Register and Memory Control
    def LDI(self, value: int, reg: str):
        self._set_reg(reg, value)

    def MOV(self, src: str, dest: str):
        self.regs[dest] = self.regs[src]

    def LD(self, address: int, reg: str):
        self.regs[reg] = format(self.memry[address] & 0xFFFF, '016b')

    def STR(self, reg: str, address: int):
        self.memry[address] = self._get_int(reg)

    def XCHG(self, regA: str, regB: str):
        self.regs[regA], self.regs[regB] = self.regs[regB], self.regs[regA]

    def PSH(self, reg: str):
        self.stack.append(self.regs[reg])

    def PSHI(self, value: int):
        self.stack.append(format(value & 0xFFFF, '016b'))

    def POP(self, reg: str):
        if self.stack:
            self.regs[reg] = self.stack.pop()
        else:
            self.regs[reg] = "0" * 16

    def SRMV(self):
        if self.stack:
            self.stack.pop()

    def SWP(self, regA: str, regB: str):
        self.regs[regA], self.regs[regB] = self.regs[regB], self.regs[regA]

    def LEA(self, address: int, reg: str):
        self._set_reg(reg, address)

    def CLR(self, reg: str):
        self.regs[reg] = "0" * 16

    ### Arithmetic
    def ADD(self, regA: str, regB: str):
        self._set_reg(regA, self._get_int(regA) + self._get_int(regB))

    def SUB(self, regA: str, regB: str):
        self._set_reg(regA, self._get_int(regA) - self._get_int(regB))

    def MUL(self, regA: str, regB: str):
        self._set_reg(regA, self._get_int(regA) * self._get_int(regB))

    def DIV(self, regA: str, regB: str):
        b = self._get_int(regB)
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        self._set_reg(regA, self._get_int(regA) // b)

    def INC(self, reg: str):
        self._set_reg(reg, self._get_int(reg) + 1)

    def DEC(self, reg: str):
        self._set_reg(reg, self._get_int(reg) - 1)

    def AND(self, regA: str, regB: str):
        self._set_reg(regA, self._get_int(regA) & self._get_int(regB))

    def OR(self, regA: str, regB: str):
        self._set_reg(regA, self._get_int(regA) | self._get_int(regB))

    def NOT(self, reg: str):
        self._set_reg(reg, ~self._get_int(reg))

    def XOR(self, regA: str, regB: str):
        self._set_reg(regA, self._get_int(regA) ^ self._get_int(regB))

    def SHL(self, reg: str):
        self._set_reg(reg, self._get_int(reg) << 1)

    def SHR(self, reg: str):
        self._set_reg(reg, self._get_int(reg) >> 1)

    def RSL(self, reg: str):
        val = self._get_int(reg)
        self._set_reg(reg, ((val << 1) | (val >> 15)) & 0xFFFF)

    def RSR(self, reg: str):
        val = self._get_int(reg)
        self._set_reg(reg, ((val >> 1) | (val << 15)) & 0xFFFF)

    ### Flow Control
    def LABL(self, label: str):
        pass

    def CMP(self, regA: str, regB: str):
        a = self._get_int(regA)
        b = self._get_int(regB)
        if a == b:
            self.regs["cmpreg"] = "000"
        if a > b:
            self.regs["cmpreg"] = "110"
        if a < b:
            self.regs["cmpreg"] = "101"
        if a >= b:
            self.regs["cmpreg"] = "010"
        if a <= b:
            self.regs["cmpreg"] = "001"
        if a != b:
            self.regs["cmpreg"][0] = "1"


    def JMP(self, programAddress: str):
        pass

    def JE(self, programAddress: str):
        pass

    def JNE(self, programAddress: str):
        pass

    def JGT(self, programAddress: str):
        pass

    def JLT(self, programAddress: str):
        pass

    def JGE(self, programAddress: str):
        pass

    def JLE(self, programAddress: str):
        pass

    def CALL(self, programAddress: str):
        pass

    def RET(self, reg: str):
        pass

    ### Misc
    def NOP(self):
        pass

    def HLT(self):
        pass

    def WAITI(self, reg: str):
        pass

    def WAIT(self, cycles: int):
        pass