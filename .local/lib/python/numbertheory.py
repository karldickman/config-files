#Aggregated from several sources

###############################################################################
# NUMBTHY.PY
# Basic Number Theory functions implemented in Python
# Note: Currently requires Python 2.x (uses +=, %= and other 2.x-isms)
# Note: Currently requires Python 2.3 (uses implicit long integers - could be
#       back-ported though)
# Author: Robert Campbell, <campbell@math.umbc.edu>
# Date: 27 April, 2007
# Version 0.41
###############################################################################

##################################################
# ent.py -- Element Number Theory
# (c) William Stein, 2004
##################################################

#TODO: Sections (GCD, Enumerating primes, Integer factorization, Linear
#equations modulo $n$, Computations of powers, primitive roots, primality
#testing, Legendere
"""Common problems in arithmetic and number theory."""

from extensions.itertools import all_up_to
from itertools import imap
from operator import mul
from math import floor, sqrt

def divisors(number):
    """divisors(number) -> All the divisors of the given number."""
    if number < 0:
        positive = divisors(-number)
        negative = [-divisor for divisor in reversed(positive)]
        return negative + positive
    elif number == 0:
        raise Exception
    elif number == 1:
        return [1]
    factorization = prime_factorization(number)
    factors = [item[0] for item in factorization]
    exponents = [item[1] for item in factorization]
    found = []
    for exponent_combo in all_up_to(exponents):
        found.append(reduce(mul, (factor ** exponent for factor, exponent
                             in zip(factors, exponent_combo))))
    return sorted(found)

def dotproduct(vec1, vec2):
    """The dot-product of the given vectors."""
    return sum(imap(mul, vec1, vec2))

def crt(a, b, m, n):
    """
    Return the unique integer between 0 and m*n - 1
    that reduces to a modulo n and b modulo m, where
    the integers m and n are coprime.
    Input:
        a, b, m, n -- integers, with m and n coprime
    Output:
        int -- an integer between 0 and m*n - 1.
    Examples:
    >>> crt(1, 2, 3, 4)
    10
    >>> crt(4, 5, 10, 3)
    14
    >>> crt(-1, -1, 100, 101)
    10099
    """
    g, c, _ = xgcd(m, n)
    assert g == 1, "m and n must be coprime."
    return (a + (b-a)*c*m) % (m*n)

def gcd(a, b):
    """gcd(a, b) returns the greatest common divisor of the integers a and
    b.
    >>> gcd(97, 100)
    1
    >>> gcd(97 * 10**15, 19**20 * 97**2)              # (2)
    97L"""
    if a == 0:
        return b
    if b == 0:
        return a
    return abs(gcd(b % a, a))

def factor(n):
    """
    Returns the factorization of the integer n as
    a sorted list of tuples (p, e), where the integers p
    are output by the split algorithm.
    Input:
        n -- an integer
    Output:
        list -- factorization of n
    Examples:
    >>> factor(500)
    [(2, 2), (5, 3)]
    >>> factor(-20)
    [(2, 2), (5, 1)]
    >>> factor(1)
    []
    >>> factor(2004)
    [(2, 2), (3, 1), (167, 1)]
    """
    if n in [-1, 0, 1]:
        return []
    if n < 0:
        n = -n
    F = []
    while n != 1:
        p = trial_division(n)
        e = 1
        n /= p
        while n % p == 0:
            e += 1
            n /= p
        F.append((p, e))
    F.sort()
    return F

def find_one_prime_factor(number):
    """find_one_prime_factor(number) - Find a prime find_one_prime_factor of number
    using a variety of methods."""
    if is_prime(number):
        return number
    for fact in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        if number % fact == 0:
            return fact
    # TODO No guarantee that a prime find_one_prime_factor will be returned
    return pollard_rho(number)

def is_euler_prime(number, base):
    """is_euler_prime(number) - Test whether number is prime or an Euler
    pseudoprime to base base."""
    if not is_fermat_prime(number, base):
        return False
    r = number-1
    while r % 2 == 0:
        r /= 2
    c = pow(base, r, number)
    if c == 1:
        return True
    while True:
        if c == 1:
            return False
        if c == number - 1:
            return True
        c = pow(c, 2, number)

def is_fermat_prime(number, base):
    """is_fermat_prime(number) - Test whether number is prime or a Fermat
    pseudoprime to base base."""
    return (pow(base, number-1, number) == 1)

