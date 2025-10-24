; Loop test
ldi 10 r0
ldi 0 r1
ldi 1 r2

labl begin_loop
    waiti 10
    inc r1
    cmp r1 r0
    je end
    jmp begin_loop

labl end
    ldi 65535 dbg