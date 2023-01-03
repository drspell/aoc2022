import cli
from cli import filename,testing

def char_count(signal,size):

    for i in range(len(signal)):
        if i < size:
            continue
        
        if len(set(signal[i-size:i])) == size:
            return i


with open(filename) as FH:
    if testing:
        for i,line in enumerate(FH):
           line = line.rstrip()
           signal, prob1, prob2 = line.split(" ")
           response1 = char_count(signal,4)
           response2 = char_count(signal,14)
           assert response1 == int(prob1), f"expected:{prob1} got: {response1}"
           assert response2 == int(prob2), f"expected:{prob2} got: {response2}"
           print(f"test {i+1} passed")
    else: 
        print(f"solution part 1: {char_count(FH.readline(),4)}")
        FH.seek(0)
        print(f"solution part 2: {char_count(FH.readline(),14)}")

