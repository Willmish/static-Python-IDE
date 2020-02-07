from typing import List, Dict, Tuple
'''
a: str = 'hi'
print(type(a))

a = 2
print(type(a))
'''

'''
def returnInt(a: int) -> int:
    return a


print(('hi'))
print(type(returnInt('hi')))

'''


'''
from typing import List


arr: List[int] = [1, 2, 'hi', True]
print(arr)
print(type(arr))
'''
'''
from typing import Dict


dict: Dict[str, int] = {}

dict['hi'] = 2
dict[3] = (1, 3.14)
print(dict)
'''
'''
i: int = 5

def hi():
    print(i)
    for j in range(8):
        print(i+j)

    def wow():
        print('wow')
        print(j)
    wow()


for i in range(10):
    j: bool = True
    print(i)

print(j)
while j:
    print(j)
    i -= 1
    print(i)
    if i == 0:
        j = False
    j += 1

print(j)
'''
# TODO TCA error check reference below:
'''
s: str = \'
print(s)

  File "C:/Users/Szymon/PycharmProjects/ShymIDE/programs/test1.py", line 67
    s: str = \'
              ^
SyntaxError: unexpected character after line continuation character

'''
'''
s = 'baba'
def wow():
    b = s + 'a'
    print(b)


wow()
'''
'''
a: int = 0
print(a, type(a))
a = 5 - 0*(2/4)
print(a, type(a))
myTuple = ('//', '+')
print('/' in myTuple)

d = 'ah \ #'
print(d)
'''

b: Dict[List[int], int] = {'ahoy': 2, 2: 4}

print(b, type(b))

myT: Tuple[str, int] = ('a', 1)
myT = ('cd', 2)

#myList: List[int] = [1, 2]
#myList -= [1]

this: str = 'a'
print(this, type(this))

def newMethod():
    this: int = 2
    print(this, type(this))

newMethod()
print(this, type(this))


