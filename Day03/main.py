import sys

if len(sys.argv) == 2 and sys.argv[1] == '-t':
    filename = "test01.txt"
else:
    filename = "input.txt"


#initialize character codes
code = {}

lc_code = list(range(ord('a'),ord('z')+1) )
uc_code = list(range(ord('A'),ord ('Z') + 1))

for ind,c in enumerate(lc_code + uc_code):
    code[chr(c)] = ind + 1

def split_to_sack(items):
    mid = len(items)//2
    return set(items[:mid]), set(items[mid:])

def problem1():
    dups = []

    with open(filename) as FH:
        for line in FH:
            l = line.strip()
            sack1, sack2 = split_to_sack(l)
            in_both = sack1.intersection(sack2)
            
            if in_both is not None:
                dups.append(list(in_both)[0])
            else:
                dups.append(in_both)

    answer1 = [code[c] for c in dups]
    print(dups)
    print(sum(answer1))

def problem2():
    result = 0

    with open(filename) as FH:
        for line in FH:
            line2 = FH.readline()
            line3 = FH.readline()

            elf1 = split_to_sack(line.strip())
            elf2 = split_to_sack(line2.strip())
            elf3 = split_to_sack(line3.strip())

            # find the dups between elf1 and elf2
            dups12 = set()
            for sack1 in elf1:
                for sack2 in elf2:
                    for item in sack1.intersection(sack2):
                        dups12.add(item)

            # find the item that is in elf3 sacks that 
            # is in the duplicats set
            for sack in elf3:
                for item in sack:
                    if item in dups12:
                        print(f"Badge: {item}")
                        result += code[item]
                        break

    print(f"problem 2 answer {result}")
# problem1()
problem2()

