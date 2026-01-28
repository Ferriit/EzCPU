ldi 100 r1 ; load 100 into r1
psh r1 ; add r1 to stack
str r1 23 ; store r1 into ram23
pshi 12 ; add 12 to stack
pshi 14 ; add 14 to stack
pshi 60 ; add 60 to stack

waiti 100 ; wait 100 cycles

pop r0 ; pop r0

waiti 100 ; wait 100 cycles

srmv ; remove top value stack