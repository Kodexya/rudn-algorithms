import random

import pytest

from algorithms import bubble_sort, quick_sort

CASES = [
    [],
    [1],
    [2, 1],
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1],
    [3, 1, 2, 3, 1, 2],
    [7] * 10,
    [-5, 0, 3, -1, 2.5],
    ["banana", "apple", "cherry"],
]


# ---------- сортировка пузырьком (на месте) ----------


@pytest.mark.parametrize("data", CASES)
def test_bubble_matches_builtin(data):
    assert bubble_sort(list(data)) == sorted(data)


def test_bubble_sorts_in_place_and_returns_same_list():
    data = [3, 1, 2]
    result = bubble_sort(data)
    assert data == [1, 2, 3]
    assert result is data


def test_bubble_random_arrays():
    rng = random.Random(1)
    for _ in range(200):
        data = [rng.randint(-100, 100) for _ in range(rng.randint(0, 100))]
        assert bubble_sort(list(data)) == sorted(data)


def test_bubble_is_stable():
    # Равные элементы не меняются местами (сравниваем только по первому полю).
    class Item:
        def __init__(self, key, tag):
            self.key, self.tag = key, tag

        def __gt__(self, other):
            return self.key > other.key

    items = [Item(1, "b"), Item(0, "a"), Item(1, "a"), Item(0, "b")]
    bubble_sort(items)
    assert [(x.key, x.tag) for x in items] == [(0, "a"), (0, "b"), (1, "b"), (1, "a")]


# ---------- быстрая сортировка (новый список) ----------


@pytest.mark.parametrize("data", CASES)
def test_quick_matches_builtin(data):
    assert quick_sort(data) == sorted(data)
    assert quick_sort(data, reverse=True) == sorted(data, reverse=True)


def test_quick_does_not_modify_input():
    data = [3, 1, 2]
    quick_sort(data)
    assert data == [3, 1, 2]


def test_quick_random_arrays():
    rng = random.Random(2)
    for _ in range(50):
        data = [rng.randint(-100, 100) for _ in range(rng.randint(0, 200))]
        assert quick_sort(data) == sorted(data)


def test_quick_key():
    words = ["ccc", "a", "bb", "dddd"]
    assert quick_sort(words, key=len) == ["a", "bb", "ccc", "dddd"]
    assert quick_sort(words, key=len, reverse=True) == ["dddd", "ccc", "bb", "a"]


def test_quick_sort_large_sorted_and_duplicates():
    # Без случайного pivot и 3-путевого разбиения тут был бы O(n^2) / RecursionError.
    big = list(range(100_000))
    assert quick_sort(big) == big
    dups = [random.randint(0, 3) for _ in range(100_000)]
    assert quick_sort(dups) == sorted(dups)
