"""Сортировка пузырьком и быстрая сортировка.

bubble_sort сортирует список на месте, quick_sort возвращает новый список.
"""

import random


def bubble_sort(values):
    """Сортирует список пузырьком на месте и возвращает его.

    O(n^2), на уже отсортированных данных — O(n).
    """
    end = len(values) - 1  # граница неотсортированной части
    while end > 0:
        last_swap = 0
        for i in range(end):
            if values[i] > values[i + 1]:
                values[i], values[i + 1] = values[i + 1], values[i]
                last_swap = i
        # Всё правее последнего обмена уже стоит на своих местах
        end = last_swap
    return values


def quick_sort(items, key=None, reverse=False):
    """Быстрая сортировка, в среднем O(n log n).

    - случайный опорный элемент (защита от O(n^2) на отсортированных данных);
    - трёхпутевое разбиение (много одинаковых элементов не ломает сложность);
    - рекурсия только в меньшую часть, глубина стека O(log n).
    """
    arr = list(items)
    keys = [key(x) for x in arr] if key else arr

    def swap(i, j):
        arr[i], arr[j] = arr[j], arr[i]
        if key:
            keys[i], keys[j] = keys[j], keys[i]

    def less(a, b):
        return b < a if reverse else a < b

    def sort(lo, hi):
        while lo < hi:
            swap(lo, random.randint(lo, hi))
            pivot = keys[lo]
            lt, i, gt = lo, lo + 1, hi
            # [lo, lt) < pivot, [lt, i) == pivot, (gt, hi] > pivot
            while i <= gt:
                if less(keys[i], pivot):
                    swap(lt, i)
                    lt += 1
                    i += 1
                elif less(pivot, keys[i]):
                    swap(i, gt)
                    gt -= 1
                else:
                    i += 1
            if lt - lo < hi - gt:
                sort(lo, lt - 1)
                lo = gt + 1
            else:
                sort(gt + 1, hi)
                hi = lt - 1

    sort(0, len(arr) - 1)
    return arr
