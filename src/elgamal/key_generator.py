def is_prime(n):
    if n <= 1:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def generate_public_key(g, x, p):
    if not is_prime(p):
        raise ValueError("p should be prime number")
    if g >= p:
        raise ValueError("g should less than p")
    if not (x > 0 and x < p - 1):
        raise ValueError("x should be 0<x<p-1")
    y = (g**x) % p
    return {'y': y, 'g': g, 'p': p}
