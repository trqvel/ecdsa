from message import hash_message
from curve import multScalar, inverseModule, genRandom

def sign_message(message, private_key, curve):
    e = int(hash_message(message), 16)
    n = curve["n"]
    G = curve["G"]

    while True:
        k = genRandom(1, n - 1)

        R = multScalar(k, G, curve)
        r = R[0] % n

        if r == 0:
            continue

        k_inv = inverseModule(k, n)
        s = (k_inv * (e + r * private_key)) % n

        if s == 0:
            continue

        return (r, s)