; Fibonacci sequence: compute F(N)
ldi 20 r0     ; r0 = N
ldi 0  r1     ; r1 = counter (start at 0)
ldi 0  r2     ; r2 = F(n-2) = 0
ldi 1  r3     ; r3 = F(n-1) = 1
mov r2 dbg    ; dbg = F(0) = 0

ldi 1  r5     ; r5 = 1 (increment)

labl begin_loop
    cmp r1 r0
    je end

    mov r2 r4    ; r4 = r2
    add r4 r3    ; r4 = r2 + r3
    mov r3 r2    ; r2 = old r3
    mov r4 r3    ; r3 = sum
    add r1 r5    ; counter += 1
    mov r3 dbg   ; dbg = current fib
    jmp begin_loop

labl end
    mov r3 dbg   ; final fib in dbg
