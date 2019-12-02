from collections import defaultdict
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
#geeksforgeeks
class Graph:

    # Constructor
    def __init__(self):

        # default dictionary to store the graph
        self.graph = defaultdict(list)

        # function to add an edge to the graph

    def addEdge(self, u, v):
        self.graph[u].append(v)

        # Function to print a BFS of the graph

    def DFSUtil(self, v, visited):

        # Mark the current node as visited and print it
        visited[v] = True
        print (v)

        # Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if visited[i] == False:
                self.DFSUtil(i, visited)

                # The function to do DFS traversal. It uses

    # recursive DFSUtil()
    def DFS(self, v):

        # Mark all the vertices as not visited
        visited = [False] * (len(self.graph))

        # Call the recursive helper function to print
        # DFS traversal
        self.DFSUtil(v, visited)
    def BFS(self, s):

        # Mark all the vertices as not visited
        visited = [False] * (len(self.graph))

        # Create a queue for BFS
        queue = []

        # Mark the source node as
        # visited and enqueue it
        queue.append(s)
        visited[s] = True

        while queue:

            # Dequeue a vertex from
            # queue and print it
            s = queue.pop(0)
            print(s, end=" ")

            # Get all adjacent vertices of the
            # dequeued vertex s. If a adjacent
            # has not been visited, then mark it
            # visited and enqueue it
            for i in self.graph[s]:
                if visited[i] == False:
                    queue.append(i)
                    visited[i] = True

'''
# Driver code

# Create a graph given in
# the above diagram
g = Graph()
g.addEdge(0, 1)
g.addEdge(0, 2)
g.addEdge(1, 2)
g.addEdge(2, 0)
g.addEdge(2, 3)
g.addEdge(3, 3)

print("Following is Breadth First Traversal"
      " (starting from vertex 2)")
g.BFS(2)
print()
g.DFS(2)

o1 = obj(chr(65), 1)
o11 = obj('D', 1)
o2 = obj('B', 3)
o3 = obj('C', 9)

q1 = CircularPriorityQueue()
q1.Add(o1)
q1.Add(o3)
q1.Add(o2)
print(q1)
print(q1.Remove())
q1.Add(o11)
print(q1)'''
