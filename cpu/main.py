import assembler as asm
import window as win
#Are ya winnin' son?
import os
import time

print("\x1b[1m", end="\0")
os.system(f"ls {__file__.replace("main.py", "")}..{asm.SEPARATOR}tests{asm.SEPARATOR}")
print("\x1b[0m", end="\0")
program = f"{__file__.replace("main.py", "")}..{asm.SEPARATOR}tests{asm.SEPARATOR}{input('Choose a program from the list: ')}"

win.main(asm.assemble([program]))