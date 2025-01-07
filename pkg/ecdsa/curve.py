import datetime


def curveNIST256p():
    p = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
    a = (p - 3) % p
    b = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
    G_x = 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296
    G_y = 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5
    n = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
    h = 1

    return {
        "p": p,
        "a": a,
        "b": b,
        "G": (G_x, G_y),
        "n": n,
        "h": h
    }

def inverseModule(k, p):
    if k == 0:
        raise ValueError("Обратного элемента не существует!")
    return pow(k, -1, p)

def checkPointOnCurve(P, curve):
    if P == (None, None):
        return True
    x, y = P
    p = curve["p"]
    a = curve["a"]
    b = curve["b"]
    lhs = (y * y) % p
    rhs = (pow(x, 3, p) + (a * x) % p + b) % p
    return lhs == rhs

def addPoint(P, Q, curve):
    if not checkPointOnCurve(P, curve):
        raise ValueError("Точка P не лежит на кривой!")
    if not checkPointOnCurve(Q, curve):
        raise ValueError("Точка Q не лежит на кривой!")
    p = curve["p"]
    if P == (None, None):
        return Q
    if Q == (None, None):
        return P
    if P[0] == Q[0] and (P[1] != Q[1]):
        return (None, None)
    if P != Q:
        lam = ((Q[1] - P[1]) * inverseModule((Q[0] - P[0]) % p, p)) % p
    else:
        lam = ((3 * (P[0] ** 2) + curve["a"]) *
               inverseModule((2 * P[1]) % p, p)) % p
    x_r = (lam * lam - P[0] - Q[0]) % p
    y_r = (lam * (P[0] - x_r) - P[1]) % p
    return (x_r, y_r)

def multScalar(k, P, curve):
    if k == 0 or P == (None, None):
        return (None, None)
    N = P
    Q = (None, None)
    while k:
        if k & 1:
            Q = addPoint(Q, N, curve)
        N = addPoint(N, N, curve)
        k >>= 1
    return Q

def genRandom(a, b):
    while True:
        h = hash(str(datetime.datetime.now())) % b
        if a <= h < b:
            return h

def generate_keys(curve):
    d = genRandom(1, curve["n"])
    Q = multScalar(d, curve["G"], curve)
    if not checkPointOnCurve(Q, curve):
        raise ValueError("Генерация некорректного публичного ключа!")
    return d, Q