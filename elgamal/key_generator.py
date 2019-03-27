import utils


def generate_public_key(g, x, p):
    if not utils.is_prime(p):
        raise ValueError("p should be prime number")
    if g >= p:
        raise ValueError("g should less than p")
    if not (x > 0 and x < p - 1):
        raise ValueError("x should be 0<x<p-1")
    y = (g**x) % p
    return {'y': y, 'g': g, 'p': p}
