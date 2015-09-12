##################################################
## The Diffie-Hellman Key Exchange
##################################################

def random_prime(num_digits, is_prime = miller_rabin):
    """
    Returns a random prime with num_digits digits.
    Input:
        num_digits -- a positive integer
        is_prime -- (optional argment)
                    a function of one argument n that
                    returns either True if n is (probably)
                    prime and False otherwise.
    Output:
        int -- an integer
    Examples:
    >>> random_prime(10)
    8599796717L              #rand
    >>> random_prime(40)
    1311696770583281776596904119734399028761L  #rand
    """
    n = randrange(10**(num_digits-1), 10**num_digits)
    if n % 2 == 0:
        n += 1
    while not is_prime(n):
        n += 2
    return n

def dh_init(p):
    """
    Generates and returns a random positive
    integer n < p and the power 2^n (mod p).
    Input:
        p -- an integer that is prime
    Output:
        int -- a positive integer < p,  a secret
        int -- 2^n (mod p), send to other user
    Examples:
    >>> p = random_prime(20)
    >>> dh_init(p)
    (15299007531923218813L, 4715333264598442112L)   #rand
    """
    n = randrange(2, p)
    return n, powermod(2, n, p)

def dh_secret(p, n, mpow):
    """
    Computes the shared Diffie-Hellman secret key.
    Input:
        p -- an integer that is prime
        n -- an integer: output by dh_init for this user
        mpow-- an integer: output by dh_init for other user
    Output:
        int -- the shared secret key.
    Examples:
    >>> p = random_prime(20)
    >>> n, npow = dh_init(p)
    >>> m, mpow = dh_init(p)
    >>> dh_secret(p, n, mpow)
    15695503407570180188L      #rand
    >>> dh_secret(p, m, npow)
    15695503407570180188L      #rand
    """
    return powermod(mpow, n, p)

##################################################
## Encoding Strings as Lists of Integers
##################################################

def str_to_numlist(s, bound):
    """
    Returns a sequence of integers between 0 and bound-1
    that encodes the string s.   Randomization is included,
    so the same string is very likely to encode differently
    each time this function is called.
    Input:
        s -- a string
        bound -- an integer >= 256
    Output:
        list -- encoding of s as a list of integers
    Examples:
    >>> str_to_numlist("Run!", 1000)
    [82, 117, 110, 33]               #rand
    >>> str_to_numlist("TOP SECRET", 10**20)
    [4995371940984439512L, 92656709616492L]   #rand
    """
    assert bound >= 256, "bound must be at least 256."
    n = int(log(bound) / log(256))          # (1)
    salt = min(int(n/8) + 1, n-1)           # (2)
    i = 0
    v = []
    while i < len(s):                       # (3)
        c = 0
        power = 1
        for j in range(n):                  # (4)
            if j < salt:
                c += randrange(1, 256)*power   # (5)
            else:
                if i >= len(s):
                    break
                c += ord(s[i])*power          # (6)
                i += 1
            power *= 256
        v.append(c)
    return v

def numlist_to_str(v, bound):
    """
    Returns the string that the sequence v of
    integers encodes.
    Input:
        v -- list of integers between 0 and bound-1
        bound -- an integer >= 256
    Output:
        str -- decoding of v as a string
    Examples:
    >>> print numlist_to_str([82, 117, 110, 33], 1000)
    Run!
    >>> x = str_to_numlist("TOP SECRET MESSAGE", 10**20)
    >>> print numlist_to_str(x, 10**20)
    TOP SECRET MESSAGE
    """
    assert bound >= 256, "bound must be at least 256."
    n = int(log(bound) / log(256))
    s = ""
    salt = min(int(n/8) + 1, n-1)
    for x in v:
        for j in range(n):
            y = x % 256
            if y > 0 and j >= salt:
                s += chr(y)
            x /= 256
    return s

##################################################
## The RSA Cryptosystem
##################################################

def rsa_init(p, q):
    """
    Returns defining parameters (e, d, n) for the RSA
    cryptosystem defined by primes p and q.  The
    primes p and q may be computed using the
    random_prime functions.
    Input:
        p -- a prime integer
        q -- a prime integer
    Output:
        Let m be (p-1)*(q-1).
        e -- an encryption key, which is a randomly
             chosen integer between 2 and m-1
        d -- the inverse of e modulo eulerphi(p*q),
             as an integer between 2 and m-1
        n -- the product p*q.
    Examples:
    >>> p = random_prime(20); q = random_prime(20)
    >>> print p, q
    37999414403893878907L 25910385856444296437L #rand
    >>> e, d, n = rsa_init(p, q)
    >>> e
    5                                           #rand
    >>> d
    787663591619054108576589014764921103213L    #rand
    >>> n
    984579489523817635784646068716489554359L    #rand
    """
    m = (p-1)*(q-1)
    e = 3
    while gcd(e, m) != 1:
        e += 1
    d = inversemod(e, m)
    return e, d, p*q

