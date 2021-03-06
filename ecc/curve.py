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
        return "(x**3 + {}*x + {}) mod {}".format(self.a, self.b, self.p)

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

    def subtract(self, p, q):
        q_neg = Point(q.x, -q.y % self.p)
        return self.add(p, q_neg)

    def mul2(self, p):
        return self._add_g(self._gradient1(p), p, p)

    def pow(self, k, p):
        if k > 0:
            out = p
            for c in bin(k)[3:]:
                out = self.mul2(out)
                if c == "1":
                    out = self.add(out, p)
            return out
        else:
            return Point()


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)
