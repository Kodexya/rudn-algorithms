import random
from collections import deque as std_deque

import pytest

from algorithms import Deque


def test_basic_operations():
    d = Deque()
    d.push_back(2)
    d.push_front(1)
    d.push_back(3)
    assert list(d) == [1, 2, 3]
    assert d.peek_front() == 1
    assert d.peek_back() == 3
    assert d.pop_front() == 1
    assert d.pop_back() == 3
    assert d.pop_back() == 2
    assert d.is_empty()


def test_empty_errors():
    d = Deque()
    for op in (d.pop_front, d.pop_back, d.peek_front, d.peek_back):
        with pytest.raises(IndexError):
            op()


def test_wraparound_and_growth():
    d = Deque()
    for i in range(20):
        d.push_front(i)
    assert list(d) == list(range(19, -1, -1))
    assert d[0] == 19
    assert d[-1] == 0


def test_against_std_deque():
    random.seed(0)
    mine, ref = Deque(), std_deque()
    for _ in range(5000):
        op = random.randint(0, 3)
        if op == 0:
            x = random.random()
            mine.push_back(x)
            ref.append(x)
        elif op == 1:
            x = random.random()
            mine.push_front(x)
            ref.appendleft(x)
        elif op == 2 and ref:
            assert mine.pop_back() == ref.pop()
        elif op == 3 and ref:
            assert mine.pop_front() == ref.popleft()
        assert len(mine) == len(ref)
    assert list(mine) == list(ref)


def test_shrinks_after_many_pops():
    d = Deque(range(10_000))
    big = d.capacity
    for _ in range(9_990):
        d.pop_front()
    assert d.capacity < big
    assert d.capacity >= len(d)
    assert list(d) == list(range(9_990, 10_000))
    while d:
        d.pop_back()
    assert d.capacity == 8
