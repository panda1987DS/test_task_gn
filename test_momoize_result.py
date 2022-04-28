import pytest
from datetime import datetime
from memoize_result import memoize_result
import pickle

@memoize_result()
def default(par1, par2):
    return datetime.now()


@memoize_result()
def for_clean(par1, par2):
    return datetime.now()


@memoize_result(maxsize=2)
def max_size(par1):
    return datetime.now()


@memoize_result(dump_memo=True)
def dump_memo(par1):
    return datetime.now()


def test_momoize_any():
    result_1_1 = default(1, 2)
    result_2_1 = default(3, 2)
    result_1_2 = default(1, 2)
    result_2_2 = default(3, 2)
    assert result_1_1 == result_1_2
    assert result_2_1 == result_2_2
    assert result_1_1 != result_2_1


def test_clean():
    assert len(for_clean) == 0
    for_clean(1, 2)
    for_clean(3, 2)
    assert len(for_clean) == 2
    for_clean.clean()
    assert len(for_clean) == 0


def test_unhashable_type():
     default({1: 1, 2: 2}, 2)


def test_max_size():
    result_1 = max_size(1)
    result_2 = max_size(2)
    assert result_1 == max_size(1)
    result_3 = max_size(3)
    assert result_1 != max_size(1)
    assert result_3 == max_size(3)


def test_dump_memo():
    result = dump_memo("test")
    with open(dump_memo.path, 'rb') as handle:
        memo = pickle.load(handle)
    assert result == memo[("test",)]


def test_print():
    default.print()
