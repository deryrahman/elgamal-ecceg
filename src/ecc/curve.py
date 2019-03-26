from .sqrt import is_square_rootable, square_root


class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def solve(self, x):
        y2 = x**3 + self.a * x + self.b

        if is_square_rootable(y2, self.p):
            return square_root(y2, self.p)
        else:
            return None


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
