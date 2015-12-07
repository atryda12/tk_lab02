__author__ = 'damian'

c = 65735346575434578
itera = 0

def step(c, div, mul, add):
    if c % 2 == 0:
        print("{}\t{}\t{}".format(c/div, int(c/div), c//div))
        return int(c // div)
    else:
        return mul * c + add

while c > 1:
    c = step(c, 2, 3, 1)
    itera = itera + 1

print(itera)
