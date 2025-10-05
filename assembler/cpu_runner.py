import inspect
from cpu import regs, memry, stack
from opcodes import opCodes, signatures, ns

OPCODES = opCodes(regs, memry, stack)
validOpCodes = [name.lower() for name, func in inspect.getmembers(opCodes, predicate=inspect.isfunction)]
validOpCodes.pop(validOpCodes.index("__init__"))