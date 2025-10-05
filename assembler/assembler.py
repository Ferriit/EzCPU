import sys
import os

class logTypes:
    INFO = 0
    WARNING = 1
    ERROR = 2


SEPARATOR = "\\" if os.name == "nt" else "/"


def log(type: logTypes, error: str, message):
    Prefixes = ["\x1b[1;94mI", "\x1b[1;93mW", "\x1b[1;91mE"]
    print(f"{Prefixes[type]}({error})\x1b[39m: \x1b[0m{message}")


def assemble(args: list[str]):
    try:
        code = open(os.getcwd() + SEPARATOR + args[0]).read()
    except IndexError:
        log(logTypes.ERROR, "SH001", "Missing file name")
        cleanup()
    print(code)


def cleanup():
    sys.exit()


def main():
    assemble(sys.argv[1:])

if __name__ == "__main__":
    main()