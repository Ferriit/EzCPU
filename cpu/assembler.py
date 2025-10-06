import sys
import os
import re
import subprocess
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
    print(args)
    try:
        if not args[0].startswith(SEPARATOR):
            filepath = os.path.join(os.getcwd(), args[0])
        else:
            filepath = args[0]
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
    labels = {"start": 0}

    byteCode = b""
    validOpCodes = [name.lower() for name, func in inspect.getmembers(opCodes, predicate=inspect.isfunction)]
    validOpCodes.pop(validOpCodes.index("__init__"))
    print(list(regs.keys()))
    
    i = 0

    for line in code:
        lineArgs = line.split(" ")
        opCode = lineArgs[0].lower()
        args = lineArgs[1:]

        if opCode == "labl":
                labels[args[0]] = i
        
        i += 6

    for line in code:
        lineArgs = line.split(" ")
        opCode = lineArgs[0].lower()
        args = lineArgs[1:]

        if opCode in validOpCodes:
            if opCode != "labl":
                byteCode += bytes([validOpCodes.index(opCode)]) + b"\x00"
                argA, argB = signatures[opCode]
                print(bytes([validOpCodes.index(opCode)]), opCode, args)
                match argA:
                    case 0:
                        byteCode += b"\x00\x00"
                    case 1:
                        byteCode += int(args[0]).to_bytes(2, byteorder="big")
                    case 2:
                        byteCode += list(regs.keys()).index(args[0]).to_bytes(2, byteorder="big")
                    case 3:
                        byteCode += int(args[0]).to_bytes(2, byteorder="big")
                    case 4:
                        byteCode += int(labels[args[0]]).to_bytes(2, byteorder="big")

                match argB:
                    case 0:
                        byteCode += b"\x00\x00"
                    case 1:
                        byteCode += int(args[1]).to_bytes(2, byteorder="big")
                    case 2:
                        byteCode += list(regs.keys()).index(args[1]).to_bytes(2, byteorder="big")
                    case 3:
                        byteCode += int(args[1]).to_bytes(2, byteorder="big")
                    case 4:
                        byteCode += int(labels[args[1]]).to_bytes(2, byteorder="big")

        else:
            log(logTypes.ERROR, "AS001", f"Unknown opcode: {opCode}")
            cleanup()

    return byteCode

def cleanup():
    sys.exit() 


def main(args):
    bytecode = assemble(args)
    open("a.bytes", "wb").write(bytecode)
    print("Assembly complete. Bytecode written to a.bytes")
    #print(bytecode.decode(encoding="utf-8", errors="strict"))
    print(bytecode)
    print(int.from_bytes(bytecode, byteorder="big"))

    #try:
    #    subprocess.run([sys.executable, "main.py"])
    #except FileNotFoundError:
    #    log(logTypes.ERROR, "EX002", "main.py not found")

if __name__ == "__main__":
    main(sys.argv[1:])
