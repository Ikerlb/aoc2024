from itertools import repeat

disk_map = input()

def format(s):
    return "".join(str(n) if n is not None else "." for n in s)

class Node:
    def __init__(self, val, next = None, prev = None):
        self.val = val
        self.next = next
        self.prev = prev

    def add_after(self, node):
        nxt = self.next
        self.next = node
        node.next = nxt
        node.prev = self
        nxt.prev = node

    def find(self, f):
        node = self
        while node:   
            if f(node):
                return node
            node = node.next

    def __iter__(self):
        yield self.val
        if self.next:
            yield from self.next

class LinkedList:
    def __init__(self):
        head = Node("|")
        tail = Node("|")
        head.next = tail
        tail.prev = head
        self._head = head
        self._tail = tail

    def add_front(self, val):
        node = Node(val)
        self._head.add_after(node)

    def add_back(self, val):
        node = Node(val)
        self._tail.prev.add_after(node)
        return node

    def head(self):
        if self.head.next.val != "|":
            return self.head.next.val

    def tail(self):
        if self.head.next.val != "|":
            return self.tail.prev.val

    def peek(self):
        if t := self.tail() is not None:
            return t.val

    def pop(self):
        t = self.tail()
        if t is None:
            return
        prv = t.prev
        prv.next = self._tail
        t.next = t.prev = None
        return t.val

    def __repr__(self):
        return "<->".join(str(node) for node in self)

    def __iter__(self):
        yield from (node for node in self._head if node != "|")

def format_linkedlist(ll):
    res = []
    for t, c, i in ll:
        print(t, c, i)
        res.append(str(i) * c if t == "FILL" else "." * c)
    return "".join(res)

def parse(disk):
    ll = LinkedList()
    empties = []
    cur = 0
    for i,c in enumerate(disk):
        if i % 2 == 0:
            ll.add_back(("FILL", int(c), cur))
            cur += 1
        else:
            node = ll.add_back(("EMPTY", int(c), None))
            empties.append(node)
    empties.reverse()
    return ll, empties


# TODO
# can probably do both parts 
# with linked lists!

def part2(disk_map):
    ll, empties

# test linked list
#ll = LinkedList()
#print("add front before", ll)
#for i in range(10):
#    ll.add_front(Node(i))
#print("add front after", ll)
#
#ll = LinkedList()
#print("add back before", ll)
#for i in range(10):
#    ll.add_back(Node(i))
#print("add back after", ll)
