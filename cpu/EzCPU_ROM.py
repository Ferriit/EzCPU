import inspect
from cpu import regs, memry, stack
from opcodes import opCodes, signatures, ns
from utils import log

OPCODES = opCodes(regs, memry, stack)

validOpCodes = [name.lower() for name, func in inspect.getmembers(opCodes, predicate=inspect.isfunction)]
validOpCodes.remove("__init__")

with open("a.bytes", "rb") as f:
    bytecode = f.read()

regs["pc"] = format(0, '016b')

def decode_arg(arg, arg_type):
    if arg_type == ns.reg:
        return list(regs.keys())[arg] 
    elif arg_type in [ns.val, ns.mmry, ns.label]:
        return arg
    else:  
        return None

def stepInstruction():
    pc_int = int(regs["pc"], 2)
    if pc_int >= len(bytecode):
        OPCODES.HALTFLAG = True
        return

    opcode_index = bytecode[pc_int]
    opcode_name = validOpCodes[opcode_index].upper()
    
    argA_type, argB_type = signatures[opcode_name.lower()]
    argA = bytecode[pc_int + 2] << 8 | bytecode[pc_int + 3]   
    argB = bytecode[pc_int + 4] << 8 | bytecode[pc_int + 5] 

    decodedA = decode_arg(argA, argA_type)
    decodedB = decode_arg(argB, argB_type)

    log(f"PC={pc_int:04X} | {opcode_name} {decodedA} {decodedB}")

    func = getattr(OPCODES, opcode_name)
    func(decodedA, decodedB)

    regs["pc"] = format(pc_int + 6, '016b')