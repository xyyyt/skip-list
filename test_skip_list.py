from skip_list import SkipList
import pytest

def patch_random(
        monkeypatch: pytest.MonkeyPatch, values: list[float]) -> None:
    """
    Patch skiplist.random.random to yield values in order,
    making randomness deterministic for tests.
    """

    it = iter(values)
    monkeypatch.setattr("skip_list.random.random", lambda: next(it))

def test_case_1(monkeypatch: pytest.MonkeyPatch) -> None:
    skip_list: SkipList[int] = SkipList[int]()

    assert len(skip_list) == 0
    assert bool(skip_list) == False
    assert skip_list.promotion_probability == 0.5
    assert skip_list.max_level == 32
    assert skip_list.size == 0
    assert skip_list.current_level == -1
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is None
    assert skip_list.retrieve(3) == False
    assert skip_list.remove(3) == False

    patch_random(monkeypatch, [0.2, 0.4, 1])

    assert skip_list.insert(3) == True

    #           Skip list status
    #
    # Level 2:  [Head] -> [3] -> [None]
    #              │       |
    # Level 1:  [Head] -> [3] -> [None]
    #              │       │
    # Level 0:  [Head] -> [3] -> [None]

    assert len(skip_list) == 1
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 0.5
    assert skip_list.max_level == 32
    assert skip_list.size == 1
    assert skip_list.current_level == 2
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [3]
    assert list(skip_list.iter_from(1)) == [3]
    assert list(skip_list.iter_from(2)) == [3]
    assert skip_list.retrieve(3) == True
    assert skip_list.retrieve(8) == False
    assert skip_list.remove(8) == False

    patch_random(monkeypatch, [0.5])

    assert skip_list.insert(8) == True

    #           Skip list status
    #
    # Level 2:  [Head] -> [3] -> [None]
    #              │       |
    # Level 1:  [Head] -> [3] -> [None]
    #              │       │
    # Level 0:  [Head] -> [3] --> [8] ---> [None]

    assert len(skip_list) == 2
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 0.5
    assert skip_list.max_level == 32
    assert skip_list.size == 2
    assert skip_list.current_level == 2
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [3, 8]
    assert list(skip_list.iter_from(1)) == [3]
    assert list(skip_list.iter_from(2)) == [3]
    assert skip_list.retrieve(8) == True
    assert skip_list.retrieve(-1) == False
    assert skip_list.remove(-1) == False

    patch_random(monkeypatch, [0.07, 0.74])

    assert skip_list.insert(-1) == True

    #           Skip list status
    #
    # Level 2:  [Head] ---------> [3] -> [None]
    #              │               |
    # Level 1:  [Head] -> [-1] -> [3] -> [None]
    #              │       │       |
    # Level 0:  [Head] -> [-1] -> [3] --> [8] --> [None]

    assert len(skip_list) == 3
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 0.5
    assert skip_list.max_level == 32
    assert skip_list.size == 3
    assert skip_list.current_level == 2
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [-1, 3, 8]
    assert list(skip_list.iter_from(1)) == [-1, 3]
    assert list(skip_list.iter_from(2)) == [3]
    assert skip_list.retrieve(-1) == True

    assert skip_list.remove(3) == True

    #           Skip list status
    #
    # Level 1:  [Head] -> [-1] -> [None]
    #              │       │
    # Level 0:  [Head] -> [-1] --> [8] --> [None]

    assert len(skip_list) == 2
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 0.5
    assert skip_list.max_level == 32
    assert skip_list.size == 2
    assert skip_list.current_level == 1
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [-1, 8]
    assert list(skip_list.iter_from(1)) == [-1]
    assert skip_list.retrieve(3) == False

    assert skip_list.remove(-1) == True

    #           Skip list status
    #
    # Level 0:  [Head] -> [8] -> [None]

    assert len(skip_list) == 1
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 0.5
    assert skip_list.max_level == 32
    assert skip_list.size == 1
    assert skip_list.current_level == 0
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [8]
    assert skip_list.retrieve(-1) == False

    assert skip_list.remove(8) == True

    #           Skip list status : Empty

    assert len(skip_list) == 0
    assert bool(skip_list) == False
    assert skip_list.promotion_probability == 0.5
    assert skip_list.max_level == 32
    assert skip_list.size == 0
    assert skip_list.current_level == -1
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is None
    assert skip_list.retrieve(8) == False

