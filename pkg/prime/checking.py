def trial_division_method(number, bases):
    arr = []
    for b in bases:
        if number % b == 0:
            arr.append(b)

    if arr:
        base = ", ".join(map(str, arr))
        return f"Число {number} составное, так как делится на основани(е/я): {base}."
    else:
        return f"Число {number} простое! Метод пробных делений успешно пройден!"

def test_miller_rabin(number, k):
    if number <= 1:
        return f"Число {number} не является простым."

    det_bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
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

    arr = []
    for a in bases:
        if not check_base(a):
            arr.append(a)

    if arr:
        base = ", ".join(map(str, arr))
        return (f"Число {number} не прошло тест Миллера-Рабина! Провалена проверка при основани(и/ях): {base}!")
    else:
        return (f"Число {number} успешно прошло тест Миллера-Рабина!")