def rsa_encrypt(plain_text, e, n):
    """
    Encrypt plain_text using the encrypt
    exponent e and modulus n.
    Input:
        plain_text -- arbitrary string
        e -- an integer, the encryption exponent
        n -- an integer, the modulus
    Output:
        str -- the encrypted cipher text
    Examples:
    >>> e = 1413636032234706267861856804566528506075
    >>> n = 2109029637390047474920932660992586706589
    >>> rsa_encrypt("Run Nikita!", e, n)
    [78151883112572478169375308975376279129L]    #rand
    >>> rsa_encrypt("Run Nikita!", e, n)
    [1136438061748322881798487546474756875373L]  #rand
    """
    plain = str_to_numlist(plain_text, n)
    return [powermod(x, e, n) for x in plain]

def rsa_decrypt(cipher, d, n):
    """
    Decrypt the cipher_text using the decryption
    exponent d and modulus n.
    Input:
        cipher_text -- list of integers output
                       by rsa_encrypt
    Output:
        str -- the unencrypted plain text
    Examples:
    >>> d = 938164637865370078346033914094246201579
    >>> n = 2109029637390047474920932660992586706589
    >>> msg1 = [1071099761433836971832061585353925961069]
    >>> msg2 = [1336506586627416245118258421225335020977]
    >>> rsa_decrypt(msg1, d, n)
    'Run Nikita!'
    >>> rsa_decrypt(msg2, d, n)
    'Run Nikita!'
    """
    plain = [powermod(x, d, n) for x in cipher]
    return numlist_to_str(plain, n)

##################################################
## Arithmetic
##################################################

def ellcurve_add(E, P1, P2):
    """
    Returns the sum of P1 and P2 on the elliptic
    curve E.
    Input:
         E -- an elliptic curve over Z/pZ, given by a
              triple of integers (a, b, p), with p odd.
         P1 --a pair of integers (x, y) or the
              string "Identity".
         P2 -- same type as P1
    Output:
         R -- same type as P1
    Examples:
    >>> E = (1, 0, 7)   # y**2 = x**3 + x over Z/7Z
    >>> P1 = (1, 3); P2 = (3, 3)
    >>> ellcurve_add(E, P1, P2)
    (3, 4)
    >>> ellcurve_add(E, P1, (1, 4))
    'Identity'
    >>> ellcurve_add(E, "Identity", P2)
    (3, 3)
    """
    a, b, p = E
    assert p > 2, "p must be odd."
    if P1 == "Identity":
        return P2
    if P2 == "Identity":
        return P1
    x1, y1 = P1
    x2, y2 = P2
    x1 %= p
    y1 %= p
    x2 %= p
    y2 %= p
    if x1 == x2 and y1 == p-y2:
        return "Identity"
    if P1 == P2:
        if y1 == 0:
            return "Identity"
        lam = (3*x1**2+a) * inversemod(2*y1, p)
    else:
        lam = (y1 - y2) * inversemod(x1 - x2, p)
    x3 = lam**2 - x1 - x2
    y3 = -lam*x3 - y1 + lam*x1
    return (x3 % p, y3 % p)

def ellcurve_mul(E, m, P):
    """
    Returns the multiple m*P of the point P on
    the elliptic curve E.
    Input:
        E -- an elliptic curve over Z/pZ, given by a
             triple (a, b, p).
        m -- an integer
        P -- a pair of integers (x, y) or the
             string "Identity"
    Output:
        A pair of integers or the string "Identity".
    Examples:
    >>> E = (1, 0, 7)
    >>> P = (1, 3)
    >>> ellcurve_mul(E, 5, P)
    (1, 3)
    >>> ellcurve_mul(E, 9999, P)
    (1, 4)
    """
    assert m >= 0, "m must be nonnegative."
    power = P
    mP = "Identity"
    while m != 0:
        if m % 2 != 0:
            mP = ellcurve_add(E, mP, power)
        power = ellcurve_add(E, power, power)
        m /= 2
    return mP

##################################################
## Integer Factorization
##################################################

def randcurve(p):
    """
    Construct a somewhat random elliptic curve
    over Z/pZ and a random point on that curve.
    Input:
        p -- a positive integer
    Output:
        tuple -- a triple E = (a, b, p)
        P -- a tuple (x, y) on E
    Examples:
    >>> p = random_prime(20); p
    17758176404715800329L    #rand
    >>> E, P = randcurve(p)
    >>> print E
    (15299007531923218813L, 1, 17758176404715800329L)  #rand
    >>> print P
    (0, 1)
    """
    assert p > 2, "p must be > 2."
    a = randrange(p)
    while gcd(4*a**3 + 27, p) != 1:
        a = randrange(p)
    return (a, 1, p), (0, 1)