def is_prime(number):
    """is_prime(number) - Test whether number is prime using a variety of
    pseudoprime tests."""
    if number in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        return True
    return (is_euler_prime(number, 2) and is_euler_prime(number, 3) and
            is_euler_prime(number, 5))

def is_primitive_root(candidate, modulus):
    """is_primitive_root(candidate, modulus) - Test whether candidate is
    primitive - generates the group of units mod modulus."""
    if gcd(candidate, modulus) != 1:
        return False  # Not in the group of units
    order = totient(modulus)
    if modular_order(modulus) != order:
        return False # Group of units isn't cyclic
    orderfacts = prime_factors(order)
    oldfact = 1
    for fact in orderfacts:
        if fact != oldfact:
            if pow(candidate, order/fact, modulus) == 1:
                return False
            oldfact = fact
    return True

def is_pseudoprime(n, bases=(2, 3, 5, 7)):
    """
    Returns True if n is a pseudoprime to the given bases,
    in the sense that n>1 and b**(n-1) = 1 (mod n) for each
    elements b of bases, with b not a multiple of n, and
    False otherwise.
    Input:
        n -- an integer
        bases -- a list of integers
    Output:
        bool
    Examples:
    >>> is_pseudoprime(91)
    False
    >>> is_pseudoprime(97)
    True
    >>> is_pseudoprime(1)
    False
    >>> is_pseudoprime(-2)
    True
    >>> s = [x for x in range(10000) if is_pseudoprime(x)]
    >>> t = primes(10000)
    >>> s == t
    True
    >>> is_pseudoprime(29341) # first non-prime pseudoprime
    True
    >>> factor(29341)
    [(13, 1), (37, 1), (61, 1)]
    """
    if n < 0:
        n = -n
    if n <= 1:
        return False
    for b in bases:
        if b % n != 0 and powermod(b, n-1, n) != 1:
            return False
    return True

def miller_rabin(n, num_trials=4):
    """
    True if n is likely prime, and False if n
    is definitely not prime.  Increasing num_trials
    increases the probability of correctness.
    (One can prove that the probability that this
    function returns True when it should return
    False is at most (1/4)**num_trials.)
    Input:
        n -- an integer
        num_trials -- the number of trials with the
                      primality test.
    Output:
        bool -- whether or not n is probably prime.
    Examples:
    >>> miller_rabin(91)
    False                         #rand
    >>> miller_rabin(97)
    True                          #rand
    >>> s = [x for x in range(1000) if miller_rabin(x, 1)]
    >>> t = primes(1000)
    >>> print len(s), len(t)  # so 1 in 25 wrong
    175 168                       #rand
    >>> s = [x for x in range(1000) if miller_rabin(x)]
    >>> s == t
    True                          #rand
    """
    if n < 0:
        n = -n
    if n in [2, 3]:
        return True
    if n <= 4:
        return False
    m = n - 1
    k = 0
    while m % 2 == 0:
        k += 1
        m /= 2
    # Now n - 1 = (2**k) * m with m odd
    for i in xrange(num_trials):
        a = randrange(2, n-1)                  # (1)
        apow = powermod(a, m, n)
        if not (apow in [1, n-1]):
            some_minus_one = False
            for j in range(k-1):              # (2)
                apow = (apow**2) % n
                if apow == n-1:
                    some_minus_one = True
                    break                     # (3)
        if (apow in [1, n-1]) or some_minus_one:
            prob_prime = True
        else:
            return False
    return True

def modular_order(number):
    """modular_order(number) - Computer Carmichael's Lambda function of number
    - the smallest exponent e such that b**e = 1 for all b coprime to number.
    Otherwise defined as the exponent of the group of integers mod number."""
    thefactors = prime_factors(number)
    thefactors.sort()
    thefactors += [0]  # Mark the end of the list of factors
    carlambda = 1 # The Carmichael Lambda function of number
    carlambda_comp = 1 # The Carmichael Lambda function of the component p**e
    oldfact = 1
    for fact in thefactors:
        if fact == oldfact:
            carlambda_comp = (carlambda_comp*fact)
        else:
            if (oldfact == 2) and (carlambda_comp >= 4):
                carlambda_comp /= 2 # Z_(2**e) is not cyclic for e>=3
            if carlambda == 1:
                carlambda = carlambda_comp
            else:
                div = gcd(carlambda, carlambda_comp)
                carlambda = (carlambda * carlambda_comp)/ div
            carlambda_comp = fact-1
            oldfact = fact
    return carlambda

