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
s: str = \'
print(s)
