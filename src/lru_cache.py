from src.cache import cache
import json
import os
from pathlib import Path

class Node:

    key = 0

    value = 0

    pre = None

    next = None

    def __init__(self, key, value):
        self.key = key
        self.value = value

class LRUCache:

    size = 0

    capacity = 100

    m = {}

    head = Node(0, 0)

    tail = Node(0, 0)

    lru = 'data/lru.json'

    path = os.path.dirname(os.path.abspath(__file__))+'/'

    def __init__(self):
        if not Path(self.path+'data').is_dir():
            os.mkdir(self.path+'data')
        if not Path(self.path+self.lru).is_file():
            open(self.path+self.lru, 'w').write('[]')
        self.head.next = self.tail
        self.tail.pre = self.head
        self.decode()

    def get_obj(self, filename):
        file = open(os.path.dirname(os.path.abspath(__file__))+'/'+filename, 'r')
        obj = json.load(file)
        file.close()
        return obj

    def save_obj(self, filename, obj):
        file = open(os.path.dirname(os.path.abspath(__file__))+'/'+filename, 'w')
        json.dump(obj, file)
        file.close()

    def get(self, key):
        if key not in self.m:
            return None
        node = self.m[key]
        self.remove(node)
        self.add(node)
        return node.value

    def put(self, key, value):
        if key in self.m:
            self.remove(self.m[key])
        node = Node(key, value)
        self.add(node)
        if self.size > self.capacity:
            self.remove(self.tail.pre)
        self.save_obj(self.lru, self.encode())

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

    def decode(self):
        arr = self.get_obj(self.lru)
        arr.reverse()
        for pair in arr:
            node = Node(pair[0], pair[1])
            self.add(node)




lru = LRUCache()

