from .koblitz import encode1, decode1

from random import randint


def pub_gen(curve, b, pri_a, pri_b):
    return curve.pow(pri_a, b), curve.pow(pri_b, b)


def encrypt(curve, b, pub_b, koblitz_k, msg):
    out = []
    for m in msg:
        pm = encode1(curve, koblitz_k, m)
        print(pm)
        k = randint(1, curve.p)

        out.append((
            curve.pow(k, b),
            curve.add(pm, curve.pow(k, pub_b))))
    return out


def decrypt(curve, b, pri_b, koblitz_k, cipher_msg):
    out = []
    for msg_tuple in cipher_msg:
        m_a, m_b = msg_tuple
        m = curve.subtract(m_b, curve.pow(pri_b, m_a))
        print(m)
        out.append(decode1(koblitz_k, m))
    return bytes(out)
