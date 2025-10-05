import sys
import os
import re
from cpu import regs, memry, stack
from opcodes import opCodes, signatures
import inspect

class logTypes:
    INFO = 0
    WARNING = 1
    ERROR = 2


SEPARATOR = "\\" if os.name == "nt" else "/"


def log(type: logTypes, error: str, message):
    Prefixes = ["\x1b[1;94mI", "\x1b[1;93mW", "\x1b[1;91mE"]
    print(f"{Prefixes[type]}({error})\x1b[39m: \x1b[0m{message}")

OPCODES = opCodes(regs, memry, stack)


def assemble(args: list[str]):
    try:
        filepath = os.path.join(os.getcwd(), args[0])
        oldCode = open(filepath).read().lower()

    except IndexError:
        log(logTypes.ERROR, "SH001", "Missing file name")
        cleanup()
    except FileNotFoundError:
        log(logTypes.ERROR, "FS002", f"File not found: {args[0]}")
        cleanup()

    code = []

    for line in oldCode.splitlines():
        line = re.sub(r";.*", "", line)
        line = line.strip()
        line = re.sub(r"\s{2,}", " ", line)
        if line:
            code.append(line)

    return(parseAssembly(code))


def parseAssembly(code: list[str]):
    byteCode = b""
    validOpCodes = [name.lower() for name, func in inspect.getmembers(opCodes, predicate=inspect.isfunction)]
    validOpCodes.pop(validOpCodes.index("__init__"))
    print(list(regs.keys()))
    
    for line in code:
        lineArgs = line.split(" ")
        opCode = lineArgs[0].lower()
        args = lineArgs[1:]

        if opCode in validOpCodes:
            byteCode += bytes([validOpCodes.index(opCode)])
            argA, argB = signatures[opCode]
            match argA:
                case 0:
                    byteCode += b"\x00\x00"
                case 1:
                    byteCode += bytes([])
            
            match argB:
                case 0:
                    byteCode += b"\x00\x00"
                case 1:
                    byteCode += bytes([])
        else:
            log(logTypes.ERROR, "AS001", f"Unknown opcode: {opCode}")
            cleanup()

    return byteCode

def cleanup():
    sys.exit() 


def main():
    print(assemble(sys.argv[1:]))


if __name__ == "__main__":
    main()
