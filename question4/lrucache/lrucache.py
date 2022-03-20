class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LruCache:
    def __init__(self, capacity):
        self.capacity = capacity
        if capacity < 1 :
            self.capacity = 1
        
        
        # simiulate orderedict
        self.cache = dict()
        # Double Linked List
        # head item is of recently added (position for to be added item)
        # tail item is of oldest  (pointer for to be deleted item)
        s = Node(0, 0)
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
        

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.value
        return None
        

    def put(self, key, value):

        # if item exist in cache, remove and append again 
        if key in self.cache:
            self._remove(self.cache[key])
        new_node = Node(key, value)

        # 
        self._add(new_node)
        self.cache[key] = new_node
        is_full = len(self.cache) > self.capacity
        if is_full:
            discard_node = self.tail.prev
            # remove from doubly linked list
            self._remove(discard_node)
            # remove from cache
            del self.cache[discard_node.key]
    
    def _remove(self, node):
        # remove targe node in linked list
        prev = node.prev
        temp_next = node.next
        prev.next = temp_next
        temp_next.prev = prev
        
    def _add(self, node):
        # add to head of linked list
        temp_next = self.head.next
        temp_next.prev = node
        node.next = temp_next
        self.head.next = node
        node.prev = self.head