def test_case_2(monkeypatch: pytest.MonkeyPatch) -> None:
    skip_list: SkipList[int] = SkipList[int](
        promotion_probability=0.8,
        max_level=6)

    assert len(skip_list) == 0
    assert bool(skip_list) == False
    assert skip_list.promotion_probability == 0.8
    assert skip_list.max_level == 6
    assert skip_list.size == 0
    assert skip_list.current_level == -1
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is None
    assert skip_list.retrieve(-37) == False
    assert skip_list.remove(-37) == False

    patch_random(monkeypatch, [0.802])

    assert skip_list.insert(-37) == True

    #           Skip list status
    #
    # Level 0:  [Head] -> [-37] -> [None]

    assert len(skip_list) == 1
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 0.8
    assert skip_list.max_level == 6
    assert skip_list.size == 1
    assert skip_list.current_level == 0
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [-37]
    assert skip_list.retrieve(-37) == True
    assert skip_list.retrieve(-70) == False
    assert skip_list.remove(-70) == False

    patch_random(monkeypatch, [0.3, 0.0001, 0.14, 0.67, 0.512, 0.98])

    assert skip_list.insert(-70) == True

    #           Skip list status
    #
    # Level 5:  [Head] -> [-70] -> [None]
    #                       |
    # Level 4:  [Head] -> [-70] -> [None]
    #                       |
    # Level 3:  [Head] -> [-70] -> [None]
    #                       |
    # Level 2:  [Head] -> [-70] -> [None]
    #                       |
    # Level 1:  [Head] -> [-70] -> [None]
    #                       |
    # Level 0:  [Head] -> [-70] -> [-37] -> [None]

    assert len(skip_list) == 2
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 0.8
    assert skip_list.max_level == 6
    assert skip_list.size == 2
    assert skip_list.current_level == 5
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [-70, -37]
    assert list(skip_list.iter_from(1)) == [-70]
    assert list(skip_list.iter_from(2)) == [-70]
    assert list(skip_list.iter_from(3)) == [-70]
    assert list(skip_list.iter_from(4)) == [-70]
    assert list(skip_list.iter_from(5)) == [-70]
    assert skip_list.retrieve(-70) == True
    assert skip_list.retrieve(-52) == False
    assert skip_list.remove(-52) == False

    patch_random(monkeypatch, [0.52, 0.79, 0.8])

    assert skip_list.insert(-52) == True

    #           Skip list status
    #
    # Level 5:  [Head] -> [-70] -> [None]
    #                       |
    # Level 4:  [Head] -> [-70] -> [None]
    #                       |
    # Level 3:  [Head] -> [-70] -> [None]
    #                       |
    # Level 2:  [Head] -> [-70] -> [-52] -> [None]
    #                       |        |
    # Level 1:  [Head] -> [-70] -> [-52] -> [None]
    #                       |        |
    # Level 0:  [Head] -> [-70] -> [-52] -> [-37] --> [None]

    assert len(skip_list) == 3
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 0.8
    assert skip_list.max_level == 6
    assert skip_list.size == 3
    assert skip_list.current_level == 5
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [-70, -52, -37]
    assert list(skip_list.iter_from(1)) == [-70, -52]
    assert list(skip_list.iter_from(2)) == [-70, -52]
    assert list(skip_list.iter_from(3)) == [-70]
    assert list(skip_list.iter_from(4)) == [-70]
    assert list(skip_list.iter_from(5)) == [-70]
    assert skip_list.retrieve(-52) == True
    assert skip_list.retrieve(6) == False
    assert skip_list.remove(6) == False

    patch_random(monkeypatch, [1.0])

    assert skip_list.insert(6) == True

    #           Skip list status
    #
    # Level 5:  [Head] -> [-70] -> [None]
    #                       |
    # Level 4:  [Head] -> [-70] -> [None]
    #                       |
    # Level 3:  [Head] -> [-70] -> [None]
    #                       |
    # Level 2:  [Head] -> [-70] -> [-52] -> [None]
    #                       |        |
    # Level 1:  [Head] -> [-70] -> [-52] -> [None]
    #                       |        |
    # Level 0:  [Head] -> [-70] -> [-52] -> [-37] --> [6] -> [None]

    assert len(skip_list) == 4
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 0.8
    assert skip_list.max_level == 6
    assert skip_list.size == 4
    assert skip_list.current_level == 5
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [-70, -52, -37, 6]
    assert list(skip_list.iter_from(1)) == [-70, -52]
    assert list(skip_list.iter_from(2)) == [-70, -52]
    assert list(skip_list.iter_from(3)) == [-70]
    assert list(skip_list.iter_from(4)) == [-70]
    assert list(skip_list.iter_from(5)) == [-70]
    assert skip_list.retrieve(6) == True

    assert skip_list.remove(-52) == True

    #           Skip list status
    #
    # Level 5:  [Head] -> [-70] -> [None]
    #                       |
    # Level 4:  [Head] -> [-70] -> [None]
    #                       |
    # Level 3:  [Head] -> [-70] -> [None]
    #                       |
    # Level 2:  [Head] -> [-70] -> [None]
    #                       |        |
    # Level 1:  [Head] -> [-70] -> [None]
    #                       |        |
    # Level 0:  [Head] -> [-70] -> [-37] --> [6] -> [None]

    assert len(skip_list) == 3
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 0.8
    assert skip_list.max_level == 6
    assert skip_list.size == 3
    assert skip_list.current_level == 5
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [-70, -37, 6]
    assert list(skip_list.iter_from(1)) == [-70]
    assert list(skip_list.iter_from(2)) == [-70]
    assert list(skip_list.iter_from(3)) == [-70]
    assert list(skip_list.iter_from(4)) == [-70]
    assert list(skip_list.iter_from(5)) == [-70]
    assert skip_list.retrieve(-52) == False

    assert skip_list.remove(-70) == True

    #           Skip list status
    #
    # Level 0:  [Head] -> [-37] --> [6] -> [None]

    assert len(skip_list) == 2
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 0.8
    assert skip_list.max_level == 6
    assert skip_list.size == 2
    assert skip_list.current_level == 0
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [-37, 6]
    assert skip_list.retrieve(-70) == False

    assert skip_list.remove(-37) == True

    #           Skip list status
    #
    # Level 0:  [Head] -> [6] -> [None]

    assert len(skip_list) == 1
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 0.8
    assert skip_list.max_level == 6
    assert skip_list.size == 1
    assert skip_list.current_level == 0
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [6]
    assert skip_list.retrieve(-37) == False

    assert skip_list.remove(6) == True

    #           Skip list status : Empty

    assert len(skip_list) == 0
    assert bool(skip_list) == False
    assert skip_list.promotion_probability == 0.8
    assert skip_list.max_level == 6
    assert skip_list.size == 0
    assert skip_list.current_level == -1
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is None
    assert skip_list.retrieve(6) == False

