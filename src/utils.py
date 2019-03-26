import numpy as np
import re


def int_to_hex(cipher):
    return ''.join(list(map(lambda x: hex(x), cipher)))


def hex_to_int(cipher):
    hexa = re.compile(r'0x[0-9a-f]+(?=0x|$)')
    return np.array(
        list(map(lambda x: int(x, 0), hexa.findall(cipher))), dtype=np.int)


def to_numpy_array(plain_text):
    return np.array(
        list(map(lambda x: ord(x), list(plain_text))), dtype=np.uint8)


def to_string(cipher_text):
    return ''.join(list(map(lambda x: chr(x), list(cipher_text))))