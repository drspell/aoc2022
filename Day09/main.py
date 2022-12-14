import sys
import logging as log


def process_input(debugging = False, test = True):

    global filename

    if test:
        filename = "test.txt" 
    else:
        filename = "input.txt"

    if debugging:
        log.basicConfig(level=log.DEBUG)
    else:
        log.basicConfig(level=log.INFO)


class Board:
    BLANK = '.'
    VISITED = '#'

    def __init__(self, rows, cols, start):
        self.rows = rows
        self.cols = cols
        self.start = start

    def draw(self,rope):
        board = []

        for r in range(self.rows):
            row_str = []
            for c in range(self.cols):
                knot = rope.knot_at(r,c)  
                if knot is not None:
                    if knot == rope.knots[0]:
                        row_str.append('H')
                    # elif knot == rope.knots[-1]:
                        # row_str.append('T')
                    else:
                        row_str.append(str(knot.id))
                else:
                    if r == self.start[0] and c == self.start[1]:
                        row_str.append('s')
                    else:
                        row_str.append(self.BLANK) 

            board.append(row_str)
        
        board = [ "".join(l) for l in board]

        print("\n".join(board))

    def draw_visited(self,rope):
        board = []
        visited = list(rope.tail_positions)
        # print(f"visisted: {visited}")

        for r in range(self.rows):
            row_str = []
            for c in range(self.cols):
                pos = next(( v for v in visited if v[0]== r and v[1] == c),None)
                if pos is None:
                    row_str.append(self.BLANK)
                else:
                    if r == self.start[0] and c == self.start[1]:
                        row_str.append('s')
                    else:
                        row_str.append(self.VISITED)

            board.append(row_str)

        board = [ "".join(l) for l in board]

        print("\n".join(board))


class Knot:
    def __init__(self, id, row, col):
        self.id = id
        self.row = row
        self.col = col

    # def __add__(self,offset):
        # self.row += offset[0]
        # self.col += offset[1]

    def move(self, row, col):
        self.row += row
        self.col += col

    def __str__(self):
        return f"([{self.id}],({self.row},{self.col}))"

    def __repr__(self):
        return self.__str__()

    def __hash__(self) -> int:
        return (self.row * 31 + self.col * 13 + self.id * 51) * 193

    def __eq__(self, __o: object) -> bool:
        return self.row == __o.row and self.col == __o.col and self.id == __o.id

    def distance(self, other):
        """ return manhatten distance to other from me""" 
        return abs(other.row - self.row) + abs(other.col - self.col) 
    
    def inline(self,other):
        return self.row == other.row or self.col == other.col



