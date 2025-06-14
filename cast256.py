from key_generator import *


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
