"""LRU-кэш: хэш-таблица + двусвязный список."""


class _Node:
    __slots__ = ("key", "next", "prev", "value")

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """Кэш фиксированного размера, вытесняющий давно не использованный элемент.

    get / put — O(1). Словарь даёт быстрый поиск узла, а двусвязный список
    хранит порядок использования: у головы — самые свежие, у хвоста — старые.
    """

    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._map = {}
        # Фиктивные узлы, чтобы не проверять граничные случаи.
        self._head = _Node()
        self._tail = _Node()
        self._head.next = self._tail
        self._tail.prev = self._head

    def __len__(self):
        return len(self._map)

    def __contains__(self, key):
        return key in self._map

    def keys(self):
        """Ключи от самого свежего к самому старому."""
        node = self._head.next
        while node is not self._tail:
            yield node.key
            node = node.next

    def _unlink(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _push_front(self, node):
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node
        self._head.next = node

    def get(self, key, default=None):
        node = self._map.get(key)
        if node is None:
            return default
        self._unlink(node)
        self._push_front(node)
        return node.value

    def put(self, key, value):
        node = self._map.get(key)
        if node is not None:
            node.value = value
            self._unlink(node)
            self._push_front(node)
            return
        if len(self._map) >= self.capacity:
            lru = self._tail.prev
            self._unlink(lru)
            del self._map[lru.key]
        node = _Node(key, value)
        self._map[key] = node
        self._push_front(node)
