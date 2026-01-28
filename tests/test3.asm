ldi 3 r0 ; load 3 in r0
waiti 60 ; wait 60 cycles

mov r0 dbg ; move r0 to dbg

jmp _start

labl fmby
    ldi 1 dbg ; load 1 in dbg

    ldi 1 r1 ; load 1 in r1
    sub r1 dbg ; r1 - dbd into dbg
    
    ldi 4 r0 ; load 4 in r0
    ret r0 ; return value

labl _start
    call fmby ; do fmby
    pop dbg ; pop top most into stack