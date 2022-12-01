from operator import itemgetter
from re import T


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self, numLevels):
        self.num = 1
        self.len = numLevels
        self.head = self.createNode(1)
        
        

    def createNode(self, level):
        node = Node(self.num)
        #print(node.value)
        self.num += 1
        level += 1
        if (level >= self.len):
            #print("At level", level, "we stopped because the max length is", self.len)
            return node

        node.left = self.createNode(level)
        node.right = self.createNode(level)
        return node

    def DFS(self, ind, node): # depth first search ie search left side first, deep down then up
        if (node):
                    #if (ind < self.len - 1):
            self.DFS(ind + 1, node.left)
            self.DFS(ind + 1, node.right)
            print(node.value)

    def lessIntuitive_DFS(self, node):
        if node:
            stack = [node]
            while (stack):
                n = stack.pop()
                print(n.value)
                if n.right:
                    stack.append(n.right)
                if n.left:
                    stack.append(n.left)

    def BFS(self, node): # breadth first search search each row first, high up then down
        if node:
            queue = [node]
            while (queue): # this means while length of queue is greater than 0
                n = queue.pop(0)
                print(n.value)
                if n.left: 
                    queue.append(n.left)
                if n.right: 
                    queue.append(n.right)
            
    
    def lessIntuitive_BFS(self, nodes):
        nextNodes = []
        if nodes:
            for node in nodes:
                print(node.value)
                if node.left:
                    nextNodes.append(node.left)
                if node.right:
                    nextNodes.append(node.right)
            self.lessIntuitive_BFS(nextNodes)




# idea: 

if __name__ == '__main__':
    bt = BinaryTree(4)
    #bt.DFS(1, bt.head)  
    bt.BFS(bt.head)  
    #bt.lessIntuitive_DFS(bt.head)  
    print("\n")
    bt.lessIntuitive_BFS([bt.head]) # takes a list  