import sys

testing = True if len(sys.argv) == 2 and sys.argv[1] == '-t' else False

# file name
if testing:
    filename = "testinput021.txt"  
else:
    filename = "input02.txt" 

ROCK = 1
PAPER = 2
SCISSORS = 3
LOSS = 0
DRAW = 3
WIN = 6

symbols = { 'A':ROCK, 'B':PAPER,'C':SCISSORS,
            'X':ROCK, 'Y':PAPER,'Z':SCISSORS}

def make_lose(move):
    if move == ROCK:
        return PAPER
    if move == PAPER:
        return SCISSORS
    if move == SCISSORS:
        return ROCK

def make_win(move):
    if move == ROCK:
        return SCISSORS
    if move == PAPER:
        return ROCK
    if move == SCISSORS:
        return PAPER

def make_draw(move):
    return move

def get_move(opp_move,code):
    if code == 'X':
        return make_win(opp_move)
    if code == 'Y':
        return make_draw(opp_move) 
    if code == 'Z':
        return make_lose(opp_move)

    raise Exception("could not get move for opponent %s and code %s" % (opp_move,code))

def rps(x,y):
    # print(f"{x} -- {y}")
    if x == y:
        return None
    # paper  beats rock
    if ROCK in [x,y] and PAPER in [x,y]: 
        return PAPER

    if ROCK in [x,y] and SCISSORS in [x,y]: 
        return ROCK
    
    if PAPER in [x,y] and SCISSORS in [x,y]: 
        return SCISSORS

    else:
        raise Exception("unaccounted for combination", x,y)

def score(other,you):
    outcome = rps(other,you)
    
    #loss
    if outcome == other:
        result =  LOSS 
    elif outcome == None:
        result =  DRAW 
    elif outcome == you:
        result = WIN
    else:
        raise Exception("unknown outcome")

    # print(f"outcome {outcome}; other {other} ; you {you}; result {result}")
    return you + result


def main1():
    total = 0

    with open(filename) as F:
        for line in F:
            opp, me = line.strip().split(" ")
            opp = opp.strip()
            me = me.strip()
            scr = score(symbols[opp], symbols[me])
            # print(f"round: ",opp, me,symbols[opp], symbols[me],scr)
            total += scr

    print(f"SCORE: {total}")

def main2():
    total = 0

    with open(filename) as F:
        for line in F:
            opp, me = line.strip().split(" ")
            opp = opp.strip()
            me = me.strip()

            mymove = get_move(symbols[opp],me)
            scr = score(symbols[opp], mymove)
            # print(f"round: ",opp, me,mymove, symbols[opp],scr)
            total += scr
    print(f"SCORE: {total}")
 
# main1()
main2()