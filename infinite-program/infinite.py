import time
numbers = []

def lengthCalc(ar):
    return len(ar)

def adder(ar):
    length = lengthCalc(ar)
    ar.append(length)
    time.sleep(1)
    
while True:
    adder(numbers)
    print(numbers)