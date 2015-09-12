from extensions.itertools import *
from extensions.itertools import _cross_off
from py.test import raises

def test_all_up_to():
    assert [[]] == list(all_up_to([]))
    assert [[0]] == list(all_up_to([0]))
    actual = list(all_up_to([1]))
    assert [0] in actual
    assert [1] in actual
    assert [[0, 0, 0, 0]] == list(all_up_to([0, 0, 0, 0]))
    correct = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0],
               [1, 0, 1], [1, 1, 0], [1, 1, 1]]
    actual = list(all_up_to([1, 1, 1]))
    assert len(correct) == len(actual)
    for item in correct:
        assert item in actual
    correct += [[0, 0, 2], [0, 1, 2], [1, 0, 2], [1, 1, 2], [2, 0, 0],
                [2, 0, 1], [2, 0, 2], [2, 1, 0], [2, 1, 1], [2, 1, 2]]
    actual = list(all_up_to([2, 1, 2]))
    assert len(correct) == len(actual)
    for item in correct:
        assert item in actual

def test_binary_numbers():
    assert 0 == len(list(binary_numbers(0)))
    for i in xrange(1, 10):
        assert 2 ** i == len(list(binary_numbers(i)))

def test_cross_off():
    assert (2, [3, 5, 7, 9]) == _cross_off(range(2, 11))
    assert (3, [5, 7]) == _cross_off([3, 5, 7, 9])

def test_primes():
    assert [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
            67, 71, 73, 79, 83, 89, 97] == list(primes(100))

def test_slices():
    correct = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
    assert correct == list(slices(range(16), 4))
    assert [[0, 1]] == list(slices([0, 1], 4))
    assert [] == list(slices([], 4))

def test_strict_slices():
    correct = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
    assert correct == list(strict_slices(range(16), 4))
    raises(TypeError, strict_slices, ([0, 1], 4))
    assert [] == list(strict_slices([], 4))

def test_two_finger():
    sequence = [1, 3, 9, 5, 22, 11]
    correct = [(1, 3), (3, 9), (9, 5), (5, 22), (22, 11)]
    assert correct == list(two_finger(sequence))
