ldi 3 r0
waiti 60000

mov r0 dbg

jmp _start

labl fmby
    ldi 1 dbg

    ldi 1 r1
    sub r1 dbg
    
    ldi 4 r0
    ret r0

labl _start
    call fmby
    pop dbg