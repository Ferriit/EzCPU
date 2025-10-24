; Fibonacci sequence: compute F(10)
ldi 20 r0     ; r0 = N (10)
ldi 1  r1     ; r1 = counter (start at 1 because r3 holds F1)
ldi 0  r2     ; r2 = F(n-2) = 0
ldi 1  r3     ; r3 = F(n-1) = 1
mov r3 dbg    ; dbg = current fib (1)
ldi 1  r5     ; r5 = 1 (increment)

labl begin_loop
    mov r2 r4    ; r4 = r2        ; copy previous to temp
    add r4 r3    ; r4 = r4 + r3   ; r4 now holds sum = r2 + r3
    mov r3 r2    ; r2 = old r3    ; shift previous := current
    mov r4 r3    ; r3 = sum       ; current := sum
    add r1 r5    ; counter += 1
    mov r3 dbg   ; update dbg to show progress (optional)
    cmp r1 r0
    je end
    jmp begin_loop

labl end
    mov r3 dbg   ; ensure final result in dbg