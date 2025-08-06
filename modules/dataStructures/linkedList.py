# modules/dataStructures/linkedList.py
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
    
    def __str__(self):
        return str(self.data)

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def append(self, data):
        newNode = Node(data)
        if not self.head:
            self.head = newNode
            self.tail = newNode
        else:
            self.tail.next = newNode
            self.tail = newNode
        self.size += 1
    
    def prepend(self, data):
        newNode = Node(data)
        if not self.head:
            self.head = newNode
            self.tail = newNode
        else:
            newNode.next = self.head
            self.head = newNode
        self.size += 1
    
    def remove(self, data):
        if not self.head:
            raise ValueError("Lista vacía")
        
        if self.head.data == data:
            self.head = self.head.next
            if not self.head:
                self.tail = None
            self.size -= 1
            return
        
        current = self.head
        while current.next:
            if current.next.data == data:
                if current.next == self.tail:
                    self.tail = current
                current.next = current.next.next
                self.size -= 1
                return
            current = current.next
        
        raise ValueError(f"Dato {data} no encontrado en la lista")
    
    def isEmpty(self):
        return self.size == 0
    
    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next
    
    def __str__(self):
        return " → ".join(str(item) for item in self) if not self.isEmpty() else "Empty List"
    
    def __len__(self):
        return self.size