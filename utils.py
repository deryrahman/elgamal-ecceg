import numpy as np
import random


def generate_random_prime():
    return random.choice(primes)


def is_prime(n):
    if n <= 1:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def int_to_hex(cipher):
    return ''.join(list(map(lambda x: hex(x), cipher)))


def bytes_to_int(bytes_string):
    return np.frombuffer(bytes_string, dtype=np.int)


def bytes_to_uint8(bytes_string):
    return np.frombuffer(bytes_string, dtype=np.uint8)


primes = [i for i in range(1 << 12, 1 << 13) if is_prime(i)]