import os


def generate_prime() -> int:
    random_bytes = os.urandom(64)
    random_number = int.from_bytes(random_bytes, byteorder='big')
    return random_number
