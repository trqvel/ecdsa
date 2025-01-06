from message import hash_message
from curve import multScalar, addPoint, inverseModule

def verify_sign(message, sign, public_key, curve):
    r, s = sign
    n = curve["n"]
    G = curve["G"]

    if not (1 <= r < n and 1 <= s < n):
        return False

    e = int(hash_message(message), 16)

    w = inverseModule(s, n)

    u1 = (e * w) % n
    u2 = (r * w) % n

    R = addPoint(multScalar(u1, G, curve), multScalar(u2, public_key, curve), curve)

    if R == (None, None):
        return False

    return (R[0] % n) == r