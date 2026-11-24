# Алгоритмы и структуры данных

![tests](../../actions/workflows/tests.yml/badge.svg)

Реализации базовых структур данных и алгоритмов на Python с тестами (pytest)
и автоматическим запуском тестов в GitHub Actions.

| Что | Файл | Сложность основных операций |
|---|---|---|
| Односвязный список | `algorithms/linked_list.py` | push_front/back, pop_front — O(1); доступ по индексу — O(n) |
| Динамический массив | `algorithms/dynamic_array.py` | доступ — O(1); append — амортизированно O(1); insert/remove — O(n) |
| Дек (кольцевой буфер) | `algorithms/deque.py` | push/pop с обоих концов — амортизированно O(1) |
| АВЛ-дерево | `algorithms/avl_tree.py` | insert/delete/search — O(log n) |
| Сортировка пузырьком | `algorithms/sorting.py` | O(n²), на отсортированных данных — O(n) |
| Быстрая сортировка | `algorithms/sorting.py` | O(n log n) в среднем (случайный pivot, 3-путевое разбиение) |
| Хэш-таблица (цепочки) | `algorithms/hash_table.py` | put/get/remove — O(1) в среднем |
| LRU-кэш | `algorithms/lru_cache.py` | get/put — O(1) (словарь + двусвязный список) |

## Запуск тестов

```bash
pip install -r requirements-dev.txt
pytest -v
```

Тесты автоматически запускаются при каждом push (см. `.github/workflows/tests.yml`).