def modular_power(base, exponent, modulus):
    """modular_power(base, exponent, modulus) computes the eth power of base
    mod modulus.  (Actually, this is not needed, as pow(base, exponent,
    modulus) does the same thing for positive integers.  This will be useful in
    future for non-integers or inverses."""
    accum = 1
    i = 0
    bpow2 = base
    while (exponent>>i) > 0:
        if (exponent>>i) & 1:
            accum = (accum*bpow2) % modulus
        bpow2 = (bpow2*bpow2) % modulus
        i += 1
    return accum

def lcm_to(B):
    """
    Returns the least common multiple of all
    integers up to B.
    Input:
        B -- an integer
    Output:
        an integer
    Examples:
    >>> lcm_to(5)
    60
    >>> lcm_to(20)
    232792560
    >>> lcm_to(100)
    69720375229712477164533808935312303556800L
    """
    ans = 1
    logB = log(B)
    for p in primes(B):
        ans *= p**int(logB/log(p))
    return ans

def legendre(a, p):
    """
    Returns the Legendre symbol a over p, where
    p is an odd prime.
    Input:
        a -- an integer
        p -- an odd prime (primality not checked)
    Output:
        int: -1 if a is not a square mod p,
              0 if gcd(a, p) is not 1
              1 if a is a square mod p.
    Examples:
    >>> legendre(2, 5)
    -1
    >>> legendre(3, 3)
    0
    >>> legendre(7, 2003)
    -1
    """
    assert p % 2 == 1, "p must be an odd prime."
    b = powermod(a, (p-1)/2, p)
    if b == 1:
        return 1
    elif b == p-1:
        return -1
    return 0

def pollard(N, m):
    """
    Use Pollard's (p-1)-method to try to find a
    nontrivial divisor of N.
    Input:
        N -- a positive integer
        m -- a positive integer, the least common
             multiple of the integers up to some
             bound, computed using lcm_to.
    Output:
        int -- an integer divisor of n
    Examples:
    >>> pollard(5917, lcm_to(5))
    61
    >>> pollard(779167, lcm_to(5))
    779167
    >>> pollard(779167, lcm_to(15))
    2003L
    >>> pollard(187, lcm_to(15))
    11
    >>> n = random_prime(5)*random_prime(5)*random_prime(5)
    >>> pollard(n, lcm_to(100))
    315873129119929L     #rand
    >>> pollard(n, lcm_to(1000))
    3672986071L          #rand
    """
    for a in [2, 3]:
        x = powermod(a, m, N) - 1
        g = gcd(x, N)
        if g != 1 and g != N:
            return g
    return N

def pollard_rho(number):
    """pollard_rho(number) - Find a find_one_prime_factor of number using the
    Pollard Rho method.  Note: This method will occasionally fail."""
    for slow in [2, 3, 4, 6]:
        numsteps = 2 * floor(sqrt(sqrt(number)))
        fast = slow
        i = 1
        while i < numsteps:
            slow = (slow*slow + 1) % number
            i = i + 1
            fast = (fast*fast + 1) % number
            fast = (fast*fast + 1) % number
            g = gcd(fast-slow, number)
            if g != 1:
                if g == number:
                    break
                else:
                    return g
    return 1

def powermod(a, m, n):
    """
    The m-th power of a modulo n.
    Input:
        a -- an integer
        m -- a nonnegative integer
        n -- a positive integer
    Output:
        int -- an integer between 0 and n-1
    Examples:
    >>> powermod(2, 25, 30)
    2
    >>> powermod(19, 12345, 100)
    99
    """
    assert m >= 0, "m must be nonnegative."   # (1)
    assert n >= 1, "n must be positive."      # (2)
    ans = 1
    apow = a
    while m != 0:
        if m % 2 != 0:
            ans = (ans * apow) % n            # (3)
        apow = (apow * apow) % n              # (4)
        m /= 2
    return ans % n

def prime_factors(number):
    """factors(number) - Return a sorted list of the prime factors of
    number."""
    if is_prime(number):
        return [number]
    fact = find_one_prime_factor(number)
    if fact == 1:
        return "Unable to find_one_prime_factor "+str(number)
    facts = prime_factors(number/fact) + prime_factors(fact)
    facts.sort()
    return facts

