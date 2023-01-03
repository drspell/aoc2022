import re
import sys

testing = True if len(sys.argv) == 2 and sys.argv[1] == '-t' else False

# file name
if testing:
    filename = "test011.txt"  
else:
    filename = "input011.txt" 

# keep track of calories for an elf
sub_total = 0
# list storing total calories of elves
totals = []

# open input file
FH = open(filename,"r")

for x in FH:
    _input = re.search("\d+",x)
    x = x.strip() 
    print(f"line length: {len(x)}")
    if _input is not None:
        calories = int(_input.group())
        sub_total += calories
    else:
        totals.append(sub_total)
        sub_total = 0

# close the file
FH.close()

# we may have a sub_total that we have not added to 
# the totals if the last line of the file is not blank
if sub_total > 0:
    totals.append(sub_total)
    sub_total = 0

# make sure that we read in all of the data
if testing:
    assert len(totals) == 5

# print(totals)
# print(f"solution part 1:  {max(totals)}")
totals.sort(reverse=True)
print(f"solution part 1:  {totals[0]}")
print(f"solution part 2:  {sum(totals[:3])}")