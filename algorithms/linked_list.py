"""Односвязный список."""


class _Node:
    __slots__ = ("next", "value")

    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node


class LinkedList:
    """Односвязный список с указателями на голову и хвост.

    push_front / push_back / pop_front — O(1)
    поиск, вставка и удаление по индексу — O(n)
    """

    def __init__(self, iterable=None):
        self._head = None
        self._tail = None
        self._size = 0
        if iterable is not None:
            for item in iterable:
                self.push_back(item)

    def __len__(self):
        return self._size

    def __iter__(self):
        node = self._head
        while node is not None:
            yield node.value
            node = node.next

    def __contains__(self, value):
        return self.find(value) != -1

    def __repr__(self):
        return f"LinkedList({list(self)})"

    def is_empty(self):
        return self._size == 0

    def push_front(self, value):
        self._head = _Node(value, self._head)
        if self._tail is None:
            self._tail = self._head
        self._size += 1

    def push_back(self, value):
        node = _Node(value)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def pop_front(self):
        if self._head is None:
            raise IndexError("pop from empty list")
        node = self._head
        self._head = node.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return node.value

    def _node_at(self, index):
        node = self._head
        for _ in range(index):
            node = node.next
        return node

    def _check_index(self, index):
        if not 0 <= index < self._size:
            raise IndexError("list index out of range")

    def get(self, index):
        self._check_index(index)
        return self._node_at(index).value

    def insert(self, index, value):
        if not 0 <= index <= self._size:
            raise IndexError("list index out of range")
        if index == 0:
            self.push_front(value)
        elif index == self._size:
            self.push_back(value)
        else:
            prev = self._node_at(index - 1)
            prev.next = _Node(value, prev.next)
            self._size += 1

    def remove_at(self, index):
        self._check_index(index)
        if index == 0:
            return self.pop_front()
        prev = self._node_at(index - 1)
        node = prev.next
        prev.next = node.next
        if node is self._tail:
            self._tail = prev
        self._size -= 1
        return node.value

    def find(self, value):
        """Индекс первого вхождения или -1."""
        for i, item in enumerate(self):
            if item == value:
                return i
        return -1

    def remove(self, value):
        """Удаляет первое вхождение. Возвращает True, если элемент был найден."""
        index = self.find(value)
        if index == -1:
            return False
        self.remove_at(index)
        return True

    def reverse(self):
        prev, node = None, self._head
        self._tail = self._head
        while node is not None:
            node.next, prev, node = prev, node, node.next
        self._head = prev

    def clear(self):
        self._head = self._tail = None
        self._size = 0
