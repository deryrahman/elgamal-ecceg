from .koblitz import encode1, decode1

from random import randint


def gen_pub(curve, b, pri):
    return curve.pow(pri, b)


def encrypt(curve, b, pub, koblitz_k, msg):
    out = []
    for m in msg:
        pm = encode1(curve, koblitz_k, m)
        k = randint(1, curve.p)

        out.append((
            curve.pow(k, b),
            curve.add(pm, curve.pow(k, pub))))
    return out


def decrypt(curve, b, pri, koblitz_k, cipher_msg):
    out = []
    for msg_tuple in cipher_msg:
        m_a, m_b = msg_tuple
        m = curve.subtract(m_b, curve.pow(pri, m_a))
        out.append(decode1(koblitz_k, m))
    return bytes(out)
