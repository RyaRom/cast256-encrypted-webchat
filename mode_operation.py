from os import urandom

import cast256
import utils
from utils import padding


def random_key():
    return int.from_bytes(urandom(16), byteorder="big")


def decrypt_chunk(blocks: list[int], key):
    """
    Расшифровать 16 байтов (128 битов)
    :param blocks: массив из 4 блоков по 4 байта (32 бита)
    :param key: ключ из 256 битов
    """
    return [cast256.decrypt_block(block, key) for block in blocks]


def encrypt_chunk(chunk: bytes, key):
    """
    Зашифровать 16 байтов (128 битов)
    :param chunk: 16 байтов
    :param key: ключ из 256 битов
    """
    blocks = utils.split_on_parts(chunk, utils.parts_per_chunk)
    return [cast256.encrypt_block(block, key) for block in blocks]


def encrypt(message: str, key: bytes):
    byte_msg = message.encode()
    padded = padding(byte_msg)
    chunks = utils.split_with_len(padded, utils.chunk_bytes)
    return [encrypt_chunk(c, key) for c in chunks]


def decrypt(encrypted: list[list[int]], key: bytes) -> str:
    decrypted_bytes = [decrypt_chunk(c, key) for c in encrypted]
    to_bytes = [
        b''.join([byte.to_bytes(utils.parts_per_chunk, byteorder='big') for byte in c])
        for c in decrypted_bytes
    ]
    result = b''.join(to_bytes)
    return utils.depadding(result).decode()
