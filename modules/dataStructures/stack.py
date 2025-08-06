# modules/dataStructures/stack.py
from .linkedList import LinkedList

class Stack:
    def __init__(self):
        self.items = LinkedList()
    
    def push(self, item):
        self.items.prepend(item)
    
    def pop(self):
        if self.isEmpty():
            raise ValueError("Stack vacío")
        item = self.items.head.data
        self.items.remove(item)
        return item
    
    def peek(self):
        if self.isEmpty():
            raise ValueError("Stack vacío")
        return self.items.head.data
    
    def isEmpty(self):
        return self.items.isEmpty()
    
    def __len__(self):
        return len(self.items)
    
    def __str__(self):
        return str(self.items)