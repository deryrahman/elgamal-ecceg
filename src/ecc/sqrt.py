# Euler's criterion
# https://geeksforgeeks.org/eulers-criterion-check-if-square-root-under-modulo-p-exists


def is_square_rootable(n, p):
    return pow(n, (p - 1) // 2, p) == 1


# Shanks Tonelli algorithm
# https://geeksforgeeks.org/find-square-root-modulo-p-set-2-shanks-tonelli-algorithm

from gmpy2 import gcd


def order(p, b):
    if gcd(p, b) != 1:
        return None

    k = 3
    while True:
        if pow(b, k, p) == 1:
            return k
        k += 1


def convert_x2e(x):
    e = 0
    while (x % 2) == 0:
        x //= 2
        e += 1
    return (x, e)


def square_root(n, p):
    if (gcd(n, p) != 1):
        return None
    if pow(n, (p - 1) // 2, p) == (p - 1):
        return None

    s, e = convert_x2e(p - 1)

    q = 2
    while True:
        if pow(q, (p - 1) // 2, p) == (p - 1):
            break
        q += 1

    x = pow(n, (s + 1) // 2, p)
    b = pow(n, s, p)
    g = pow(q, s, p)

    r = e

    while True:
        m = 0
        while m < r:
            val = order(p, b)
            if val is None:
                return None
            if val == pow(2, m):
                break
            m += 1
        if m == 0:
            return x

        x = (x * pow(g, pow(2, r - m - 1), p)) % p
        g = pow(g, pow(2, r - m), p)
        b = (b * g) % p

        if b == 1:
            return x
        r = m
