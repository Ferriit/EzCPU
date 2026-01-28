labl hej    ; creates a lable
ldi 12 r0   ; Load 12 into r0
ldi 6 r1    ; Load 6 into r1
add r0 r1   ; r0 + r1 into r0, operand 1 + operand 2 into operand 1
mov r0 dbg  ; Display r0 as the output
jmp hej     ; Jumps back to the lable