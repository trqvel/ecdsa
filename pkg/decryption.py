def decrypt_message_with_curve(encrypted_message, receiver_private_key, sender_public_key, curve):
    """Расшифровка сообщения с использованием эллиптических кривых."""
    # Восстановление общего секрета
    shared_secret = (receiver_private_key * sender_public_key[0]) % curve.p

    # Преобразование общего секрета в ключ
    decryption_key = shared_secret % 256  # Упростим ключ до 1 байта

    # Расшифровка сообщения
    decrypted_message = "".join(chr(ord(char) ^ decryption_key) for char in encrypted_message)
    return decrypted_message