def prime_factorization(number):
    """Calculate the prime factorization of the given number."""
    if number < 0:
        raise ValueError
    elif number in (0, 1):
        return []
    root = int(sqrt(number))
    found = _prime_factorization(number, iter(primes(root)))
    if len(found) == 0:
        found = [(number, 1)]
    return found

def _prime_factorization(number, generator):
    while True:
        try:
            prime = next(generator)
        except StopIteration:
            return [(number, 1)] if number != 1 else []
        if number % prime == 0:
            power = 0
            while number % prime == 0:
                power += 1
                number /= prime
            return [(prime, power)] + _prime_factorization(number, generator)

def primes(n):
    """
    Returns a list of the primes up to n, computed
    using the Sieve of Eratosthenes.
    Input:
        n -- a positive integer
    Output:
        list -- a list of the primes up to n
    Examples:
    >>> primes(10)
    [2, 3, 5, 7]
    >>> primes(45)
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
    """
    if n <= 1:
        return []
    X = [i for i in range(3, n+1) if i % 2 != 0]
    P = [2]
    sqrt_n = sqrt(n)
    while len(X) > 0 and X[0] <= sqrt_n:
        p = X[0]
        P.append(p)
        X = [a for a in X if a % p != 0]
    return P + X

def primitive_root(p):
    """
    Returns first primitive root modulo the prime p.
    (If p is not prime, this return value of this function
    is not meaningful.)
    Input:
        p -- an integer that is assumed prime
    Output:
        int -- a primitive root modulo p
    Examples:
    >>> primitive_root(7)
    3
    >>> primitive_root(389)
    2
    >>> primitive_root(5881)
    31
    """
    if p == 2:
        return 1
    F = factor(p-1)
    a = 2
    while a < p:
        generates = True
        for q, _ in F:
            if powermod(a, (p-1)/q, p) == 1:
                generates = False
                break
        if generates:
            return a
        a += 1
    assert False, "p must be prime."

def power_of_factor(number, factor):
    """Calculate the power to which the factor occurs in number.  This is
    probably only useful for prime numbers."""
    power = 0
    while number % factor == 0:
        power += 1
        number /= factor
    return power

def solve_linear(a, b, n):
    """
    If the equation ax = b (mod n) has a solution, return a
    solution normalized to lie between 0 and n-1, otherwise
    returns None.
    Input:
        a -- an integer
        b -- an integer
        n -- an integer
    Output:
        an integer or None
    Examples:
    >>> solve_linear(4, 2, 10)
    8
    >>> solve_linear(2, 1, 4) == None
    True
    """
    g, c, _ = xgcd(a, n)                 # (1)
    if b % g != 0:
        return None
    return ((b/g)*c) % n

def sqrtmod(a, p):
    """
    Returns a square root of a modulo p.
    Input:
        a -- an integer that is a perfect
             square modulo p (this is checked)
        p -- a prime
    Output:
        int -- a square root of a, as an integer
               between 0 and p-1.
    Examples:
    >>> sqrtmod(4, 5)              # p == 1 (mod 4)
    3              #rand
    >>> sqrtmod(13, 23)            # p == 3 (mod 4)
    6              #rand
    >>> sqrtmod(997, 7304723089)   # p == 1 (mod 4)
    761044645L     #rand
    """
    a %= p
    if p == 2:
        return a
    assert legendre(a, p) == 1, "a must be a square mod p."
    if p % 4 == 3:
        return powermod(a, (p+1)/4, p)

    modmul = lambda x, y: ((x[0]*y[0] + a*y[1]*x[1]) % p,
                           (x[0]*y[1] + x[1]*y[0]) % p)
    def modpow(x, n):   # exponentiation in R       # (2)
        ans = (1, 0)
        xpow = x
        while n != 0:
            if n % 2 != 0:
                ans = modmul(ans, xpow)
            xpow = modmul(xpow, xpow)
            n /= 2
        return ans

    while True:
        z = randrange(2, p)
        u, v = modpow((1, z), (p-1)/2)
        if v != 0:
            vinv = inversemod(v, p)
            for x in [-u*vinv, (1-u)*vinv, (-1-u)*vinv]:
                if (x*x) % p == a:
                    return x % p
            assert False, "Bug in sqrtmod."

