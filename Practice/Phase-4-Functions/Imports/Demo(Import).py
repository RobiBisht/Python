import Demo

print(Demo.p)

z = Demo.calc()
print(z)

from Demo import p
from Demo import calc
from Demo import *

print(p)

z = calc()
print(z)