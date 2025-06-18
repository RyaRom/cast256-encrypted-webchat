from os import urandom

from key_generator import *
from utils import padding


def random_key(bytes_count: int = 32) -> bytes:
    """
    Случайный ключ от 128 до 256 бит длинной
    :param bytes_count: длина ключа
    """
    return urandom(bytes_count)


def encrypt_block(message, key):
    """
    Эта функция выполняет шифрование блока размером 128 бит,
    выполняя последовательные раунды алгоритма CAST-256.

    :param message: блок данных для шифрования (128 бит)
    :param key: ключ шифрования (256 бит)
    :return: зашифрованный блок (128 бит)
    """
    kr, km = key_generator(key)

    for i in range(0, 6):
        message = forward_quad_round(message, kr[i], km[i])
    for i in range(6, 12):
        message = reverse_quad_round(message, kr[i], km[i])

    return message


def decrypt_block(cipher, key):
    """
    Эта функция выполняет расшифровку блока размером 128 бит,
    выполняя последовательные раунды алгоритма CAST-256.

    :param cipher: блок данных для расшифровки (128 бит)
    :param key: ключ шифрования (256 бит)
    :return: расшифрованный блок (128 бит)
    """
    kr, km = key_generator(key)

    kr.reverse()
    km.reverse()

    for i in range(0, 6):
        cipher = forward_quad_round(cipher, kr[i], km[i])
    for i in range(6, 12):
        cipher = reverse_quad_round(cipher, kr[i], km[i])

    return cipher


def encrypt(message: str | bytes, key: bytes) -> list[int]:
    """
    Зашифровать сообщение
    """
    if type(message) is str:
        message = message.encode()
    padded = padding(message)
    chunks = utils.split_with_len(padded, utils.chunk_bytes)
    return [encrypt_block(c, key) for c in chunks]


def decrypt(encrypted: list[int], key: bytes) -> bytes:
    """
    Расшифровать сообщение
    """
    decrypted_bytes = [decrypt_block(c, key) for c in encrypted]
    to_bytes = b''.join([
        byte.to_bytes(utils.chunk_bytes, byteorder='big') for byte in decrypted_bytes
    ])
    return utils.depadding(to_bytes)
