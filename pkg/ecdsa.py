from pkg.generate import generate_prime

# Параметры эллиптической кривой
class EllipticCurve:
    def __init__(self, p, a, b, g, n):
        self.p = p  # Простое число (модуль)
        self.a = a  # Коэффициент a кривой
        self.b = b  # Коэффициент b кривой
        self.g = g  # Генератор (точка на кривой)
        self.n = n  # Порядок группы

# Генерация эллиптической кривой
def create_curve():
    # Генерируем параметры кривой
    p = generate_prime(10**5, 10**6, 4)  # Простое число для модуля
    a = generate_prime(10, 100, 2)  # Коэффициент a
    b = generate_prime(10, 100, 2)  # Коэффициент b
    g = (2, 3)  # Точка генератор (можно сделать фиксированной, если нужно)
    n = generate_prime(10**4, 10**5, 3)  # Порядок группы
    return EllipticCurve(p, a, b, g, n)

# Генерация ключей
def generate_keys(curve):
    private_key = generate_prime(1, curve.n - 1, 2)  # Случайный приватный ключ
    public_key = (
        (private_key * curve.g[0]) % curve.p,
        (private_key * curve.g[1]) % curve.p,
    )  # Публичный ключ - точка на кривой
    return private_key, public_key

# Простая хеш-функция (имитация sha256)
def simple_hash(message):
    hash_value = 0
    for char in message:
        hash_value = (hash_value + ord(char) ** 2) % (10**5)  # Простая хеш-функция
    return hash_value

# Подпись сообщения
def sign_message(private_key, message, curve):
    hashed_msg = simple_hash(message)  # Хешируем сообщение
    k = generate_prime(1, curve.n - 1, 2)  # Случайное число k
    r = (k * curve.g[0]) % curve.p  # Вычисляем r
    s = ((hashed_msg + r * private_key) * pow(k, -1, curve.n)) % curve.n  # Вычисляем s
    return r, s

# Проверка подписи
def verify_signature(public_key, message, signature, curve):
    r, s = signature
    hashed_msg = simple_hash(message)  # Хешируем сообщение
    w = pow(s, -1, curve.n)  # Обратное значение s
    u1 = (hashed_msg * w) % curve.n
    u2 = (r * w) % curve.n
    x = (u1 * curve.g[0] + u2 * public_key[0]) % curve.p  # Проверяем x-координату
    return r == x
