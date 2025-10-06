import inspect

from cpu import regs, memry, stack
from opcodes import opCodes, signatures, ns

OPCODES = opCodes(regs, memry, stack)

validOpCodes = [name.lower() for name, func in inspect.getmembers(opCodes, predicate=inspect.isfunction)]
validOpCodes.remove("__init__")

bytecode = open("a.bytes", "rb").read()

global internal_pc
internal_pc = "0" * 16
regs["pc"] = format(0, '016b')  # start at byte 0

def readPC():
    return int(internal_pc)

def decode_arg(arg, arg_type):
    if arg_type == ns.reg:
        return list(regs.keys())[arg]
    elif arg_type in [ns.val, ns.mmry, ns.label]:
        return arg
    else:  # ns.zero
        return None

def stepInstruction():
    pc_int = int(regs["pc"], 2)

    pc_int = int(regs["pc"], 2)
    if pc_int >= len(bytecode):
        print("PC is out of bounds. Halting execution.")
        #OPCODES.HALTFLAG = True
        return

    # Read opcode and skip padding
    if not OPCODES.ExecuteRAM:
        opcode_index = bytecode[pc_int]
        pc_int += 2  # opcode + padding
        argA = int.from_bytes(bytecode[pc_int:pc_int+2], "big")
        pc_int += 2
        argB = int.from_bytes(bytecode[pc_int:pc_int+2], "big")
        pc_int += 2
    else:
        opcode_index = memry[pc_int]
        pc_int += 2
        argA = memry[pc_int] << 8 | memry[pc_int + 1]
        pc_int += 2
        argB = memry[pc_int] << 8 | memry[pc_int + 1]
        pc_int += 2

    # Decode and execute
    opcode_name = validOpCodes[opcode_index]
    argA_type, argB_type = signatures[opcode_name]
    decodedA = decode_arg(argA, argA_type)
    decodedB = decode_arg(argB, argB_type)

    # Update PC
    regs["pc"] = format(pc_int, '016b')

    func = getattr(OPCODES, opcode_name.upper())
    func(decodedA, decodedB)

    if OPCODES.VERBOSE:
        print(f"Executed {opcode_name.upper()} with args {decodedA}, {decodedB}")
        print("Debug register:", regs["dbg"], int(regs["dbg"], 2))
        print("Program Counter:", regs["pc"], int(regs["pc"], 2))
        print("---")
