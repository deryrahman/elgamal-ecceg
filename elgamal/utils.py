import numpy as np


def int_to_hex(cipher):
    return ''.join(list(map(lambda x: hex(x), cipher)))


def bytes_to_int(bytes_string):
    return np.frombuffer(bytes_string, dtype=np.int)


def bytes_to_uint8(bytes_string):
    return np.frombuffer(bytes_string, dtype=np.uint8)
