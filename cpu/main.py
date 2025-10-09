import assembler as asm
import window as win
import os

tests_path = f"{__file__.replace('main.py', '')}..{asm.SEPARATOR}tests{asm.SEPARATOR}"
asm_files = [f for f in os.listdir(tests_path) if f.endswith(".asm")]

print("\x1b[1m", end="\0")
print("Available programs:")
for i, file in enumerate(asm_files, 1):
    print(f"{i}. {file[:-4]}")
print("\x1b[0m", end="\0")

choice = input("Choose a program: ").strip()

if choice.isdigit():
    choice = asm_files[int(choice) - 1]
else:
    if not choice.endswith(".asm"):
        choice += ".asm"

program = f"{tests_path}{choice}"

win.main(asm.assemble([program]))