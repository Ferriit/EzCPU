import inspect
from cpu import regs, memry, stack
from opcodes import opCodes, signatures, ns

OPCODES = opCodes(regs, memry, stack)

validOpCodes = [name.lower() for name, func in inspect.getmembers(opCodes, predicate=inspect.isfunction)]
validOpCodes.remove("__init__")

bytecode = open("a.bytes", "rb").read()

regs["pc"] = 0

def decode_arg(arg, arg_type):
    if arg_type == ns.reg:
        return list(regs.keys())[arg]
    elif arg_type in [ns.val, ns.mmry]:
        return arg
    else:  # ns.zero
        return None
    
while regs["pc"] < len(bytecode):
    opcode_index = bytecode[regs["pc"]]
    regs["pc"] += 1

    argA = int.from_bytes(bytecode[regs["pc"]:regs["pc"]+2], "big")
    regs["pc"] += 2
    argB = int.from_bytes(bytecode[regs["pc"]:regs["pc"]+2], "big")
    regs["pc"] += 2

    opcode_name = validOpCodes[opcode_index]
    argA_type, argB_type = signatures[opcode_name]

    decodedA = decode_arg(argA, argA_type)
    decodedB = decode_arg(argB, argB_type)

    func = getattr(OPCODES, opcode_name.upper())
    func(decodedA, decodedB)

    print(f"Executed {opcode_name.upper()} with args {decodedA}, {decodedB}")
    #print("Registers:", {k: regs[k] for k in list(regs.keys())[:15]})
    #print("Stack:", stack)
    print("Debug register:", regs["dbg"], int(regs["dbg"], 2))
    print("---")

print("Execution finished!")