def totient(number):
    """totient(number) - Computer Euler's Phi function of number - the number
    of integers strictly less than number which are coprime to number.
    Otherwise defined as the order of the group of integers mod number."""
    thefactors = prime_factors(number)
    thefactors.sort()
    phi = 1
    oldfact = 1
    for fact in thefactors:
        if fact == oldfact:
            phi = phi*fact
        else:
            phi = phi*(fact-1)
            oldfact = fact
    return phi

def trial_division(n, bound=None):
    """
    Return the smallest prime divisor <= bound of the
    positive integer n, or n if there is no such prime.
    If the optional argument bound is omitted, then bound=n.
    Input:
        n -- a positive integer
        bound - (optional) a positive integer
    Output:
        int -- a prime p<=bound that divides n, or n if
               there is no such prime.
    Examples:
    """
    if n == 1:
        return 1
    for p in [2, 3, 5]:
        if n % p == 0:
            return p
    if bound == None:
        bound = n
    dif = [6, 4, 2, 4, 2, 4, 6, 2]
    m = 7
    i = 1
    while m <= bound and m*m <= n:
        if n % m == 0:
            return m
        m += dif[i % 8]
        i += 1
    return n

def xgcd(a, b):
    """
    Returns g, x, y such that g = x*a + y*b = gcd(a, b).
    Input:
        a -- an integer
        b -- an integer
    Output:
        g -- an integer, the gcd of a and b
        x -- an integer
        y -- an integer
    Examples:
    >>> xgcd(2, 3)
    (1, -1, 1)
    >>> xgcd(10, 12)
    (2, -1, 1)
    >>> g, x, y = xgcd(100, 2004)
    >>> print g, x, y
    4 -20 1
    >>> print x*100 + y*2004
    4
    """
    if a == 0 and b == 0:
        return (0, 0, 1)
    if a == 0:
        return (abs(b), 0, b/abs(b))
    if b == 0:
        return (abs(a), a/abs(a), 0)
    x_sign = 1
    y_sign = 1
    if a < 0:
        a = -a
        x_sign = -1
    if b < 0:
        b = -b
        y_sign = -1
    x = 1
    y = 0
    r = 0
    s = 1
    while b != 0:
        (c, q) = (a % b, a/b)
        (a, b, r, s, x, y) = (b, c, x-q*r, y-q*s, r, s)
    return (a, x*x_sign, y*y_sign)

##################################################
## Continued Fractions
##################################################

def convergents(v):
    """
    Returns the partial convergents of the continued
    fraction v.
    Input:
        v -- list of integers [a0, a1, a2, ..., am]
    Output:
        list -- list [(p0, q0), (p1, q1), ...]
                of pairs (pm, qm) such that the mth
                convergent of v is pm/qm.
    Examples:
    >>> convergents([1, 2])
    [(1, 1), (3, 2)]
    >>> convergents([3, 7, 15, 1, 292])
    [(3, 1), (22, 7), (333, 106), (355, 113), (103993, 33102)]
    """
    w = [(0, 1), (1, 0)]
    for n in range(len(v)):
        pn = v[n]*w[n+1][0] + w[n][0]
        qn = v[n]*w[n+1][1] + w[n][1]
        w.append((pn, qn))
    del w[0]
    del w[0]  # remove first entries of w
    return w

def contfrac_rat(numer, denom):
    """
    Returns the continued fraction of the rational
    number numer/denom.
    Input:
        numer -- an integer
        denom -- a positive integer coprime to num
    Output
        list -- the continued fraction [a0, a1, ..., am]
                of the rational number num/denom.
    Examples:
    >>> contfrac_rat(3, 2)
    [1, 2]
    >>> contfrac_rat(103993, 33102)
    [3, 7, 15, 1, 292]
    """
    assert denom > 0, "denom must be positive"
    a = numer
    b = denom
    v = []
    while b != 0:
        v.append(a/b)
        (a, b) = (b, a % b)
    return v