class Rope:
    # HEAD = 0
    # TAIL = 1

    def __init__(self, ps):
        self.knots = []

        for i,pos in enumerate(ps):
            row,col = pos
            self.knots.append(Knot(i,row,col))
        
        self.head = self.knots[0] #Knot(0,head[0],head[1])
        self.tail = self.knots[-1] #Knot(1,tail[0],tail[1])
        self.tail_positions = set([(self.tail.row, self.tail.col)])

    def __str__(self):
        return f"({self.head},{self.tail})"
    
    def __repr__(self):
        return self.__str__()

    def knot_at(self,r,c):
        for knot in self.knots:
            if knot.row == r and knot.col == c:
                return knot
        
        return None

    def down(self,which):
        knot = self.knots[which]
        knot.move(1,0)
        # if which == Rope.HEAD:
        #     self.head = (self.head[0] + 1, self.head[1])
        # else:
        #     self.tail = (self.tail[0] + 1, self.tail[1])

    def up(self,which):
        knot = self.knots[which]
        knot.move(-1,0)
        # if which == Rope.HEAD:
        #     self.head = (self.head[0] - 1, self.head[1])
        # else:
        #     self.tail = (self.tail[0] - 1, self.tail[1])

    def right(self,which):
        knot = self.knots[which]
        # print(f"\t\t(move right): {knot} ",end='...')
        knot.move(0,1)
        # print(f"(to): {knot} ")
        
        # if which == Rope.HEAD:
        #     self.head = (self.head[0], self.head[1] + 1)
        # else:
        #     self.tail = (self.tail[0], self.tail[1] + 1)

    def left(self,which):
        knot = self.knots[which]
        knot.move(0,-1)
        
        # if which == Rope.HEAD:
            # self.head = (self.head[0], self.head[1] - 1)
        # else:
            # self.tail = (self.tail[0], self.tail[1] - 1)

    def up_left(self,which):
        # print("up_left")
        knot = self.knots[which]
        knot.move(-1,-1)
        
        # self.up(step,which)
        # self.left(step,which)

    def up_right(self,which):
        knot = self.knots[which]
        knot.move(-1,1)
        
        # print("up_right")
        # self.up(step,which)
        # self.right(step,which)

    def down_right(self,which):
        knot = self.knots[which]
        knot.move(1,1)
        
        # print("down_right")
        # self.down(step,which)
        # self.right(step,which)

    def down_left(self,which):
        knot = self.knots[which]
        knot.move(1,-1)
        
        # print("down_left")
        # self.down(step,which)
        # self.left(step,which)

    def update(self):

        for i in range(1,len(self.knots)):
            leading_node, trailing_node = self.knots[i-1:i+1]
            
            # check to see if we need to move the tail
            distance = leading_node.distance(trailing_node) #self.length()
            delta_row = leading_node.row - trailing_node.row
            delta_col = leading_node.col - trailing_node.col

            # if abs(delta_row) > 1: 
                # print(f"\t\t{trailing_node}--{leading_node}",end='...')
                # print(f"distance:{distance}; delta_row:{delta_row}; delta_col:{delta_col}")

            is_inline = trailing_node.inline(leading_node)

            if is_inline and distance > 1:
                # need to move the tail by 1 towards the head
                if delta_col < 0:
                    self.left(i)
                elif delta_col > 0:
                    self.right(i)
                elif delta_row < 0:
                    # print(f"{i} should be moving up...")
                    self.up(i)
                    # print(f"{i} after moving up??")
                elif delta_row > 0:
                    self.down(i)
                else:
                    raise Exception("should not be here")
            
            elif not is_inline and distance > 2:
                if delta_col < 0:
                    if delta_row < 0:
                        self.up_left(i)
                    elif delta_row > 0:
                        self.down_left(i)
                    else:
                        raise Exception("should not be here")

                elif delta_col > 0:
                    if delta_row > 0:
                        self.down_right(i)
                    elif delta_row < 0:
                        self.up_right(i)
                    else:
                        raise Exception("should not be here")

                else:
                    raise Exception("should not be here")

        self.tail_positions.add((self.knots[-1].row, self.knots[-1].col))

            # print(f"\t{trailing_node} -- {leading_node}")

       
    def update_old(self):
        # check to see if we need to move the tail
        dist = self.length()
        delta_row = self.head.row - self.tail.row
        delta_col = self.head.col - self.tail.col

        if self.inline() and dist > 1:
            # need to move the tail by 1 towards the head

            if delta_col < 0:
                self.left(Rope.TAIL)
            elif delta_col > 0:
                self.right(Rope.TAIL)
            elif delta_row < 0:
                self.up(Rope.TAIL)
            elif delta_row > 0:
                self.down(Rope.TAIL)
        
        elif not self.inline() and dist > 2:
            if delta_col < 0:
                if delta_row < 0:
                    self.up_left(Rope.TAIL)
                elif delta_row > 0:
                    self.down_left(Rope.TAIL)

            elif delta_col > 0:
                if delta_row > 0:
                    self.down_right(Rope.TAIL)
                elif delta_row < 0:
                    self.up_right(Rope.TAIL)

        self.tail_positions.add((self.tail.row, self.tail.col))

    # def inline(self):
        # return self.head.row == self.tail.row or self.head.col == self.tail.col
        # return self.head[0] == self.tail[0] or self.head[1] == self.tail[1]

    # def length(self):
        # return abs(self.head.row - self.tail.row) + abs(self.head.col - self.tail.col)
        # return abs(self.head[0] - self.tail[0]) + abs(self.head[1] - self.tail[1])

    def tail_position_count(self):
        return len(self.tail_positions)


def run_command(dir,count,rope,display=True):
    cmd = None

    if display:
        print_command(dir,count)

    if dir == 'U':
        cmd = getattr(rope,'up')

    elif dir == 'D':
        cmd = getattr(rope,'down')

    elif dir == 'L':
        cmd = getattr(rope,'left')

    elif dir == 'R':
        cmd = getattr(rope,'right')


    for i in range(int(count)):
        cmd(0)
        rope.update()

        if display:
            board.draw(rope)
            print()


def print_command(dir,steps):
    print(f"== {dir} {steps} ==")

if __name__ == '__main__':
    testing = '-t' in sys.argv
    debugging = '-d' in sys.argv
    # process_input(debugging=debugging, test = testing) 
    filename = 'test.txt' if testing else 'input.txt'

    init_pos = (4,0)

    if testing:
        board = Board(5,6,init_pos)

    short_rope = Rope([init_pos,init_pos])
    long_rope = Rope([init_pos for i in range(10)])

    rope = long_rope

    if testing:
        board.draw(rope)

    with open(filename) as FH:
        for line in FH:
            # print(line)
            line.rstrip()
            dir,count = line.split(" ")
            run_command(dir,count,rope, display=testing)

            # print('\t',rope,rope.tail_position_count())

    print("VISITED",rope.tail_position_count())

    if testing:
        board.draw_visited(rope)

    # run_command('R', 4,rope)
    # print(rope,rope.tail_position_count())

    # run_command("U", 1,rope)
    # print(rope,rope.tail_position_count())

    # run_command("U", 1,rope)
    # run_command("U", 1,rope)
    # print(rope,rope.tail_position_count())

    # run_command("L", 3,rope)
    # run_command("D", 1,rope)
    # run_command('R', 4,rope)
    # run_command("D", 1,rope)
    # print(rope)
    # run_command("L", 1,rope)
    # print(rope)
    # run_command("L", 1,rope)
    # print(rope)
    # run_command("L", 1,rope)
    # print(rope)
    # run_command("L", 1,rope)
    # print(rope)
    # run_command("L", 1,rope)
    # print(rope)



    

