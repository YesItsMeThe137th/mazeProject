class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class linkedList:
    def __init__(self):
        self.head = None
        self.end = None
        self.len = 0
    
    def push(self, value):
        newNode = Node(value)
        if (self.len == 0):
            self.head = newNode
        else:
            self.end.next = newNode
        self.end = newNode
        self.len += 1

    def popNode(self):
        v = self.end.value
        tempNode = self.head
        for i in range(self.len - 2):
            #print("Checking linked list at index", i, tempNode.value)
            tempNode = tempNode.next
        tempNode.next = None
        self.end = tempNode
        self.len -= 1
        return v

if __name__ == '__main__':
    ll = linkedList()
    ll.push("hi there")
    ll.push("I'm the best")
    ll.push(3.1415)
    seahorse = "seahorse"
    ll.push(seahorse)
    print(ll.popNode())
    print(ll.popNode())
    print(ll.popNode())
    print(ll.popNode())