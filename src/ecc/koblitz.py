from math import floor

from gmpy2 import divm

from .curve import Point


def encode(curve, k, msg):
    out = []

    for m in msg:
        p = None

        for ik in range(1, k - 1):
            x = m * k + ik
            y = curve.solve(x)

            if y is not None:
                p = Point(x, y)
                break
        if p is not None:
            out.append(p)
        else:
            raise ValueError(f"Unable to encode {m} into elliptic curve")

    return out


def decode(k, points):
    return bytes([(p.x - 1) // k for p in points])