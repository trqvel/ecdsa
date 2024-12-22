def encrypt_message_with_curve(message, sender_private_key, receiver_public_key, curve):
    """Шифрование сообщения с использованием эллиптических кривых."""
    # Генерация общего секрета
    shared_secret = (sender_private_key * receiver_public_key[0]) % curve.p

    # Преобразование общего секрета в ключ
    encryption_key = shared_secret % 256  # Упростим ключ до 1 байта

    # Шифрование сообщения
    encrypted_message = "".join(chr(ord(char) ^ encryption_key) for char in message)
    return encrypted_message