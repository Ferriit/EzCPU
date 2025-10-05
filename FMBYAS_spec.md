# FMBYAS
### (Pronounced "Femboy Ass")
## Formattable Multi-architecture Based Yield ASsembly

## OPCODES:
### Register and Memory Control:
```
LDI = Load immediate into register                                  (ldi [value] [register])
MOV = Move value from register A to B                               (mov [register] [register])
LD = Load value from RAM into register                              (ld [addr] [register])
STR = Store value from register into RAM                            (str [register] [addr])
XCHG = Swaps the contents of two registers                          (xchg [register] [register])
PSH = Pushes a register value onto the stack                        (psh [register])
PSHI = Pushes an immediate value onto the stack                     (pshi [value])
POP = Pops the top-most value on the stack into the register        (pop [register])
SRMV = Removes the top-most value on the stack (stack remove)       (srmv)
SWP = Swaps the values between register and RAM                     (swp [register] [addr])
LEA = Loads the address of a value into a register                  (lea [addr] [register])
CLR = Clears the register (same as ldi 0 [register])                (clr [register])
```

### Arithmetic:
#### Everything saves in the first mentioned register
```
ADD = Add contents of registers                                     (add [register] [register])
SUB = Subtract contents of registers                                (sub [register] [register])
MUL = Multiply contents of registers                                (mul [register] [register])
DIV = Divide contents of registers                                  (div [register] [register])
INC = Increment contents of registers                               (inc [register])
DEC = Decrement contents of registers                               (dec [register])
AND = Performs a bitwise AND operation on both registers            (and [register] [register])
OR = Performs a bitwise OR operation on both registers              (or [register] [register])
NOT = Performs a bitwise NOT on one register                        (not [register])
XOR = Performs a bitwise XOR between registers                      (xor [register] [register])
SHL = Logical bitshift left                                         (shl [register] [shift])
SHR = Logical bitshift right                                        (shr [register] [shift])
RSL = Rotate bits in register left                                  (rsl [register] [shift])
RSR = Rotate bits in register right                                 (rsr [register] [shift])
```

### Flow Control:
```
LABL = Sets a label there that you can jump to                      (labl [label name])
CMP = Compares two registers. Sets the result in IMPREG             (cmp [register] [register])
JMP = Jumps to a label                                              (jmp [label name])
JE = Jumps if the CMPREG register is 000 (equal)                    (je [label name])
JNE = Jumps if the CMPREG register is 111 (not equal)               (jne [label name])
JGT = Jumps if the CMPREG register is 110 (greather than)           (jgt [label name])
JLT = Jumps if the CMPREG register is 101 (less than)               (jtl [label name])
JGE = Jumps if the CMPREG register is 010 (greather than or equal)  (jge [label name])
JLE = Jumps if the CMPREG register is 001 (less than or equal)      (jle [label name])
CALL = Calls a subroutine that saves to stack when returned         (call [label name])
RET = Returns a value from register in a subroutine                 (ret [register])
```

### Misc:
```
NOP = No-op. Doesn't do anything                                    (nop)
HLT = Halts execution until resume button is pressed                (hlt)
WAIT = Halts for the amount of cycles described by a register       (wait [register])
WAITI = Halts for a certain amount of cycles                        (waiti [value])
```