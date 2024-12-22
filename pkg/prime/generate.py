import os
import time
import threading
from typing import List


# Функция для проверки, является ли число простым
def is_prime(n: int, primes: List[int]) -> bool:
    if n < 2:
        return False
    if n % 2 == 0 and n != 2:
        return False
    for p in primes:
        if n % p == 0:
            return False
        if p * p > n:
            break
    return True


# Функция для генерации простого числа в диапазоне
def generate_prime(start: int, end: int, workers: int) -> int:
    base_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29]
    result = None
    results_lock = threading.Lock()

    # Функция для генерации случайного числа на основе системной энтропии
    def generate_seed(worker_id: int) -> int:
        entropy = int(time.time() * 1000000) ^ os.getpid() ^ worker_id
        return int(entropy % (end - start + 1)) + start

    # Функция, выполняющая поиск простого числа в диапазоне
    def worker(worker_id: int):
        nonlocal result
        start_point = generate_seed(worker_id)

        for num in range(start_point, end + 1):
            if is_prime(num, base_primes):
                with results_lock:
                    if result is None:
                        result = num
                        return

            if num == end:
                num = start - 1

    threads = []
    for i in range(workers):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return result
