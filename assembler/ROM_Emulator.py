import inspect
import time

from cpu import regs, memry, stack
from opcodes import opCodes, signatures, ns

OPCODES = opCodes(regs, memry, stack)

validOpCodes = [name.lower() for name, func in inspect.getmembers(opCodes, predicate=inspect.isfunction)]
validOpCodes.remove("__init__")

bytecode = open("a.bytes", "rb").read()

internal_pc = "0" * 16

speed = 60 # Speed in instructions / second

def readPC():
    return int(internal_pc)

def decode_arg(arg, arg_type):
    if arg_type == ns.reg:
        return list(regs.keys())[arg]
    elif arg_type in [ns.val, ns.mmry, ns.label]:
        return arg
    else:  # ns.zero
        return None
    
while int(internal_pc, 2) < len(bytecode):
    start = time.time()

    internal_pc = regs["pc"]
    opcode_index = bytecode[int(internal_pc, 2)]
    internal_pc = bin(int(internal_pc, 2) + 1)

    argA = int.from_bytes(bytecode[int(internal_pc, 2):int(internal_pc, 2) + 2], "big")
    internal_pc = bin(int(internal_pc, 2) + 2)
    argB = int.from_bytes(bytecode[int(internal_pc, 2):int(internal_pc, 2) + 2], "big")
    internal_pc = bin(int(internal_pc, 2) + 2)
    

    internal_pc = internal_pc[2:].zfill(16)

    opcode_name = validOpCodes[opcode_index]
    argA_type, argB_type = signatures[opcode_name]

    decodedA = decode_arg(argA, argA_type)
    decodedB = decode_arg(argB, argB_type)

    regs["pc"] = internal_pc[2:].zfill(16)

    func = getattr(OPCODES, opcode_name.upper())
    func(decodedA, decodedB)

    internal_pc = regs["pc"]

    print(f"Executed {opcode_name.upper()} with args {decodedA}, {decodedB}")
    #print("Registers:", {k: regs[k] for k in list(regs.keys())[:15]})
    #print("Stack:", stack)
    print("Debug register:", regs["dbg"], int(regs["dbg"], 2))
    print("Dummy debug:", int(regs["dbg"], 2))
    print("Program Counter:", regs["pc"], int(regs["pc"], 2))

    end = time.time()
    time.sleep(1 / speed - (end - start))
    print("---")

    while OPCODES.freezecycles > 0:
        print(f"WAIT... {OPCODES.freezecycles} cycles left")
        OPCODES.freezecycles -= 1

    while OPCODES.HALTFLAG:
        user = input("Enter 'c' to continue: ")
        if user.lower() == 'c':
            OPCODES.HALTFLAG = False

print("Execution finished!")