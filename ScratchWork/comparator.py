import util

def compareBodies(a, b):
    mistakes = 0
    for i in range(len(a)):
        if abs(a[i]-b[i]) > .1:
            mistakes += 1
    return mistakes > 2

