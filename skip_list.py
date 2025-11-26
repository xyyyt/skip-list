from __future__ import annotations
from typing import Protocol, Any, TypeVar, Generic, Self, Final, Iterator, cast
import random

# defines a type bound, so skip list node values
# can be compared (<, >, <=, >=, ==, !=) in mypy
class Comparable(Protocol):
    def __lt__(self, other: Any) -> bool: ...
    def __gt__(self, other: Any) -> bool: ...
    def __le__(self, other: Any) -> bool: ...
    def __ge__(self, other: Any) -> bool: ...
    def __eq__(self, other: Any) -> bool: ...
    def __ne__(self, other: Any) -> bool: ...

T = TypeVar("T", bound=Comparable)

class SkipList(Generic[T]):
    """
    A probabilistic ordered data structure supporting fast search,
    insertion, and deletion of elements.

    Average-time complexity for operations is O(log n),
    equivalent to balanced binary search trees.
    """

    class Node:
        """
        A node in the SkipList, holding a value and
        forward pointers across multiple levels.
        """

        __slots__ = ("value", "current_level", "forward")

        current_level: int
        forward: list[Self | None]

        def __init__(self, value: T | None, max_level: int) -> None:
            self.value: T | None = value
            self.current_level = -1
            self.forward = [None] * (max_level + 1)

    __slots__ = ("_p", "_max_level", "_size", "_head")

    _p: Final[float]
    _max_level: Final[int]
    _size: int
    _head: SkipList.Node

    def __init__(self,
                 promotion_probability: float = 0.5,
                 max_level: int = 32) -> None:
        if promotion_probability < 0 or promotion_probability > 1:
            raise ValueError(
                f"Invalid promotion probability value: {promotion_probability}. "
                "Parameter 'promotion_probability' must be "
                "between 0 and 1 inclusive.")

        self._p = promotion_probability

        if max_level < 0:
            raise ValueError(
                f"Invalid max_level value: {max_level}. "
                "Parameter 'max_level' must be greater than or equal to 0.")

        self._max_level = max_level
        self._size = 0
        self._head = SkipList.Node(None, self._max_level)

    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return self._size > 0

    def iter_from(self, level: int) -> Iterator[T]:
        if level < 0:
            raise ValueError(
                f"'level' {level} is too low (min 0)")
        elif level > self._head.current_level:
            raise ValueError(
                f"'level' {level} is too high "
                f"(max {self._head.current_level})")

        current_node: SkipList.Node | None = self._head.forward[level]

        while current_node is not None:
            yield cast(T, current_node.value)
            current_node = current_node.forward[level]

    @property
    def promotion_probability(self) -> float:
        return self._p

    @property
    def max_level(self) -> int:
        return self._max_level

    @property
    def size(self) -> int:
        return self._size

    @property
    def current_level(self) -> int:
        return self._head.current_level

    def insert(self, value: T) -> bool:
        new_node: SkipList.Node
        level: int

        # only to add first element
        if self._head.forward[0] is None:
            new_node = SkipList.Node(value, self._max_level)

            for level in range(self._random_level() + 1):
                new_node.current_level = level
                self._head.current_level = level
                self._head.forward[level] = new_node
        else:
            current_level: int = self._head.current_level
            update: list[SkipList.Node | None] = \
                [None] * (current_level + 1)
            current_node: SkipList.Node = self._head

            while True:
                while True:
                    next_node: SkipList.Node | None = \
                        current_node.forward[current_level]

                    if next_node is None or next_node.value is None:
                        break

                    if value == next_node.value:
                        return False
                    elif value > next_node.value:
                        current_node = next_node
                    else:
                        break

                update[current_level] = current_node

                if current_level == 0:
                    break

                current_level -= 1

            new_node = SkipList.Node(value, self._max_level)

            for level in range(self._random_level() + 1):
                new_node.current_level = level

                if level >= len(update):
                    self._head.current_level = level
                    self._head.forward[level] = new_node
                else:
                    prev: SkipList.Node | None = update[level]

                    if prev is None:
                        continue

                    new_node.forward[level] = prev.forward[level]
                    prev.forward[level] = new_node

        self._size += 1

        return True

    def remove(self, value: T) -> bool:
        if self._head.forward[0] is None:
            return False

        current_level: int = self._head.current_level
        update: list[SkipList.Node | None] = \
            [None] * (current_level + 1)
        current_node: SkipList.Node = self._head
        next_node: SkipList.Node | None
        value_found: bool = False

        while True:
            while True:
                next_node = current_node.forward[current_level]

                if next_node is None or next_node.value is None:
                    break

                if value == next_node.value:
                    value_found = True
                    break
                elif value > next_node.value:
                    current_node = next_node
                else:
                    break

            update[current_level] = current_node

            if current_level == 0:
                break

            current_level -= 1

        if value_found == False:
            return False

        for level in range(self._head.current_level + 1):
            prev: SkipList.Node | None = update[level]

            if prev is None:
                continue

            next_node = prev.forward[level]

            if next_node is None or next_node.value is None:
                continue

            if value != next_node.value:
                break

            prev.forward[level] = next_node.forward[level]

        for level in range(self._head.current_level, -1, -1):
            if self._head.forward[level] is None:
                self._head.current_level -= 1

        self._size -= 1

        return True

    def retrieve(self, value: T) -> bool:
        if self._head.forward[0] is None:
            return False

        current_level: int = self._head.current_level
        current_node: SkipList.Node = self._head

        while True:
            while True:
                next_node: SkipList.Node | None = \
                    current_node.forward[current_level]

                if next_node is None or next_node.value is None:
                    break

                if value == next_node.value:
                    return True
                elif value > next_node.value:
                    current_node = next_node
                else:
                    break

            if current_level == 0:
                break

            current_level -= 1

        return False

    def _random_level(self) -> int:
        level: int = 0

        while level < self._max_level and random.random() < self._p:
            level += 1

        return level
