ldi 0 r0
ldi 100 r9

labl loop
   mov r0 dbg
   waiti 1000

   inc r0
   cmp r0 r9
   jgt reset
   jmp loop

labl reset 
   ldi 0 r0
   jmp loop