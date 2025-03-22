import datetime
import time


def time_entropy_32bits():
    t1 = time.perf_counter_ns()
    x = 1
    for _ in range(1000):
        x ^= (x << 13) & 0xffffffff
        x ^= (x >> 17)
        x ^= (x << 5) & 0xffffffff
    t2 = time.perf_counter_ns()
    datetime_str = str(datetime.datetime.now())
    combined = hash((t1, t2, x, datetime_str))
    return combined & ((1 << 32) - 1)

def genRandom(a, b):
    while True:
        r = time_entropy_32bits() % b
        if a <= r < b:
            return r

def gen512():
    bits = 0
    for _ in range(16):
        bits = (bits << 32) | time_entropy_32bits()
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