class Instruction:
    signal_points = list(range(20,221,40))

    def check_signal(self,env):
        if env.cycle in self.signal_points:
            print(f" ** signal ({env.cycle}) : {env.cycle * env.X}")
            env.signal.append(env.cycle * env.X) 

class Noop(Instruction):

    def __init__(self):
        pass

    def enter(self,env):
        pass
        # print("enter noop")

    def execute(self,env):
        # print(f"({env.cycle}) execute NOOP")
        env.cycle += 1
        self.check_signal(env)
        env.change_instruction() 

    # def exit(self,env):n
        # print("exit noop")

class Add(Instruction):
    def __init__(self, val):
        self.value = val
    
    def enter(self,env):
        env.cycle_target = env.cycle + 2
        # print(f"Add enter cycle target = {env.cycle_target}")

    def execute(self,env):
        # print(f"({env.cycle}) execute ADD..value: {self.value}")
        env.cycle += 1

        if env.cycle == env.cycle_target:
            env.X += self.value
            env.cycle_target = 0
            env.change_instruction()

        self.check_signal(env)
    # def exit(self,env):
    #     print("Add exit")
    #     env.cycle_target = 0
    #     env.X += self.value


class Environment: 
    def __init__(self, program):
        self.program = self.program_generator(program)
        self.cycle = 1
        self.cycle_target = 1
        self.X = 1
        self.done = False
        self.signal = []
        self.mask = 1
        for i in range(40):
            self.mask |= 2**i
        
        self.draw_bit_mask(self.mask)

        self.instruction = next(self.program)
        self.instruction.enter(self)
        # print(self)

    def run(self):
        if self.instruction is None:
            self.done = True
        
        if not self.done:
            self.instruction.execute(self)
            
            if self.cycle % 20 == 0:
                print(self)
        else:
            raise Exception("program halt")

    def change_instruction(self):
        if not self.done:
            # self.instruction.exit(self)
            self._next_instruction()

            if self.instruction is None:
                self.done = True
            else:
                self.instruction.enter(self)

    def _next_instruction(self):
        self.instruction = next(self.program,None)

    def program_generator(iself, program):
        for str in program:
            str = str.rstrip()

            parse = str.split(" ")
            instr = parse[0]

            if instr == 'noop':
                yield Noop()
            else:
                yield Add(int(parse[1]))

    def __str__(self):
        return f"cycle: {self.cycle} X:{self.X}"

    def draw_sprite(self):
        pass

    def draw_bit_mask(self, b):
        print(format(b,'040b'))

    def _get_cycle_bits(self):
        cycle_bit_pos = int(map_range(self.cycle,1,40,39,0))
        print(cycle_bit_pos)
        cycle_bit_pos = 2 ** cycle_bit_pos
        print(bin(cycle_bit_pos))
        print(bin(self.mask))
        # cycle_bit_pos = bin(self.mask & cycle_bit_pos)
        return cycle_bit_pos 

    def _get_register_bits(self):
        registers = [ int(map_range(x, 0,39,39,0)) for x in range(self.X-1,self.X+2) if x >-1  and x < 40]

        bits = 0

        for r in registers:
            bits |= 2**r

        return bits


# ENV = {'program':None, 'instruction':None, 'cycle':1,'cycle_target':0, 'X':0}


def map_range(val,from_min,from_max,to_min,to_max):
    n = norm(val,from_min,from_max)
    return lerp(to_min,to_max,n)

def norm(val,range_min,range_max):
    return (val - range_min) / (range_max - range_min)

def lerp(range_min, range_max,t):
    return (1.0 - t) * range_min + t * range_max

# def next_instruction(env):
#     # print(env)
#     env['instruction'].exit(env)
#     env['instruction'] = next(env['program'])

#     if env['instruction'] is None:
#         print('done')
#     else:
#         env['instruction'].enter(env)



if __name__=='__main__':
    import sys

    dev_instr= ['noop', 'addx 3', 'addx -5' ]

    testing = '-t' in sys.argv

    filename = 'test.txt' if testing else 'input.txt'

    e = Environment(['noop'] * 4)
    bits = e._get_register_bits()
    e.draw_bit_mask(bits)
    print()


    for i in range(3):
        bits = e._get_cycle_bits()
        e.draw_bit_mask(bits)
        e.run()
    exit(0)
    main = Environment( iter(open(filename)))
    #ain = Environment(dev_instr)

    while not main.done:
        try:
            main.run()
        except StopIteration:
            print(f"program done {main}")
            main.done = True

    print(f"Signal: {main.signal} SUM:{sum(main.signal)}")

    # ENV['program'] = parse_instruction(dev_instr)
    # ENV['instruction'] = next(ENV['program'])
    # print(ENV)

    # ENV['instruction'].execute(ENV)
    # print(ENV)

    # next_instruction(ENV)


    # print(ENV)


