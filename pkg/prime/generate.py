import datetime


def genRandom(a, b):
    while True:
        h = hash(str(datetime.datetime.now())) % b
        if a <= h < b:
            return h

def gen512():
    bits = 0
    for _ in range(512):
        bits <<= 1
        bit_val = genRandom(0, 2)
        bits |= bit_val
    bits |= (1 << 511)
    bits |= 1
    return bits

def testFerma(n, rounds=10):
    if n < 2:
        return False
    if n > 2 and (n % 2 == 0):
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19]
    for p in small_primes:
        if n == p:
            return True
        if n % p == 0 and n != p:
            return False

    def ferma_check(a, n):
        return pow(a, n - 1, n) == 1

    for _ in range(rounds):
        a = genRandom(2, n)
        if not ferma_check(a, n):
            return False
    return True

def generate_prime(rounds=10):
    while True:
        candidate = gen512()
        if testFerma(candidate, rounds):
            return candidate