def test_case_3(monkeypatch: pytest.MonkeyPatch) -> None:
    skip_list: SkipList[int] = SkipList[int](
        promotion_probability=0.3,
        max_level=3)

    assert len(skip_list) == 0
    assert bool(skip_list) == False
    assert skip_list.promotion_probability == 0.3
    assert skip_list.max_level == 3
    assert skip_list.size == 0
    assert skip_list.current_level == -1
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is None
    assert skip_list.retrieve(6) == False
    assert skip_list.remove(6) == False

    patch_random(monkeypatch, [0.2, 0.1, 0.29, 0.22, 0.001])

    assert skip_list.insert(42) == True

    #           Skip list status
    #
    # Level 3:  [Head] -> [42] -> [None]
    #                      |
    # Level 2:  [Head] -> [42] -> [None]
    #              │       |
    # Level 1:  [Head] -> [42] -> [None]
    #              │       │
    # Level 0:  [Head] -> [42] -> [None]

    assert len(skip_list) == 1
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 0.3
    assert skip_list.max_level == 3
    assert skip_list.size == 1
    assert skip_list.current_level == 3
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [42]
    assert list(skip_list.iter_from(1)) == [42]
    assert list(skip_list.iter_from(2)) == [42]
    assert list(skip_list.iter_from(3)) == [42]
    assert skip_list.retrieve(42) == True
    assert skip_list.retrieve(31) == False
    assert skip_list.remove(31) == False

    patch_random(monkeypatch, [0.67])

    assert skip_list.insert(31) == True

    #           Skip list status
    #
    # Level 3:  [Head] ---------> [42] -> [None]
    #              |               |
    # Level 2:  [Head] ---------> [42] -> [None]
    #              │               |
    # Level 1:  [Head] ---------> [42] -> [None]
    #              │               |
    # Level 0:  [Head] -> [31] -> [42] -> [None]

    assert len(skip_list) == 2
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 0.3
    assert skip_list.max_level == 3
    assert skip_list.size == 2
    assert skip_list.current_level == 3
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [31, 42]
    assert list(skip_list.iter_from(1)) == [42]
    assert list(skip_list.iter_from(2)) == [42]
    assert list(skip_list.iter_from(3)) == [42]
    assert skip_list.retrieve(31) == True
    assert skip_list.retrieve(5) == False
    assert skip_list.remove(5) == False

    patch_random(
        monkeypatch, [0.000, 0.05, 0.17, 0.24, 0.12, 0.001, 0.28, 0.93])

    assert skip_list.insert(5) == True

    #           Skip list status
    #
    # Level 3:  [Head] -> [5] ---------> [42] -> [None]
    #                      |              |
    # Level 2:  [Head] -> [5] ---------> [42] -> [None]
    #              │       |              |
    # Level 1:  [Head] -> [5] ---------> [42] -> [None]
    #              │       |              |
    # Level 0:  [Head] -> [5] -> [31] -> [42] -> [None]

    assert len(skip_list) == 3
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 0.3
    assert skip_list.max_level == 3
    assert skip_list.size == 3
    assert skip_list.current_level == 3
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [5, 31, 42]
    assert list(skip_list.iter_from(1)) == [5, 42]
    assert list(skip_list.iter_from(2)) == [5, 42]
    assert list(skip_list.iter_from(3)) == [5, 42]
    assert skip_list.retrieve(5) == True

    assert skip_list.remove(31) == True

    #           Skip list status
    #
    # Level 3:  [Head] -> [5] -> [42] -> [None]
    #              |       |      |
    # Level 2:  [Head] -> [5] -> [42] -> [None]
    #              │       |      |
    # Level 1:  [Head] -> [5] -> [42] -> [None]
    #              │       |      |
    # Level 0:  [Head] -> [5] -> [42] -> [None]

    assert len(skip_list) == 2
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 0.3
    assert skip_list.max_level == 3
    assert skip_list.size == 2
    assert skip_list.current_level == 3
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [5, 42]
    assert list(skip_list.iter_from(1)) == [5, 42]
    assert list(skip_list.iter_from(2)) == [5, 42]
    assert list(skip_list.iter_from(3)) == [5, 42]
    assert skip_list.retrieve(31) == False

    assert skip_list.remove(42) == True

    #           Skip list status
    #
    # Level 2:  [Head] -> [5] -> [None]
    #              |       |
    # Level 2:  [Head] -> [5] -> [None]
    #              │       |
    # Level 1:  [Head] -> [5] -> [None]
    #              │       |
    # Level 0:  [Head] -> [5] -> [None]

    assert len(skip_list) == 1
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 0.3
    assert skip_list.max_level == 3
    assert skip_list.size == 1
    assert skip_list.current_level == 3
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [5]
    assert list(skip_list.iter_from(1)) == [5]
    assert list(skip_list.iter_from(2)) == [5]
    assert list(skip_list.iter_from(3)) == [5]
    assert skip_list.retrieve(42) == False

    assert skip_list.remove(5) == True

    #           Skip list status : Empty

    assert len(skip_list) == 0
    assert bool(skip_list) == False
    assert skip_list.promotion_probability == 0.3
    assert skip_list.max_level == 3
    assert skip_list.size == 0
    assert skip_list.current_level == -1
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is None
    assert skip_list.retrieve(5) == False

