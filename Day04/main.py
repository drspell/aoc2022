import sys
import re

if len(sys.argv) == 2 and sys.argv[1] == '-t':
    filename = "test01.txt"
else:
    filename = "input.txt"

regex = '(\d+)-(\d+),(\d+)-(\d+)'

def problem1():
    count, intersections = 0,0
    with open(filename) as FH:
        for line in FH:
            a,b,c,d = re.findall(regex,line)[0]
            a,b,c,d = [int(x) for x in [a,b,c,d]]
            section1 = set(list(range(a,b+1)))
            section2 = set(list(range(c,d+1)))

            if section1.issubset(section2) or section1.issuperset(section2):
                count += 1
            if len(section1.intersection(section2)) > 0:
                intersections += 1

    print(f"fully contained: {count} intersect: {intersections}")
problem1()