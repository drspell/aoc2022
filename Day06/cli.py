import sys

testing = True if len(sys.argv) == 2 and sys.argv[1] == '-t' else False

# file name
if testing:
    filename = "test.txt"  
else:
    filename = "input.txt" 