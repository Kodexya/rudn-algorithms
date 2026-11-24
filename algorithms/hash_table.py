"""Простая хэш-таблица с разрешением коллизий методом цепочек."""


class HashTable:
    """put / get / remove — в среднем O(1).

    При коэффициенте заполнения больше 0.75 число корзин удваивается.
    """

    _INITIAL_CAPACITY = 8
    _MAX_LOAD = 0.75

    def __init__(self):
        self._buckets = [[] for _ in range(self._INITIAL_CAPACITY)]
        self._size = 0

    def __len__(self):
        return self._size

    def __contains__(self, key):
        return any(k == key for k, _ in self._bucket(key))

    def __getitem__(self, key):
        for k, v in self._bucket(key):
            if k == key:
                return v
        raise KeyError(key)

    def __setitem__(self, key, value):
        self.put(key, value)

    def __delitem__(self, key):
        if not self.remove(key):
            raise KeyError(key)

    def __iter__(self):
        for bucket in self._buckets:
            for k, _ in bucket:
                yield k

    def items(self):
        for bucket in self._buckets:
            yield from bucket

    @property
    def capacity(self):
        return len(self._buckets)

    def _bucket(self, key):
        return self._buckets[hash(key) % len(self._buckets)]

    def put(self, key, value):
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1
        if self._size > self._MAX_LOAD * len(self._buckets):
            self._resize(len(self._buckets) * 2)

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default

    def remove(self, key):
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = bucket[-1]
                bucket.pop()
                self._size -= 1
                return True
        return False

    def _resize(self, new_capacity):
        old_items = list(self.items())
        self._buckets = [[] for _ in range(new_capacity)]
        for k, v in old_items:
            self._buckets[hash(k) % new_capacity].append((k, v))
