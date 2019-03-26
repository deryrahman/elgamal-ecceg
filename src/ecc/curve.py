from gmpy2 import divm

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

    def __repr__(self):
        return f"(x**3 + {self.a}*x + {self.b}) mod {self.p}"

    def _gradient(self, p, q):
        dy = p.y - q.y
        dx = p.x - q.x
        return divm(dy, dx, self.p)

    def _gradient1(self, p):
        n = 3 * p.x**2 + self.a
        d = 2 * p.y
        return divm(n, d, self.p)

    def _add_g(self, g, p, q):
        r = Point()
        r.x = (g**2 - p.x - q.x) % self.p
        r.y = (g * (p.x - r.x) - p.y) % self.p
        return r

    def add(self, p, q):
        return self._add_g(self._gradient(p, q), p, q)

    def substract(self, p, q):
        q_neg = Point(q.x, -q.y % self.p)
        return self.add(p, q_neg)

    def mul2(self, p):
        return self._add_g(self._gradient1(p), p, p)


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"
