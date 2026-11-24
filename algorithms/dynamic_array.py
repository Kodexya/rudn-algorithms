"""Динамический массив (аналог vector / ArrayList)."""


class DynamicArray:
    """Массив, который увеличивает ёмкость в 2 раза при заполнении.

    append — амортизированно O(1)
    get / set по индексу — O(1)
    insert / remove_at — O(n)
    """

    _MIN_CAPACITY = 4

    def __init__(self, iterable=None):
        self._capacity = self._MIN_CAPACITY
        self._data = [None] * self._capacity
        self._size = 0
        if iterable is not None:
            for item in iterable:
                self.append(item)

    def __len__(self):
        return self._size

    def __iter__(self):
        for i in range(self._size):
            yield self._data[i]

    def __getitem__(self, index):
        return self._data[self._normalize(index)]

    def __setitem__(self, index, value):
        self._data[self._normalize(index)] = value

    def __repr__(self):
        return f"DynamicArray({list(self)})"

    @property
    def capacity(self):
        return self._capacity

    def is_empty(self):
        return self._size == 0

    def _normalize(self, index):
        if index < 0:
            index += self._size
        if not 0 <= index < self._size:
            raise IndexError("array index out of range")
        return index

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity

    def append(self, value):
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        self._data[self._size] = value
        self._size += 1

    def insert(self, index, value):
        if not 0 <= index <= self._size:
            raise IndexError("array index out of range")
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        self._data[index] = value
        self._size += 1

    def pop(self):
        if self._size == 0:
            raise IndexError("pop from empty array")
        return self.remove_at(self._size - 1)

    def remove_at(self, index):
        index = self._normalize(index)
        value = self._data[index]
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        self._size -= 1
        self._data[self._size] = None
        # Сжимаем в 2 раза, если заполнено меньше четверти (без "дребезга").
        if self._capacity > self._MIN_CAPACITY and self._size <= self._capacity // 4:
            self._resize(max(self._MIN_CAPACITY, self._capacity // 2))
        return value

    def find(self, value):
        for i in range(self._size):
            if self._data[i] == value:
                return i
        return -1