def test_case_4(monkeypatch: pytest.MonkeyPatch) -> None:
    skip_list: SkipList[int] = SkipList[int](
        promotion_probability=1.0,
        max_level=0)

    assert len(skip_list) == 0
    assert bool(skip_list) == False
    assert skip_list.promotion_probability == 1.0
    assert skip_list.max_level == 0
    assert skip_list.size == 0
    assert skip_list.current_level == -1
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is None
    assert skip_list.retrieve(82) == False
    assert skip_list.remove(82) == False

    patch_random(monkeypatch, [0.9456, 0.487, 0.125])

    assert skip_list.insert(82) == True

    #           Skip list status
    #
    # Level 0:  [Head] -> [82] -> [None]

    assert len(skip_list) == 1
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 1.0
    assert skip_list.max_level == 0
    assert skip_list.size == 1
    assert skip_list.current_level == 0
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [82]
    assert skip_list.retrieve(82) == True
    assert skip_list.retrieve(127) == False
    assert skip_list.remove(127) == False

    patch_random(monkeypatch, [])

    assert skip_list.insert(127) == True

    #           Skip list status
    #
    # Level 0:  [Head] -> [82] -> [127] -> [None]

    assert len(skip_list) == 2
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 1.0
    assert skip_list.max_level == 0
    assert skip_list.size == 2
    assert skip_list.current_level == 0
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [82, 127]
    assert skip_list.retrieve(127) == True
    assert skip_list.retrieve(255) == False
    assert skip_list.remove(255) == False

    patch_random(monkeypatch, [0.97, 0.4143, 0.003, 0.450, 1.0])

    assert skip_list.insert(255) == True

    #           Skip list status
    #
    # Level 0:  [Head] -> [82] -> [127] -> [255] -> [None]

    assert len(skip_list) == 3
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 1.0
    assert skip_list.max_level == 0
    assert skip_list.size == 3
    assert skip_list.current_level == 0
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [82, 127, 255]
    assert skip_list.retrieve(255) == True

    assert skip_list.remove(82) == True

    #           Skip list status
    #
    # Level 0:  [Head] -> [127] -> [255] -> [None]

    assert len(skip_list) == 2
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 1.0
    assert skip_list.max_level == 0
    assert skip_list.size == 2
    assert skip_list.current_level == 0
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [127, 255]
    assert skip_list.retrieve(82) == False

    assert skip_list.remove(255) == True

    #           Skip list status
    #
    # Level 0:  [Head] -> [127] -> [None]

    assert len(skip_list) == 1
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 1.0
    assert skip_list.max_level == 0
    assert skip_list.size == 1
    assert skip_list.current_level == 0
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [127]
    assert skip_list.retrieve(255) == False

    assert skip_list.remove(127) == True

    #           Skip list status : Empty

    assert len(skip_list) == 0
    assert bool(skip_list) == False
    assert skip_list.promotion_probability == 1.0
    assert skip_list.max_level == 0
    assert skip_list.size == 0
    assert skip_list.current_level == -1
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is None
    assert skip_list.retrieve(127) == False

