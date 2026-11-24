import random
from collections import OrderedDict

import pytest

from algorithms import LRUCache


def test_invalid_capacity():
    with pytest.raises(ValueError):
        LRUCache(0)


def test_eviction_order():
    c = LRUCache(2)
    c.put(1, "a")
    c.put(2, "b")
    assert c.get(1) == "a"  # 1 стал самым свежим
    c.put(3, "c")           # вытесняется 2
    assert 2 not in c
    assert c.get(1) == "a"
    assert c.get(3) == "c"
    assert len(c) == 2


def test_update_refreshes():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(1, 10)  # обновление делает 1 самым свежим
    c.put(3, 3)   # вытесняется 2
    assert c.get(1) == 10
    assert c.get(2) is None
    assert list(c.keys()) == [1, 3]


def test_capacity_one():
    c = LRUCache(1)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a", "miss") == "miss"
    assert c.get("b") == 2


def test_random_against_reference():
    random.seed(4)
    cap = 10
    c, ref = LRUCache(cap), OrderedDict()
    for _ in range(5000):
        k = random.randint(0, 30)
        if random.random() < 0.5:
            c.put(k, k)
            ref[k] = k
            ref.move_to_end(k)
            if len(ref) > cap:
                ref.popitem(last=False)
        else:
            expected = ref.get(k)
            if k in ref:
                ref.move_to_end(k)
            assert c.get(k) == expected
    assert list(c.keys()) == list(reversed(ref))
