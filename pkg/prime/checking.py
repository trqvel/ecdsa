def trial_division_method(number, max_primes):
    if number <= 0:
        raise ValueError("Число для проверки методом пробных делений должно быть натуральным!")
    if max_primes <= 0:
        raise ValueError("Введите натуральное число!")
    if max_primes > 25:
        raise ValueError("Не могу осуществить проверку с более чем 25 простыми числами!")
    
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    
    if max_primes < len(primes):
        primes = primes[:max_primes]
    for p in primes:
        if number % p == 0:
            return f"Число {number} делится на {p}. Не является простым!"
    return f"Число {number} успешно прошло тест пробных делений!"


def test_miller_rabin(number, k):
    if number <= 1:
        return f"Число {number} не является простым."
    if k <= 0:
        raise ValueError("Число оснований теста Миллера-Рабина должно быть натуральным!")
    if k > 20:
        raise ValueError("Не могу осуществить проверку с более чем 20 основаниями в тесте Миллера-Рабина!")

    det_bases = [101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197]
    bases = det_bases[:k]

    for p in bases:
        if number == p:
            return f"Число {number} вероятно простое."
        if number % p == 0 and number != p:
            return f"Число {number} делится на {p}. Не является простым!"
    if number % 2 == 0:
        return f"Число {number} чётное. Не является простым!"

    n = number
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    def check_base(a):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                return True
        return False

    fail_bases = []
    for a in bases:
        if not check_base(a):
            fail_bases.append(a)

    if fail_bases:
        return (f"Число {number} не прошло тест Миллера-Рабина: {fail_bases}!")
    else:
        return (f"Число {number} успешно прошло тест Миллера-Рабина!")