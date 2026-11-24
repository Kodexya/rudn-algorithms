"""АВЛ-дерево — самобалансирующееся двоичное дерево поиска."""


class _Node:
    __slots__ = ("height", "key", "left", "right", "value")

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


def _height(node):
    return node.height if node is not None else 0


def _update(node):
    node.height = 1 + max(_height(node.left), _height(node.right))


def _balance_factor(node):
    return _height(node.left) - _height(node.right)


def _rotate_right(y):
    x = y.left
    y.left = x.right
    x.right = y
    _update(y)
    _update(x)
    return x


def _rotate_left(x):
    y = x.right
    x.right = y.left
    y.left = x
    _update(x)
    _update(y)
    return y


def _rebalance(node):
    _update(node)
    balance = _balance_factor(node)
    if balance > 1:  # перевес влево
        if _balance_factor(node.left) < 0:  # случай LR
            node.left = _rotate_left(node.left)
        return _rotate_right(node)
    if balance < -1:  # перевес вправо
        if _balance_factor(node.right) > 0:  # случай RL
            node.right = _rotate_right(node.right)
        return _rotate_left(node)
    return node


class AVLTree:
    """Словарь ключ -> значение на АВЛ-дереве.

    insert / delete / search — O(log n) гарантированно.
    """

    def __init__(self):
        self._root = None
        self._size = 0

    def __len__(self):
        return self._size

    def __contains__(self, key):
        return self._find(key) is not None

    def _nodes(self):
        """Узлы в порядке возрастания ключей (in-order обход без рекурсии)."""
        stack, node = [], self._root
        while stack or node is not None:
            while node is not None:
                stack.append(node)
                node = node.left
            node = stack.pop()
            yield node
            node = node.right

    def __iter__(self):
        for node in self._nodes():
            yield node.key

    def items(self):
        """Пары (ключ, значение) по возрастанию ключа — O(n)."""
        for node in self._nodes():
            yield node.key, node.value

    @property
    def height(self):
        return _height(self._root)

    def _find(self, key):
        node = self._root
        while node is not None:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return node
        return None

    def search(self, key, default=None):
        node = self._find(key)
        return node.value if node is not None else default

    def insert(self, key, value=None):
        """Вставляет ключ. Если ключ уже есть — обновляет значение."""
        self._root = self._insert(self._root, key, value)

    def _insert(self, node, key, value):
        if node is None:
            self._size += 1
            return _Node(key, value)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value
            return node
        return _rebalance(node)

    def delete(self, key):
        """Удаляет ключ. Возвращает True, если ключ был в дереве."""
        old_size = self._size
        self._root = self._delete(self._root, key)
        return self._size < old_size

    def _delete(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None or node.right is None:
                self._size -= 1
                return node.left or node.right
            # Два потомка: заменяем минимальным из правого поддерева.
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.key, node.value = successor.key, successor.value
            node.right = self._delete(node.right, successor.key)
        return _rebalance(node)

    def min(self):
        if self._root is None:
            raise ValueError("min of empty tree")
        node = self._root
        while node.left is not None:
            node = node.left
        return node.key

    def max(self):
        if self._root is None:
            raise ValueError("max of empty tree")
        node = self._root
        while node.right is not None:
            node = node.right
        return node.key

    def is_balanced(self):
        """Проверка инвариантов АВЛ (используется в тестах)."""

        def check(node, lo, hi):
            if node is None:
                return 0
            if (lo is not None and node.key <= lo) or (hi is not None and node.key >= hi):
                raise AssertionError("BST property violated")
            lh = check(node.left, lo, node.key)
            rh = check(node.right, node.key, hi)
            if abs(lh - rh) > 1:
                raise AssertionError("AVL balance violated")
            if node.height != 1 + max(lh, rh):
                raise AssertionError("stored height is wrong")
            return node.height

        try:
            check(self._root, None, None)
        except AssertionError:
            return False
        return True
