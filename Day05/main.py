import sys
from queue import LifoQueue
import re
from stack import Stack

testing = True if len(sys.argv) == 2 and sys.argv[1] == '-t' else False

# file name
if testing:
    filename = "testinput.txt"  
else:
    filename = "input.txt" 

board = []

def read_board(file):
    # board_list = []
    raw_board = []
    line = file.readline()

    #initialize stack count
    stacks = len(line) // 4
    for i in range(stacks):
        raw_board.append([])
        # board_list.append(Stack())

    while len(line) > 1: # blank lines have length of 1
        # strip \n
        line = line[:-1]

        # if there are numbers then we are at the
        # last line of the map
        if re.match("^.*\d",line)  is not None:
            line = file.readline()
            continue

        for i in range(0,len(line),4):
            # grab the 3 characters for the position
            location = line[i:i+4]
            # the crate
            crate = location[1]
            if crate != " ":
                raw_board[i // 4].append(crate)

        line = file.readline()

    for stacks in raw_board:
        board.append(Stack(stacks))

    # print(f"board_list = {board_list}")
    # print(f"board = {board}")

    # for idx, crates in enumerate(board_list):
    #     # last entry of each list is the stack number
    #     # need to erase that
    #     board_list[idx] = crates[:-1] #board_list[idx][:-1]
    #     board_list[idx].reverse()

    #     # create a LIFO queue for each stack 
    #     q = LifoQueue()
    #     for crate in board_list[idx]:
    #         q.put(crate)

    #     # add the LifoQueue to the Board
    #     board.append(q)

def command_1(amount, frm, to):
    source = board[frm - 1]
    dest = board[to - 1]

    # print(f"source size: {source.size()}; dest size: {dest.size()}")
    for i in range(amount):
        source_crate = source.pop()
        # print(f"\tmoving crate: {source_crate}")
        dest.push(source_crate)        

def command_2(amount, frm, to):
    source = board[frm - 1]
    dest = board[to - 1]

    source_crates = source.data[:amount]
    source.data = source.data[amount:]
    # print(f"source_crates: {source_crates}; source: {source}; dest: {dest}")
    dest.data = source_crates + dest.data
    # print(f"source size: {source.size()}; dest size: {dest.size()}")
    # for i in range(amount):
    #     source_crate = source.pop()
    #     # print(f"\tmoving crate: {source_crate}")
    #     dest.push(source_crate)        




def top_of_stacks():
    return [ stack.peek() for stack in board]

# pass in the problem number [1,2]
def solve(prob_number):
    command = command_1 if prob_number == 1 else command_2
    with open(filename) as FH:
        read_board(FH)

        # for stack in board:
            # print(f"stack {stack.qsize()}")

        # print("-------")
        # for idx,stack in enumerate(board):
            # print(f"Stack: {idx}")

            # for crate in range(stack.qsize()):
                # print("\t",crate, stack.get())


        for line in FH:
            matches = re.findall("move\s(\d+)\sfrom\s(\d+)\sto\s(\d+)",line)
            # print(line,matches)
            amount,frm,to = [int(x) for x in matches[0]]
            # print(amount,frm,to)
            command(amount,frm,to)
            # print(board)

    print("".join(top_of_stacks()))

solve(2)
