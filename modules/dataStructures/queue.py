# modules/dataStructures/queue.py
from .linkedList import LinkedList

class Queue:
    def __init__(self):
        self.items = LinkedList()
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        if self.isEmpty():
            raise ValueError("Queue vacía")
        item = self.items.head.data
        self.items.remove(item)
        return item
    
    def peek(self):
        if self.isEmpty():
            raise ValueError("Queue vacía")
        return self.items.head.data
    
    def isEmpty(self):
        return self.items.isEmpty()
    
    def __len__(self):
        return len(self.items)
    
    def __str__(self):
        return str(self.items)