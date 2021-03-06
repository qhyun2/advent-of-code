import queue

class CPU():
    
    def __init__(self):
        self.tape = list(map(int, open("11.in").read().strip().split(",")))
        
        for i in range(30000):
            self.tape.append(0)

        self.ip = 0
        self.sp = 0
        self.mode = "Stopped"
        self.stdout = queue.Queue()
        self.stdin = queue.Queue()

    def lookup(self, i, mode):
        
        if mode == 0:
            return self.tape[i]
        elif mode == 1:
            return i
        elif mode == 2:
            # print(tape[sp+i])
            return self.tape[self.sp+i]
        else:
            print("Invalid mode: ", mode)
            exit()    

    def run(self):
    
        while True:
            
            instruction = self.tape[self.ip]
            
            opcode = instruction % 100
            mode_num = instruction // 100
            modes = []
            
            while mode_num > 0:
                modes.append(mode_num % 10)
                mode_num = mode_num // 10
                
            modes.append(0)
            modes.append(0)
            modes.append(0)

            # no input available
            if self.stdin.empty() and opcode == 3:
                self.mode = "Waiting on input"
                break
            
            # params
            none = [99]
            single = [3, 4, 9]
            double = [5, 6]
            triple = [1, 2, 7, 8]
            
            increment = 0
            
            a = b = c = 0
            
            ta = self.tape[self.ip+1]
            tb = self.tape[self.ip+2]
            tc = self.tape[self.ip+3]

            if opcode in none:
                pass
            if opcode in single:
                a = self.lookup(ta, modes[0])
                increment = 2
            if opcode in double:
                a = self.lookup(ta, modes[0])
                b = self.lookup(tb, modes[1])
                increment = 3
            if opcode in triple:
                a = self.lookup(ta, modes[0])
                b = self.lookup(tb, modes[1])
                c = self.lookup(tc, modes[2])
                increment = 4

            self.ip += increment

            # print("opcode:", opcode)
            # print("tape:", tape)
            # print("modes:", modes)
            # print("a:", a, "b:", b, "c:", c)
            
            if modes[0] == 2:
                ta += self.sp
            
            if modes[1] == 2:
                tb += self.sp
                
            if modes[2] == 2:
                tc += self.sp
            
            
            # add
            if opcode == 1:
                self.tape[tc] = a + b
            # multiply
            elif opcode == 2:
                self.tape[tc] = a * b
            # input
            elif opcode == 3:
                self.tape[ta] = int(self.stdin.get())
            # output
            elif opcode == 4:
                print("adding")
                self.stdout.put(a)
            # jump if true    
            elif opcode == 5:
                if not a == 0:
                    self.ip = b
                    continue
            # jump if false
            elif opcode == 6:
                if a == 0:
                    self.ip = b
                    continue
            # less than
            elif opcode == 7:
                if a < b:
                    self.tape[tc] = 1
                else:
                    self.tape[tc] = 0
            # equals
            elif opcode == 8:
                if a == b:
                    self.tape[tc] = 1
                else:
                    self.tape[tc] = 0
            elif opcode == 9:
                # print("changing sp", sp, a)
                self.sp += a
                
            # halt    
            elif opcode == 99:
                print("halt")
                self.mode = "HALT"
                break
            
cpu = CPU()
cpu.run()

x = 50
y = 50

grid = [[0 for _ in range(100)] for _ in range(100)]
grid[y][x] = 1
cdir = 0

# 0 up
# 1 right
# 2 left
# 3 down

mod = set()

while True:
    
    cpu.stdin.put(grid[y][x])
    cpu.run()
    
    if cpu.mode == "HALT":
        break
    
    assert not cpu.stdout.empty()
    colour = cpu.stdout.get()
    ndir = cpu.stdout.get()
    
    print(x, y)
    mod.add((x,y))
    grid[y][x] = colour
    
    cdir += -1 if ndir == 0 else 1
    
    cdir %= 4
    
    if cdir == 0:
        y -= 1
    elif cdir == 1:
        x += 1
    elif cdir == 2:
        y += 1
    elif cdir == 3:
        x -= 1
    
print('\n'.join([''.join(["." if cell == 0 else "#" for cell in row]) for row in grid]))
print(len(mod))