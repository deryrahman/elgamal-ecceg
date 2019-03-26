import numpy as np


def encrypt(plain, public_key, k):
    c1 = public_key['g']**k % public_key['p']
    c1 = np.full(len(plain), c1, dtype=np.int)
    c2 = (public_key['y']**k) * plain % public_key['p']
    return np.array(list(zip(c1, c2)), dtype=np.int).reshape(-1)


def decrypt(cipher, private_key, p):
    x = private_key['x']
    cipher = np.reshape(cipher, (-1, 2))
    c2 = cipher[:, 1]
    c1 = np.int(cipher[:, 0][0])
    s = c1**(p - 1 - x) % p
    return np.array(c2 * s % p, dtype=np.uint8)