def test_case_5(monkeypatch: pytest.MonkeyPatch) -> None:
    skip_list: SkipList[int] = SkipList[int](
        promotion_probability=0.0,
        max_level=57)

    assert len(skip_list) == 0
    assert bool(skip_list) == False
    assert skip_list.promotion_probability == 0.0
    assert skip_list.max_level == 57
    assert skip_list.size == 0
    assert skip_list.current_level == -1
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is None
    assert skip_list.retrieve(1) == False
    assert skip_list.remove(1) == False

    patch_random(monkeypatch, [1, 0.97, 0.5, 0.87654])

    assert skip_list.insert(1) == True

    #           Skip list status
    #
    # Level 0:  [Head] -> [1] -> [None]

    assert len(skip_list) == 1
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 0.0
    assert skip_list.max_level == 57
    assert skip_list.size == 1
    assert skip_list.current_level == 0
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [1]
    assert skip_list.retrieve(1) == True
    assert skip_list.retrieve(0) == False
    assert skip_list.remove(0) == False

    patch_random(monkeypatch, [0.2])

    assert skip_list.insert(0) == True

    #           Skip list status
    #
    # Level 0:  [Head] -> [0] -> [1] -> [None]

    assert len(skip_list) == 2
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 0.0
    assert skip_list.max_level == 57
    assert skip_list.size == 2
    assert skip_list.current_level == 0
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [0, 1]
    assert skip_list.retrieve(0) == True
    assert skip_list.retrieve(2) == False
    assert skip_list.remove(2) == False

    patch_random(
        monkeypatch, [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0])

    assert skip_list.insert(2) == True

    #           Skip list status
    #
    # Level 0:  [Head] -> [0] -> [1] -> [2] [None]

    assert len(skip_list) == 3
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 0.0
    assert skip_list.max_level == 57
    assert skip_list.size == 3
    assert skip_list.current_level == 0
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [0, 1, 2]
    assert skip_list.retrieve(0) == True

    assert skip_list.remove(0) == True

    #           Skip list status
    #
    # Level 0:  [Head] -> [1] -> [2] [None]

    assert len(skip_list) == 2
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 0.0
    assert skip_list.max_level == 57
    assert skip_list.size == 2
    assert skip_list.current_level == 0
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [1, 2]
    assert skip_list.retrieve(0) == False

    assert skip_list.remove(1) == True

    #           Skip list status
    #
    # Level 0:  [Head] -> [2] [None]

    assert len(skip_list) == 1
    assert bool(skip_list) == True
    assert skip_list.promotion_probability == 0.0
    assert skip_list.max_level == 57
    assert skip_list.size == 1
    assert skip_list.current_level == 0
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is not None
    assert list(skip_list.iter_from(0)) == [2]
    assert skip_list.retrieve(1) == False

    assert skip_list.remove(2) == True

    #           Skip list status : Empty

    assert len(skip_list) == 0
    assert bool(skip_list) == False
    assert skip_list.promotion_probability == 0.0
    assert skip_list.max_level == 57
    assert skip_list.size == 0
    assert skip_list.current_level == -1
    assert len(skip_list._head.forward) == skip_list.max_level + 1
    assert skip_list._head.forward[0] is None
    assert skip_list.retrieve(2) == False

def test_case_6() -> None:
    with pytest.raises(ValueError):
        SkipList[int](promotion_probability=-1.0)

    with pytest.raises(ValueError):
        SkipList[int](promotion_probability=2.0)

    with pytest.raises(ValueError):
        SkipList[int](max_level=-1)

    with pytest.raises(ValueError):
        next(SkipList[int]().iter_from(level=-1))

    with pytest.raises(ValueError):
        next(SkipList[int]().iter_from(level=1))
