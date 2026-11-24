import pytest

from algorithms import DynamicArray


def test_append_and_index():
    arr = DynamicArray()
    for i in range(100):
        arr.append(i)
    assert len(arr) == 100
    assert arr[0] == 0
    assert arr[99] == 99
    assert arr[-1] == 99
    assert list(arr) == list(range(100))


def test_capacity_grows_and_shrinks():
    arr = DynamicArray()
    start = arr.capacity
    for i in range(start + 1):
        arr.append(i)
    assert arr.capacity == start * 2
    while len(arr) > 1:
        arr.pop()
    assert arr.capacity == start


def test_setitem():
    arr = DynamicArray([1, 2, 3])
    arr[1] = 20
    arr[-1] = 30
    assert list(arr) == [1, 20, 30]


def test_insert_and_remove_at():
    arr = DynamicArray([1, 3])
    arr.insert(1, 2)
    arr.insert(0, 0)
    arr.insert(4, 4)
    assert list(arr) == [0, 1, 2, 3, 4]
    assert arr.remove_at(2) == 2
    assert arr.remove_at(-1) == 4
    assert list(arr) == [0, 1, 3]


def test_find_and_pop():
    arr = DynamicArray("abc")
    assert arr.find("b") == 1
    assert arr.find("z") == -1
    assert arr.pop() == "c"
    assert len(arr) == 2


def test_errors():
    arr = DynamicArray()
    with pytest.raises(IndexError):
        arr.pop()
    with pytest.raises(IndexError):
        arr[0]
    with pytest.raises(IndexError):
        arr.insert(1, 5)
