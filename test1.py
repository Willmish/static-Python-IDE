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

i: int = 5

def hi():
    print(i)
    for j in range(8):
        print(i+j)

    def wow():
        print('wow')
        print(j)
    wow()


hi()
print(i)
print(type(i))