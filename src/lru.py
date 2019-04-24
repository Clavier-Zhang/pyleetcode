from src.cache import cache

class Node:

    key = 0

    value = 0

    pre = None

    next = None

    def __init__(self, key, value):
        self.key = key
        self.value = value

class LRU:

    size = 0

    capacity = 100

    m = {}

    head = Node(0, 0)

    tail = Node(0, 0)

    def __init__(self):
        self.head.next = self.tail
        self.tail.pre = self.head
        self.decode(cache.get_lru())

    def get(self, key):
        if key not in self.m:
            return -1
        node = self.m[key]
        self.remove(node)
        self.add(node)

    def put(self, key, value):
        if key in self.m:
            self.remove(self.m[key])
        node = Node(key, value)
        self.add(node)
        if self.size > self.capacity:
            self.remove(self.tail.pre)
        cache.save_lru(self.encode())

    def add(self, node):
        node.pre = self.head
        node.next = self.head.next
        self.head.next.pre = node
        self.head.next = node
        self.size += 1
        self.m[node.key] = node

    def remove(self, node):
        node.next.pre = node.pre
        node.pre.next = node.next
        self.size -= 1
        self.m.pop(node.key)

    def encode(self):
        arr = []
        cur = self.head.next
        while cur != self.tail:
            arr.append([cur.key, cur.value])
            cur = cur.next
        return arr

    def decode(self, arr):
        arr.reverse()
        for pair in arr:
            node = Node(pair[0], pair[1])
            self.add(node)





lru = LRU()
lru.put(1, 50)
lru.put(3, 100)
# lru.decode(arr)
# lru.encode()