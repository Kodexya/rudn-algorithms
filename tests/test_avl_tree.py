import math
import random

import pytest

from algorithms import AVLTree


def test_empty():
    t = AVLTree()
    assert len(t) == 0
    assert t.height == 0
    assert list(t) == []
    assert t.search(1) is None
    with pytest.raises(ValueError):
        t.min()


def test_insert_search_update():
    t = AVLTree()
    t.insert(5, "five")
    t.insert(3, "three")
    t.insert(8, "eight")
    assert t.search(3) == "three"
    assert t.search(42, "nope") == "nope"
    t.insert(3, "THREE")
    assert t.search(3) == "THREE"
    assert len(t) == 3
    assert 8 in t and 4 not in t


def test_sorted_insert_stays_balanced():
    # Обычное BST выродилось бы в список высотой 1000.
    t = AVLTree()
    for i in range(1000):
        t.insert(i)
    assert t.is_balanced()
    assert t.height <= 1.45 * math.log2(1000 + 2)
    assert list(t) == list(range(1000))
    assert t.min() == 0 and t.max() == 999


@pytest.mark.parametrize("keys", [[3, 2, 1], [1, 2, 3], [3, 1, 2], [1, 3, 2]])
def test_all_rotation_cases(keys):
    t = AVLTree()
    for k in keys:
        t.insert(k)
    assert t.height == 2
    assert t.is_balanced()


def test_delete():
    t = AVLTree()
    for k in [50, 30, 70, 20, 40, 60, 80]:
        t.insert(k, str(k))
    assert t.delete(20) is True   # лист
    assert t.delete(30) is True   # один потомок
    assert t.delete(50) is True   # два потомка (корень)
    assert t.delete(999) is False
    assert list(t) == [40, 60, 70, 80]
    assert t.search(60) == "60"
    assert len(t) == 4
    assert t.is_balanced()


def test_random_against_set():
    random.seed(1)
    t, ref = AVLTree(), set()
    for _ in range(3000):
        k = random.randint(0, 500)
        if random.random() < 0.6:
            t.insert(k)
            ref.add(k)
        else:
            assert t.delete(k) == (k in ref)
            ref.discard(k)
    assert list(t) == sorted(ref)
    assert len(t) == len(ref)
    assert t.is_balanced()


def test_items():
    t = AVLTree()
    for k in "dbac":
        t.insert(k, k.upper())
    assert list(t.items()) == [("a", "A"), ("b", "B"), ("c", "C"), ("d", "D")]
