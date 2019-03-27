import numpy as np

from gmpy2 import mpz

from .curve import Point


def to_np(msg_cipher):
    return np.array([[(u.x, u.y) for u in t] for t in msg_cipher],
                    dtype=np.int).reshape(-1)


def from_np(np_cipher):
    return [
        tuple(Point(*(int(d) for d in u)) for u in e)
        for e in np_cipher.reshape(-1, 2, 2)
    ]
