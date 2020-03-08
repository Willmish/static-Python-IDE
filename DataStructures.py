from typing import List

class Stack:
    def __init__(self, size: int = 10) -> None:
        self._stack: List[object] = [None for _ in range(size)]
        self._size: int = size
        self._top: int = 0

    def pop(self) -> object:
        if self.isEmpty():
            raise Exception("Stack is Empty! Cannot Pop more objects!")

        self._top -= 1
        return self._stack[self._top]

    def push(self, toPush: object) -> None:
        if self.isFull():
            raise Exception("Stack is Full! Cannot Push more objects!")
        self._stack[self._top] = toPush
        self._top += 1

    def peek(self):
        return self._stack[self._top - 1]

    def isFull(self) -> bool:
        return self._top == self._size

    def isEmpty(self) -> bool:
        return self._top == 0

    def __str__(self) -> str:
        result: str = ""
        rstack: List[object] = self._stack[self._top - 1::-1]
        for i in range(self._top):
            result += str(rstack[i])
            result += '\n'

        return result


class LinearQueue:
    def __init__(self, size: int = 10) -> None:
        self._q = [None for _ in range(size)]
        self._size = size
        self._rear = 0

    def add(self, obj) -> None:
        if self.isFull():
            raise Exception("The Queue is Full! Cannot add more objects!")
        self._q[self._rear] = obj
        self._rear += 1

    def remove(self):
        if self._rear == 0:
            raise Exception("The Queue is Empty! Cannot remove more objects!")
        obj = self._q[0]
        for i in range(1, self._rear):
            self._q[i - 1] = self._q[i]
        self._rear -= 1
        return obj

    def isFull(self) -> bool:
        return self._rear == self._size

    def isEmpty(self) -> bool:
        return self._rear == 0

    def __str__(self) -> str:
        return ' '.join([str(self._q[i]) for i in range(self._rear)])
        # result: str= ""
        # for i in range(self._rear):
        #   result += str(self._q[i]) + " "
        # return result


class CircularQueue:
    def __init__(self, size: int = 10):
        self._size = size
        self._q = [None for _ in range(size)]
        self._rear = 0
        self._front = 0
        self._itemsInQ: int = 0

    def add(self, obj) -> None:
        if self.isFull():
            raise Exception("The Queue is Full! Cannot add more objects!")
        self._q[self._rear] = obj
        self._itemsInQ += 1
        self._rear = (self._rear + 1) % self._size

    def remove(self):
        if self.isEmpty():
            raise Exception("The Queue is Empty! Cannot remove more objects!")
        obj = self._q[self._front]
        self._front = (self._front + 1) % self._size
        self._itemsInQ -= 1
        return obj

    def isFull(self) -> bool:
        return self._itemsInQ == self._size

    def isEmpty(self) -> bool:
        return self._itemsInQ == 0

    def __str__(self) -> str:
        result = " ".join([str(self._q[i % self._size]) for i in range(self._front, self._front + self._itemsInQ)])
        return result


class obj:
    def __init__(self, value, priority: int):
        self._value = value
        self._priority: int = priority

    def __str__(self) -> str:
        return str(self._value) + ' ' + str(self._priority)


class LinearPriorityQueue:
    def __init__(self, size: int = 10) -> None:
        self._q = [None for _ in range(size)]
        self._size = size
        self._rear = 0

    def add(self, obj) -> None:
        if self.isFull():
            raise Exception("The Queue is Full! Cannot add more objects!")
        if self._rear > 0:
            for i in range(self._rear, -1, -1):
                if i == 0:
                    self._q[i] = obj
                    break
                if obj._priority <= self._q[i - 1]._priority:
                    self._q[i] = obj
                    break
                else:
                    self._q[i] = self._q[i - 1]
        else:
            self._q[self._rear] = obj
        self._rear += 1

    def remove(self):
        if self._rear == 0:
            raise Exception("The Queue is Empty! Cannot remove more objects!")
        obj = self._q[0]
        for i in range(1, self._rear):
            self._q[i - 1] = self._q[i]
        self._rear -= 1
        return obj

    def isFull(self) -> bool:
        return self._rear == self._size

    def isEmpty(self) -> bool:
        return self._rear == 0

    def __str__(self) -> str:
        return ' '.join([str(self._q[i]) for i in range(self._rear)])


class CircularPriorityQueue():
    def __init__(self, size: int = 10):
        self._size = size
        self._q = [None for _ in range(size)]
        self._rear = 0
        self._front = 0
        self._itemsInQ: int = 0

    def add(self, obj) -> None:
        if self.isFull():
            raise Exception("The Queue is Full! Cannot add more objects!")
        if self._itemsInQ > 0:
            for i in range(self._front, self._front+self._size):
                j = i % self._size

                if j == self._rear:
                    self._q[j] = obj
                    break
                if obj._priority > self._q[j]._priority:
                    s = obj
                    obj = self._q[j]
                    self._q[j] = s
        else:
            self._q[self._rear] = obj

        self._itemsInQ += 1
        self._rear = (self._rear + 1) % self._size

    def remove(self):
        if self.isEmpty():
            raise Exception("The Queue is Empty! Cannot remove more objects!")
        obj = self._q[self._front]
        self._front = (self._front + 1) % self._size
        self._itemsInQ -= 1
        return obj

    def isFull(self) -> bool:
        return self._itemsInQ == self._size

    def isEmpty(self) -> bool:
        return self._itemsInQ == 0

    def __str__(self) -> str:
        result = " ".join([str(self._q[i % self._size]) for i in range(self._front, self._front + self._itemsInQ)])
        return result
'''
class Graph():
    def __init__(self, numNodes: int = 10):
        self.size = numNodes
        self.nodes = [[0 for _ in range(numNodes)] for _ in range(numNodes)]

    def addEdge(self, nodeA: int, nodeB: int) -> None:
        self.nodes[nodeA][nodeB] = 1
        self.nodes[nodeB][nodeA] = 1

    def removeEdge(self, nodeA: int, nodeB: int) -> None:
        self.nodes[nodeA][nodeB] = 0
        self.nodes[nodeB][nodeA] = 0

    def isEdge(self, nodeA: int, nodeB: int) -> bool:
        if self.nodes[nodeB][nodeA] == 1:
            return True
        return False

    def BFS(self, s):
        vis: bool = [False for _ in range(self.size)]
        q = []
        q.append(s)
        vis[s] = True
        while (q):
            s = q.pop(0)
            print(s, end=' ')

            for i in self.nodes[s]:
                if (not vis[i]):
                    q.append(i)
                    vis[i] = False
'''