def contfrac_float(x):
    """
    Returns the continued fraction of the floating
    point number x, computed using the continued
    fraction procedure, and the sequence of partial
    convergents.
    Input:
        x -- a floating point number (decimal)
    Output:
        list -- the continued fraction [a0, a1, ...]
                obtained by applying the continued
                fraction procedure to x to the
                precision of this computer.
        list -- the list [(p0, q0), (p1, q1), ...]
                of pairs (pm, qm) such that the mth
                convergent of continued fraction
                is pm/qm.
    Examples:
    >>> v, w = contfrac_float(3.14159); print v
    [3, 7, 15, 1, 25, 1, 7, 4]
    >>> v, w = contfrac_float(2.718); print v
    [2, 1, 2, 1, 1, 4, 1, 12]
    >>> contfrac_float(0.3)
    ([0, 3, 2, 1], [(0, 1), (1, 3), (2, 7), (3, 10)])
    """
    v = []
    w = [(0, 1), (1, 0)] # keep track of convergents
    start = x
    while True:
        a = int(x)                                  # (1)
        v.append(a)
        n = len(v)-1
        pn = v[n]*w[n+1][0] + w[n][0]
        qn = v[n]*w[n+1][1] + w[n][1]
        w.append((pn, qn))
        x -= a
        if abs(start - float(pn)/float(qn)) == 0:    # (2)
            del w[0]
            del w[0]                       # (3)
            return v, w
        x = 1/x

def sum_of_two_squares(p):
    """
    Uses continued fractions to efficiently compute
    a representation of the prime p as a sum of
    two squares.   The prime p must be 1 modulo 4.
    Input:
        p -- a prime congruent 1 modulo 4.
    Output:
        integers a, b such that p is a*a + b*b
    Examples:
    >>> sum_of_two_squares(5)
    (1, 2)
    >>> sum_of_two_squares(389)
    (10, 17)
    >>> sum_of_two_squares(86295641057493119033)
    (789006548L, 9255976973L)
    """
    assert p % 4 == 1, "p must be 1 modulo 4"
    r = sqrtmod(-1, p)                                # (1)
    v = contfrac_rat(-r, p)                           # (2)
    n = int(sqrt(p))
    for a, b in convergents(v):                       # (3)
        c = r*b + p*a                                 # (4)
        if -n <= c and c <= n:
            return (abs(b), abs(c))
    assert False, "Bug in sum_of_two_squares."        # (5)
###############################################################################
################################## UNIT TESTS #################################
###############################################################################

from py.test import raises

def test_divisors():
    assert [1] == divisors(1)
    assert [1, 3] == divisors(3)
    assert [1, 2, 3, 6] == divisors(6)
    assert [1, 3, 9] == divisors(9)
    assert [1, 2, 4, 8, 16] == divisors(16)
    assert [1, 2, 5, 10] == divisors(10)
    assert [1, 3, 5, 15] == divisors(15)
    assert [1, 3, 7, 21] == divisors(21)
    assert [1, 2, 4, 7, 14, 28] == divisors(28)
    assert [-1, 1] == divisors(-1)
    assert [-3, -1, 1, 3] == divisors(-3)
    assert [-6, -3, -2, -1, 1, 2, 3, 6] == divisors(-6)
    assert [1, 2, 4, 5, 10, 11, 20, 22, 44, 55, 110, 220] == divisors(220)
    assert [1, 2, 4, 71, 142, 284] == divisors(284)

def test_gcd():
    assert 1 == gcd(97, 100)
    assert 97 == gcd(97 * 10**15, 19**20 * 97**2)              # (2)

def test_power_of_factor():
    assert 0 == power_of_factor(3, 2)
    assert 1 == power_of_factor(2, 2)
    assert 2 == power_of_factor(4, 2)
    assert 0 == power_of_factor(3, 2)
    assert 5 == power_of_factor(32, 2)
    assert 4 == power_of_factor(81, 3)

def test_prime_factorization():
    assert [(2, 1)] == prime_factorization(2)
    assert [(2, 2)] == prime_factorization(4)
    assert [(2, 1), (3, 2)] == prime_factorization(18)
    assert [(2, 2), (5, 1)] == prime_factorization(20)
    assert [(2, 4), (3, 1)] == prime_factorization(2**4 * 3)
    assert [(2, 2), (5, 3)] == prime_factorization(500)
    assert [(2, 2), (5, 1)] == prime_factorization(20)
    raises(ValueError, prime_factorization, -20)
    assert [] == prime_factorization(1)
    assert [(2, 2), (3, 1), (167, 1)] == prime_factorization(2004)

def test_primes():
    assert [2, 3, 5, 7] == primes(10)
    wanted = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
    assert wanted == primes(45)

def test_trial_division():
    assert 3 == trial_division(15)
    assert 7 == trial_division(91)
    assert 11 == trial_division(11)
    assert 387833 == trial_division(387833, 300)
    assert 389 == trial_division(387833, 400)
