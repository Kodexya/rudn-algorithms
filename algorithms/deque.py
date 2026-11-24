"""Дек (двусторонняя очередь) на кольцевом буфере."""


class Deque:
    """Все операции добавления/удаления с обоих концов — амортизированно O(1)."""

    _MIN_CAPACITY = 8

    def __init__(self, iterable=None):
        self._data = [None] * self._MIN_CAPACITY
        self._head = 0  # индекс первого элемента
        self._size = 0
        if iterable is not None:
            for item in iterable:
                self.push_back(item)

    def __len__(self):
        return self._size

    def __iter__(self):
        cap = len(self._data)
        for i in range(self._size):
            yield self._data[(self._head + i) % cap]

    def __getitem__(self, index):
        if index < 0:
            index += self._size
        if not 0 <= index < self._size:
            raise IndexError("deque index out of range")
        return self._data[(self._head + index) % len(self._data)]

    def __repr__(self):
        return f"Deque({list(self)})"

    def is_empty(self):
        return self._size == 0

    @property
    def capacity(self):
        return len(self._data)

    def _resize(self, new_capacity):
        items = list(self)
        self._data = items + [None] * (new_capacity - len(items))
        self._head = 0

    def _shrink_if_sparse(self):
        # Уменьшаем в 2 раза, если занято не больше четверти (без "дребезга").
        cap = len(self._data)
        if cap > self._MIN_CAPACITY and self._size <= cap // 4:
            self._resize(cap // 2)

    def push_back(self, value):
        if self._size == len(self._data):
            self._resize(2 * len(self._data))
        self._data[(self._head + self._size) % len(self._data)] = value
        self._size += 1

    def push_front(self, value):
        if self._size == len(self._data):
            self._resize(2 * len(self._data))
        self._head = (self._head - 1) % len(self._data)
        self._data[self._head] = value
        self._size += 1

    def pop_front(self):
        if self._size == 0:
            raise IndexError("pop from empty deque")
        value = self._data[self._head]
        self._data[self._head] = None
        self._head = (self._head + 1) % len(self._data)
        self._size -= 1
        self._shrink_if_sparse()
        return value

    def pop_back(self):
        if self._size == 0:
            raise IndexError("pop from empty deque")
        index = (self._head + self._size - 1) % len(self._data)
        value = self._data[index]
        self._data[index] = None
        self._size -= 1
        self._shrink_if_sparse()
        return value

    def peek_front(self):
        if self._size == 0:
            raise IndexError("peek from empty deque")
        return self._data[self._head]

    def peek_back(self):
        if self._size == 0:
            raise IndexError("peek from empty deque")
        return self._data[(self._head + self._size - 1) % len(self._data)]
