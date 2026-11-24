import random

import pytest

from algorithms import HashTable


def test_put_get():
    h = HashTable()
    h.put("a", 1)
    h["b"] = 2
    assert h.get("a") == 1
    assert h["b"] == 2
    assert h.get("z") is None
    assert h.get("z", 0) == 0
    assert len(h) == 2


def test_overwrite():
    h = HashTable()
    h["k"] = 1
    h["k"] = 2
    assert h["k"] == 2
    assert len(h) == 1


def test_remove():
    h = HashTable()
    h["x"] = 1
    assert h.remove("x") is True
    assert h.remove("x") is False
    assert "x" not in h
    with pytest.raises(KeyError):
        h["x"]
    with pytest.raises(KeyError):
        del h["x"]


def test_resize_keeps_data():
    h = HashTable()
    start = h.capacity
    for i in range(1000):
        h[i] = i * i
    assert h.capacity > start
    assert len(h) == 1000
    assert all(h[i] == i * i for i in range(1000))
    assert sorted(h) == list(range(1000))


class BadHash:
    """Все объекты попадают в одну корзину — проверка цепочек."""

    def __init__(self, v):
        self.v = v

    def __hash__(self):
        return 42

    def __eq__(self, other):
        return isinstance(other, BadHash) and self.v == other.v


def test_collisions():
    h = HashTable()
    keys = [BadHash(i) for i in range(20)]
    for i, k in enumerate(keys):
        h[k] = i
    for i, k in enumerate(keys):
        assert h[k] == i
    h.remove(keys[5])
    assert keys[5] not in h
    assert len(h) == 19


def test_random_against_dict():
    random.seed(3)
    h, ref = HashTable(), {}
    for _ in range(5000):
        k = random.randint(0, 300)
        if random.random() < 0.7:
            v = random.random()
            h[k] = v
            ref[k] = v
        else:
            assert h.remove(k) == (k in ref)
            ref.pop(k, None)
    assert len(h) == len(ref)
    assert dict(h.items()) == ref