def elliptic_curve_method(N, m, tries=5):
    """
    Use the elliptic curve method to try to find a
    nontrivial divisor of N.
    Input:
        N -- a positive integer
        m -- a positive integer, the least common
             multiple of the integers up to some
             bound, computed using lcm_to.
        tries -- a positive integer, the number of
             different elliptic curves to try
    Output:
        int -- a divisor of n
    Examples:
    >>> elliptic_curve_method(5959, lcm_to(20))
    59L       #rand
    >>> elliptic_curve_method(10007*20011, lcm_to(100))
    10007L   #rand
    >>> p = random_prime(9); q = random_prime(9)
    >>> n = p*q; n
    117775675640754751L   #rand
    >>> elliptic_curve_method(n, lcm_to(100))
    117775675640754751L   #rand
    >>> elliptic_curve_method(n, lcm_to(500))
    117775675640754751L   #rand
    """
    for _ in range(tries):                     # (1)
        E, P = randcurve(N)                    # (2)
        try:                                   # (3)
            Q = ellcurve_mul(E, m, P)          # (4)
        except ZeroDivisionError, x:           # (5)
            g = gcd(x[0], N)                    # (6)
            if g != 1 or g != N:
                return g      # (7)
    return N

##################################################
## ElGamal Elliptic Curve Cryptosystem
##################################################

def elgamal_init(p):
    """
    Constructs an ElGamal cryptosystem over Z/pZ, by
    choosing a random elliptic curve E over Z/pZ, a
    point B in E(Z/pZ), and a random integer n.  This
    function returns the public key as a 4-tuple
    (E, B, n*B) and the private key n.
    Input:
        p -- a prime number
    Output:
        tuple -- the public key as a 3-tuple
                 (E, B, n*B), where E = (a, b, p) is an
                 elliptic curve over Z/pZ, B = (x, y) is
                 a point on E, and n*B = (x', y') is
                 the sum of B with itself n times.
        int -- the private key, which is the pair (E, n)
    Examples:
    >>> p = random_prime(20); p
    17758176404715800329L    #rand
    >>> public, private = elgamal_init(p)
    >>> print "E =", public[0]
    E = (15299007531923218813L, 1, 17758176404715800329L)   #rand
    >>> print "B =", public[1]
    B = (0, 1)
    >>> print "nB =", public[2]
    nB = (5619048157825840473L, 151469105238517573L)   #rand
    >>> print "n =", private[1]
    n = 12608319787599446459    #rand
    """
    E, B = randcurve(p)
    n = randrange(2, p)
    nB = ellcurve_mul(E, n, B)
    return (E, B, nB), (E, n)

def elgamal_encrypt(plain_text, public_key):
    """
    Encrypt a message using the ElGamal cryptosystem
    with given public_key = (E, B, n*B).
    Input:
       plain_text -- a string
       public_key -- a triple (E, B, n*B), as output
                     by elgamal_init.
    Output:
       list -- a list of pairs of points on E that
               represent the encrypted message
    Examples:
    >>> public, private = elgamal_init(random_prime(20))
    >>> elgamal_encrypt("RUN", public)
    [((6004308617723068486L, 15578511190582849677L), \ #rand
     (7064405129585539806L, 8318592816457841619L))]    #rand
    """
    E, B, nB = public_key
    a, b, p = E
    assert p > 10000, "p must be at least 10000."
    v = [1000*x for x in \
           str_to_numlist(plain_text, p/1000)]       # (1)
    cipher = []
    for x in v:
        while not legendre(x**3+a*x+b, p) == 1:        # (2)
            x = (x+1) % p
        y = sqrtmod(x**3+a*x+b, p)                   # (3)
        P = (x, y)
        r = randrange(1, p)
        encrypted = (ellcurve_mul(E, r, B), \
                ellcurve_add(E, P, ellcurve_mul(E, r, nB)))
        cipher.append(encrypted)
    return cipher

def elgamal_decrypt(cipher_text, private_key):
    """
    Encrypt a message using the ElGamal cryptosystem
    with given public_key = (E, B, n*B).
    Input:
        cipher_text -- list of pairs of points on E output
                       by elgamal_encrypt.
    Output:
        str -- the unencrypted plain text
    Examples:
    >>> public, private = elgamal_init(random_prime(20))
    >>> v = elgamal_encrypt("TOP SECRET MESSAGE!", public)
    >>> print elgamal_decrypt(v, private)
    TOP SECRET MESSAGE!
    """
    E, n = private_key
    p = E[2]
    plain = []
    for rB, P_plus_rnB in cipher_text:
        nrB = ellcurve_mul(E, n, rB)
        minus_nrB = (nrB[0], -nrB[1])
        P = ellcurve_add(E, minus_nrB, P_plus_rnB)
        plain.append(P[0]/1000)
    return numlist_to_str(plain, p/1000)


