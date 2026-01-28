import inspect
from cpu import regs, memry, stack
from opcodes import opCodes, signatures, ns
from utils import log

# --- Initialize CPU ---
OPCODES = opCodes(regs, memry, stack)

# Get valid opcode names in order
validOpCodes = [name.lower() for name, func in inspect.getmembers(opCodes, predicate=inspect.isfunction)]
validOpCodes.remove("__init__")

# Load bytecode
with open("a.bytes", "rb") as f:
    bytecode = f.read()

# Start PC at 0
regs["pc"] = format(0, '016b')


# --- Helper to decode arguments ---
def decode_arg(arg, arg_type):
    if arg_type == ns.reg:
        return list(regs.keys())[arg]  # map numeric index to register name
    elif arg_type in [ns.val, ns.mmry, ns.label]:
        return arg
    else:  # ns.zero
        return None


# --- Step one instruction ---
def stepInstruction():
    pc_int = int(regs["pc"], 2)
    if pc_int >= len(bytecode):
        OPCODES.HALTFLAG = True
        return

    # Read opcode and arguments
    opcode_index = bytecode[pc_int]
    opcode_name = validOpCodes[opcode_index].upper()
    
    # Read arguments according to signature
    argA_type, argB_type = signatures[opcode_name.lower()]
    argA = bytecode[pc_int + 2] << 8 | bytecode[pc_int + 3]   # example
    argB = bytecode[pc_int + 4] << 8 | bytecode[pc_int + 5]   # example

    # Decode arguments
    decodedA = decode_arg(argA, argA_type)
    decodedB = decode_arg(argB, argB_type)

    # Log BEFORE executing
    log(f"PC={pc_int:04X} | {opcode_name} {decodedA} {decodedB}")

    # Execute
    func = getattr(OPCODES, opcode_name)
    func(decodedA, decodedB)

    # Update PC AFTER execution
    regs["pc"] = format(pc_int + 6, '016b')  # move past opcode+args