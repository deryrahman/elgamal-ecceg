import numpy as np
import re


def int_to_hex(cipher):
    return ''.join(list(map(lambda x: hex(x), cipher)))


def hex_to_int(cipher):
    hexa = re.compile(r'0x[0-9a-f]+(?=0x|$)')
    return np.array(
        list(map(lambda x: int(x, 0), hexa.findall(cipher))), dtype=np.int)


def encrypt(plain, public_key, k):
    c1 = public_key['g']**k % public_key['p']
    c1 = np.full(len(plain), c1, dtype=np.int)
    c2 = (public_key['y']**k) * plain % public_key['p']
    return np.array(list(zip(c1, c2)), dtype=np.int).reshape(-1)


def decrypt(cipher, private_key, p):
    cipher = np.reshape(cipher, (-1, 2))
    c2 = cipher[:, 1]
    c1 = np.int(cipher[:, 0][0])
    s = c1**(p - 1 - private_key) % p
    return np.array(c2, dtype=np.int) * s % p