##################################################
## Associativity of the Group Law
##################################################

# The variable order is x1, x2, x3, y1, y2, y3, a, b
class Poly:                                     # (1)
    def __init__(self, d):                      # (2)
        self.v = dict(d)
    def __cmp__(self, other):                   # (3)
        self.normalize()
        other.normalize()     # (4)
        if self.v == other.v:
            return 0
        return -1

    def __add__(self, other):                   # (5)
        w = Poly(self.v)
        for m in other.monomials():
            w[m] += other[m]
        return w
    def __sub__(self, other):
        w = Poly(self.v)
        for m in other.monomials():
            w[m] -= other[m]
        return w
    def __mul__(self, other):
        if len(self.v) == 0 or len(other.v) == 0:
            return Poly([])
        m1 = self.monomials()
        m2 = other.monomials()
        r = Poly([])
        for m1 in self.monomials():
            for m2 in other.monomials():
                z = [m1[i] + m2[i] for i in range(8)]
                r[z] += self[m1]*other[m2]
        return r
    def __neg__(self):
        v = {}
        for m in self.v.keys():
            v[m] = -self.v[m]
        return Poly(v)
    def __div__(self, other):
        return Frac(self, other)

    def __getitem__(self, m):                   # (6)
        m = tuple(m)
        if not self.v.has_key(m):
            self.v[m] = 0
        return self.v[m]
    def __setitem__(self, m, c):
        self.v[tuple(m)] = c
    def __delitem__(self, m):
        del self.v[tuple(m)]

    def monomials(self):                        # (7)
        return self.v.keys()
    def normalize(self):                        # (8)
        while True:
            finished = True
            for m in self.monomials():
                if self[m] == 0:
                    del self[m]
                    continue
                for i in range(3):
                    if m[3+i] >= 2:
                        finished = False
                        nx0 = list(m)
                        nx0[3+i] -= 2
                        nx0[7] += 1
                        nx1 = list(m)
                        nx1[3+i] -= 2
                        nx1[i] += 1
                        nx1[6] += 1
                        nx3 = list(m)
                        nx3[3+i] -= 2
                        nx3[i] += 3
                        c = self[m]
                        del self[m]
                        self[nx0] += c
                        self[nx1] += c
                        self[nx3] += c
                # end for
            # end for
            if finished:
                return
        # end while

one = Poly({(0, 0, 0, 0, 0, 0, 0, 0):1})               # (9)

class Frac:                                     # (10)
    def __init__(self, num, denom=one):
        self.num = num
        self.denom = denom
    def __cmp__(self, other):                   # (11)
        if self.num * other.denom == self.denom * other.num:
            return 0
        return -1

    def __add__(self, other):                   # (12)
        return Frac(self.num*other.denom + \
                    self.denom*other.num,
                    self.denom*other.denom)
    def __sub__(self, other):
        return Frac(self.num*other.denom - \
                    self.denom*other.num,
                    self.denom*other.denom)
    def __mul__(self, other):
        return Frac(self.num*other.num, \
                    self.denom*other.denom)
    def __div__(self, other):
        return Frac(self.num*other.denom, \
                    self.denom*other.num)
    def __neg__(self):
        return Frac(-self.num, self.denom)

def var(i):                                     # (14)
    v = [0, 0, 0, 0, 0, 0, 0, 0]
    v[i] = 1
    return Frac(Poly({tuple(v):1}))

def prove_associative():                        # (15)
    x1 = var(0)
    x2 = var(1)
    x3 = var(2)
    y1 = var(3)
    y2 = var(4)
    y3 = var(5)
    #a  = var(6)
    #b  = var(7)

    lambda12 = (y1 - y2)/(x1 - x2)
    x4       = lambda12*lambda12 - x1 - x2
    nu12     = y1 - lambda12*x1
    y4       = -lambda12*x4 - nu12
    lambda23 = (y2 - y3)/(x2 - x3)
    x5       = lambda23*lambda23 - x2 - x3
    nu23     = y2 - lambda23*x2
    y5       = -lambda23*x5 - nu23
    s1 = (x1 - x5)*(x1 - x5)*((y3 - y4)*(y3 - y4) \
                   - (x3 + x4)*(x3 - x4)*(x3 - x4))
    s2 = (x3 - x4)*(x3 - x4)*((y1 - y5)*(y1 - y5) \
                   - (x1 + x5)*(x1 - x5)*(x1 - x5))
    print "Associative?"
    print s1 == s2                              # (17)
