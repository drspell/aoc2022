import sys
import logging as log


def process_input(debug = False):
    global filename

    if len(sys.argv) > 1 or debug:
        filename = "test.txt" if '-t' in sys.argv else "input.txt"
        debugging = True if '-d' in sys.argv else False
    else:
        filename = "input.txt"
        debugging = False

    if debugging:
        log.basicConfig(level=log.DEBUG)
    else:
        log.basicConfig(level=log.INFO)


def left(forest):
    visible = []
    for row,trees in enumerate(forest[1:-1]):
        peak = trees[0]
        # print(f"row {row+1}: {trees}, peak: {peak}")

        for col,t in enumerate(trees[1:-1]):
            if t > peak:
                # print(f"visible {row+1},{col+1}; peak:{t}")
                visible.append((row+1,col+1))
                peak = t

        # print(f"row: {row+1}; visible: {visible}")

    return visible

def top(forest):
    visible = []
    for col in range(1,width-1):
        trees = get_col(col,forest)
        peak = trees[0]
        
        # print(f"top line of sight: {col} {trees[1:-1]} initial peak = {peak}")

        for row, t in enumerate(trees[1:-1]):
            if t > peak:
                # print(f"\t {(row+1, col)}, peak={peak}")
                visible.append((row+1,col))
                peak = t
    return visible

def right(forest):
    # print(f"FROM RIGHT:")
    visible = []
    for row, trees in enumerate(forest[1:-1]):
        # trees = trees[::-1]
        peak = trees[-1]
        # print(f"row {row+1}; {trees}, slice: {trees[-2:0:-1]} peak: {peak}")

        for col, t in enumerate(trees[-2:0:-1]):
            c = width - 2 - col
            # print(f"\trow {row+1},{c},{t}")
            if t > peak:
                # print(f"\t\tvisible {row+1} , {c}; peak:{t}")
                # visible_right.append(((row+1),(col+1),t))
                visible.append(((row+1),c))
                peak = t


        # for col, t in enumerate(trees[1:-1]):
        #     if t > peak:
        #         print(f"visible {row+1} , {col+1}; peak:{t}")
        #         # visible_right.append(((row+1),(col+1),t))
        #         visible.append(((row+1),(col+1)))
        #         peak = t

        # print(f"row: {row+1}: visible: {visible}")
    return visible

def bottom(forest):
    # print("FROM BOTTOM")
    visible = []

    for col in range(1,width-1):
        trees = get_col(col, forest)
        peak = trees[-1]

        # print(f"bottom line of sight: {col} {trees[1:-1]} initial peak = {peak}")
        # print(f"col {col+1}; {trees}, slice: {trees[-2:0:-1]} peak: {peak}")

        for row, t in enumerate(trees[-2:0:-1]):
            r = (height - 2) - row
            # print(f"\trow {r+1},{col},{t}")

            if t > peak:
                # print(f"\t\t{(r , col)}, peak={peak}")
                visible.append((r,col))
                peak = t

        # print(f"col: {col+1}: visible: {visible}")
    return visible
 

def get_col(col,lst):
    ret = [ val for row in lst for ind,val in enumerate(row) if ind == col ]
    return ret

def problem1():
    global width, height
    process_input()

    with open(filename) as F:
        forest = []
        for line in F:
            forest.append([ int(pos) for pos in line.rstrip()])
        
        width = len(forest[0])
        height = len(forest)
        perimeter = (2*width) + 2 * (height - 2)

        print(f"width: {width}, height:{height}")

        visible_top = top(forest)
        # print("\n")
        visible_bottom = bottom(forest)

        visible_interior = set(left(forest) + right(forest) + top(forest) + bottom(forest))
        visible_exterior = 2 * width + 2 * (height - 2)
        
        print(f"interior {len(visible_interior)}; exterior {visible_exterior} solution: {visible_exterior + len(visible_interior)}")
        
def problem2():
    filename = "input.txt"
    with open(filename) as F:
        forest = []
        for line in F:
            forest.append([ int(pos) for pos in line.rstrip()])
        
        width = len(forest[0])
        height = len(forest)
        perimeter = (2*width) + 2 * (height - 2)

        return forest

def up(lst, pos):
    if pos == 0:
        return []
    # pos = constrain(pos,1,len(lst))
    return lst[pos-1::-1] #slice(pos-1,None,-1)

def down(lst, pos):
    if pos == len(lst) - 1:
        return []

    # pos = constrain(pos,0,len(lst)-2)
    return lst[pos+1:] #slice(pos+1,None)

def left(lst, pos):
    return up(lst, pos)

def right(lst, pos):
    return down(lst, pos)
 
def constrain(val,min_val,max_val):
    return max(min(val,max_val),min_val)

def up_view(lst,pos):
    curr_height = lst[pos]
    in_view = 0

    for ht in up(lst, pos):
        in_view += 1
        if ht >= curr_height:
            break
    
    return in_view

def down_view(lst, pos):
    curr_height = lst[pos]
    in_view = 0

    for ht in down(lst,pos):
        in_view += 1
        if ht >= curr_height:
            break
    
    return in_view

def left_view(lst, pos):
    return up_view(lst, pos)

def right_view(lst, pos):
    return down_view(lst, pos)

def view_score(row,col,tree_row,tree_col):
    left_in_view = left_view(tree_row, col)
    right_in_view = right_view(tree_row, col)
    up_in_view = up_view(tree_col, row)
    down_in_view = down_view(tree_col, row)
    
    view_score = left_in_view * right_in_view * up_in_view * down_in_view

    return view_score

if __name__ == '__main__':
    forest = problem2()
    forest_cols = [ get_col(i,forest) for i in range(len(forest[0])) ]

    # scores = []
    best = 0
    for row,tree_row in enumerate(forest):
        for col,tree in enumerate(tree_row):
            score = view_score(row,col,tree_row,forest_cols[col])
            best = max(best,score)
            # scores.append((row,col,score))

    print(best)


    def get_left(i,j):
        # get the row for this cell
        row = forest[i]
        print(f"{row}")
        print(f"({i},{j}) - {row[j]}")
        # print(row[3:0:-1])
        for tree in row[j:0:-1]:
            print(tree)

    # Test the score of a single position for debugging
    # row, col = (3,2)
    # tree_row = forest[row]
    # tree_col = get_col(col,forest )
    # tree_ht = tree_col[row]

    # left_in_view = left_view(tree_row, col)
    # right_in_view = right_view(tree_row, col)
    # up_in_view = up_view(tree_col, row)
    # down_in_view = down_view(tree_col, row)
    
    # view_score = left_in_view * right_in_view * up_in_view * down_in_view

    # print(left_in_view, right_in_view, up_in_view, down_in_view, view_score)
    
