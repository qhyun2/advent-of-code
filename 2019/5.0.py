tape = list(map(int, open("5.in").read().strip().split(",")))

tape.append(0)
tape.append(0)
tape.append(0)

ip = 0

def lookup(i, mode):
    
    if mode == 0:
        return tape[i]
    elif mode == 1:
        return i

while True:
    
    instruction = tape[ip]

    opcode = instruction % 100
    mode_num = instruction // 100
    modes = []
    
    while mode_num > 0:
        modes.append(mode_num % 10)
        mode_num = mode_num // 10
        
    modes.append(0)
    modes.append(0)
    modes.append(0)
    modes.append(0)
        
    # params
    none = [99]
    single = [3, 4]
    triple = [1, 2]
    
    increment = 0
    
    a = b = c = 0
    
    ta = tape[ip+1]
    tb = tape[ip+2]
    tc = tape[ip+3]

    
    if opcode in single:
        a = lookup(tape[ip+1], modes[0])
        increment = 2
    if opcode in triple:
        a = lookup(tape[ip+1], modes[0])
        b = lookup(tape[ip+2], modes[1])
        c = lookup(tape[ip+3], modes[2])
        increment = 4

    # print("opcode:", opcode)
    # print("tape:", tape)
    # print("modes:", modes)
    # print("a:", a, "b:", b, "c:", c)
    
    if modes[2] == 1:
        print("writing is abs???")
    
    # add
    if opcode == 1:
        tape[tc] = a + b
    # multiply
    elif opcode == 2:
        tape[tc] = a * b
    # input
    elif opcode == 3:
        tape[ta] = int(input())
    # output    
    elif opcode == 4:
        print(a)
    # halt    
    elif opcode == 99:
        print("halt")
        break

    ip += increment
    
    