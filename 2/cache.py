class ListNode:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class Cache:
    def __init__(self, n):
        self.n = n
        self.bucket_size = 97
        self.count = 0
        self.head = ListNode()  # Dummy head
        self.tail = ListNode()  # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head
        self.nodes = [None] * self.bucket_size  # Initial bucket size as 97

    def calculate_hash(self, key):
        hash = 0
        idx = 1
        for i in key:
            hash += ord(i)
            idx += 1
        return hash % self.bucket_size

    def _remove(self, node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_head(self, node):
        first_node = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = first_node
        first_node.prev = node

    def access_page(self, url, contents):
        index = self.calculate_hash(url) 
        node = self.nodes[index]

        # Check if the URL is already in cache
        while node:
            if node.key == url:
                self._remove(node)
                self._add_to_front(node)
                node.value = contents  # Update the content if needed
                return
            # print(node.key)

            node = node.next

        # If not in cache, add it
        new_node = ListNode(url, contents)
        new_node.next = self.nodes[index]
        if self.nodes[index]:
            self.nodes[index].prev = new_node
        self.nodes[index] = new_node
        self._add_to_head(new_node)
        self.count += 1

        # If the cache is full, remove the least recently accessed item
        if self.count > self.n:
            lru = self.tail.prev
            self._remove(lru)
            self.count -= 1

            # Remove from nodes
            index = self.calculate_hash(lru.key) 
            node = self.nodes[index]
            prev_node = None
            while node:
                if node.key == lru.prev.key:
                    if prev_node:
                        prev_node.next = node.next
                    else:
                        self.nodes[index] = node.next
                    if node.next:
                        node.next.prev = prev_node
                    break
                prev_node = node
                node = node.next

    def get_pages(self):
        result = []
        current = self.head.next
        while current != self.tail:
            result.append(current.key)
            current = current.next
        return result

def cache_test():
    cache = Cache(4)
    assert cache.get_pages() == []
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com"]
    cache.access_page("b.com", "BBB")
    assert cache.get_pages() == ["b.com", "a.com"]
    cache.access_page("c.com", "CCC")
    assert cache.get_pages() == ["c.com", "b.com", "a.com"]
    cache.access_page("d.com", "DDD")
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]
    cache.access_page("d.com", "DDD")
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "d.com", "c.com", "b.com"]
    cache.access_page("c.com", "CCC")
    assert cache.get_pages() == ["c.com", "a.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]
    cache.access_page("e.com", "EEE")
    assert cache.get_pages() == ["e.com", "a.com", "c.com", "d.com"]
    cache.access_page("f.com", "FFF")
    assert cache.get_pages() == ["f.com", "e.com", "a.com", "c.com"]
    cache.access_page("e.com", "EEE")
    assert cache.get_pages() == ["e.com", "f.com", "a.com", "c.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "e.com", "f.com", "c.com"]
    print("Tests passed!")

if __name__ == "__main__":
    cache_test()
