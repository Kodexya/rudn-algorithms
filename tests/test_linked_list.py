import pytest

from algorithms import LinkedList


def test_empty():
    lst = LinkedList()
    assert len(lst) == 0
    assert lst.is_empty()
    assert list(lst) == []
    with pytest.raises(IndexError):
        lst.pop_front()


def test_push_and_iterate():
    lst = LinkedList()
    lst.push_back(2)
    lst.push_back(3)
    lst.push_front(1)
    assert list(lst) == [1, 2, 3]
    assert len(lst) == 3


def test_get_insert_remove_at():
    lst = LinkedList([1, 2, 4])
    lst.insert(2, 3)
    lst.insert(0, 0)
    lst.insert(5, 5)
    assert list(lst) == [0, 1, 2, 3, 4, 5]
    assert lst.get(3) == 3
    assert lst.remove_at(5) == 5
    assert lst.remove_at(0) == 0
    assert list(lst) == [1, 2, 3, 4]
    lst.push_back(10)  # хвост должен быть корректным после remove_at
    assert list(lst) == [1, 2, 3, 4, 10]
    with pytest.raises(IndexError):
        lst.get(10)
    with pytest.raises(IndexError):
        lst.insert(-1, 0)


def test_find_remove_contains():
    lst = LinkedList(["a", "b", "c", "b"])
    assert lst.find("b") == 1
    assert lst.find("z") == -1
    assert "c" in lst
    assert lst.remove("b") is True
    assert list(lst) == ["a", "c", "b"]
    assert lst.remove("z") is False


def test_reverse():
    lst = LinkedList([1, 2, 3, 4])
    lst.reverse()
    assert list(lst) == [4, 3, 2, 1]
    lst.push_back(0)
    assert list(lst) == [4, 3, 2, 1, 0]


def test_pop_until_empty_then_reuse():
    lst = LinkedList([1, 2])
    assert lst.pop_front() == 1
    assert lst.pop_front() == 2
    assert lst.is_empty()
    lst.push_back(7)
    assert list(lst) == [7]


def test_clear():
    lst = LinkedList(range(5))
    lst.clear()
    assert len(lst) == 0 and list(lst) == []
