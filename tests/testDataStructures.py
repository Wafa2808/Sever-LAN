# tests/testDataStructures.py
import unittest
from modules.dataStructures.linkedList import LinkedList, Node
from modules.dataStructures.queue import Queue
from modules.dataStructures.stack import Stack

class TestDataStructures(unittest.TestCase):
    def testLinkedList(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.prepend(0)
        
        self.assertEqual(list(ll), [0, 1, 2])
        self.assertEqual(len(ll), 3)
        
        ll.remove(1)
        self.assertEqual(list(ll), [0, 2])
    
    def testQueue(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.peek(), 2)
        self.assertFalse(q.isEmpty())
    
    def testStack(self):
        s = Stack()
        s.push(1)
        s.push(2)
        
        self.assertEqual(s.pop(), 2)
        self.assertEqual(s.peek(), 1)
        self.assertFalse(s.isEmpty())

if __name__ == '__main__':
    unittest.main()