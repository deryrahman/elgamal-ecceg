from math import floor

from gmpy2 import divm

from .curve import Point


def encode1(curve, k, m):
    for ik in range(1, k - 1):
        x = m * k + ik
        y = curve.solve(x)

        if x >= curve.p:
            raise ValueError("curve.p is too small or k is too big")
        if y is not None:
            return Point(x, y)
    return None


def decode1(k, p):
    return (p.x - 1) // k
