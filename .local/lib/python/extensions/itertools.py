"""Functional tools for creating and using iterators."""

def all_up_to(counts):
    """Generate a list of all the numbers in the items up to the value in each
    slot."""
    if len(counts) == 0:
        yield []
    else:
        for i in xrange(counts[0] + 1):
            for partial in all_up_to(counts[1:]):
                yield [i] + partial

def binary_numbers(length):
    """Construct all possible binary numbers of the given length."""
    if length < 1:
        return
    elif length == 1:
        yield [0]
        yield [1]
    else:
        for path in binary_numbers(length - 1):
            yield [0] + path
            yield [1] + path

def combinations_with_replacement(iterable, r):
    "combinations_with_replacement('ABC', 2) --> AA AB AC BB BC CC"
    # number items returned:  (n+r-1)! / r! / (n-1)!
    pool = tuple(iterable)
    n = len(pool)
    if not n and r:
        return
    indices = [0] * r
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != n - 1:
                break
        else:
            return
        indices[i:] = [indices[i] + 1] * (r - i)
        yield tuple(pool[i] for i in indices)

def compress(data, selectors):
    "compress('ABCDEF', [1,0,1,0,1,1]) --> A C E F"
    return (d for d, s in izip(data, selectors) if s)

def consume(iterator, n):
    "Advance the iterator n-steps ahead. If n is none, consume entirely."
    collections.deque(islice(iterator, n), maxlen=0)

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def ncycles(iterable, n):
    "Returns the sequence elements n times"
    return chain.from_iterable(repeat(iterable, n))

def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    return next(islice(iterable, n, None), default)

def padnone(iterable):
    """Returns the sequence elements and then returns None indefinitely.

    Useful for emulating the behavior of the built-in map() function.
    """
    return chain(iterable, repeat(None))

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def reorder(sequence, ordering):
    """Reorder the given sequence using the given ordering.  Note that if
    ordering is an r-length list containing no repeated items, it is an
    r-permutation of sequence."""
    for index in ordering:
        yield sequence[index]

def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = cycle(iter(it).next for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))

def slices(sequence, slice_size):
    """Generate a series of non-overlapping sequence slices of arbitrary
    size."""
    for i in xrange(len(sequence) / slice_size + 1):
        if i * slice_size == len(sequence):
            return
        yield sequence[i*slice_size:(i+1)*slice_size]

def strict_slices(sequence, slice_size):
    if len(sequence) % slice_size != 0:
        raise TypeError("A sequence with " + str(len(sequence)) + " items " +
                        "cannot generate a sequence of " + str(slice_size) +
                        "-slices.")
    return slices(sequence, slice_size)

def unique_everseen(iterable, key=None):
    """List unique elements, preserving order. Remember all elements ever seen.
    >>> unique_everseen('AAAABBBCCDAABBB')
    ['A', 'B', 'C', 'D']
    >>> unique_everseen('ABBCcAD', str.lower) --> A B C D
    ['A', 'B', 'C', 'D']"""
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in iterable:
            if element not in seen:
                seen_add(element)
                yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element

def unique_justseen(iterable, key=None):
    """List unique elements, preserving order. Remember only the element just
    seen.
    >>> list(unique_justseen('AAAABBBCCDAABBB'))
    ['A', 'B', 'C', 'D', 'A', 'B']
    >>> list(unique_justseen('ABBCcAD', str.lower))
    ['A', 'B', 'C', 'A', 'D']"""
    return imap(next, imap(itemgetter(1), groupby(iterable, key)))

#******************************************************************************
#********************************* UNIT TESTS *********************************
#******************************************************************************

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
