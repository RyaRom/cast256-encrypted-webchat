chunk_bytes = 16
parts_per_chunk = 4


def split_with_len(data, size):
    """
    Разбить на части длинной size байт
    """
    parts = len(data) // size
    return [data[i * size: i * size + size] for i in range(parts)]


def padding(data: bytes):
    """
    Добавляем недостающие байты в конец по алгоритму pkcs#7
    """
    size = len(data)
    padding_len = chunk_bytes - (size % chunk_bytes)
    padding_str = bytes([padding_len]) * padding_len
    return data + padding_str


def depadding(padded: bytes):
    padding_len = int(padded[-1])
    return padded[:-padding_len]


def sum_mod_232(a, b):
    return (a + b) % (2 ** 32)


def diff_mod_232(a, b):
    return (a - b) % (2 ** 32)


def build_128_bit_bloc_from_32_bit_blocs(a, b, c, d):
    """
    Эта функция собирает четыре 32-битных блока в один 128-битный.
    Блоки передаются в порядке от старшего к младшему,
    то есть в финальной последовательности слева направо: a, b, c, d.
    :return: один 128-битный блок в порядке 'abcd'
    """
    return (a << 96) | (b << 64) | (c << 32) | d


def extract_32bit_bloc_from_128(abcd):
    """
    Эта функция разбивает 128-битный блок на четыре 32-битных. Результирующие блоки расположены от старшего к младшему,
    то есть в том же порядке, как они были собраны: слева направо.
    :param abcd: 128-битный блок
    :return: четыре 32-битных блока a, b, c, d, такие, что 'abcd' — исходный блок
    """
    mask_32_bits = 0xFFFFFFFF
    if type(abcd) is bytes:
        abcd = int.from_bytes(abcd, byteorder='big')
    a = (abcd >> 96) & mask_32_bits
    b = (abcd >> 64) & mask_32_bits
    c = (abcd >> 32) & mask_32_bits
    d = abcd & mask_32_bits
    return a, b, c, d


def extract_32bit_bloc_from_256(abcdefgh):
    """
    Эта функция разбивает 256-битный блок на восемь 32-битных. Результирующие блоки расположены от старшего к младшему,
    в том же порядке, как они были собраны: слева направо.
    :param abcdefgh: 256-битный блок
    :return: восемь 32-битных блоков a, b, c, d, e, f, g, h, такие, что 'abcdefgh' — исходный блок
    """
    mask_32_bits = 0xFFFFFFFF
    if type(abcdefgh) is bytes:
        abcdefgh = int.from_bytes(abcdefgh, byteorder='big')
    a = (abcdefgh >> 224) & mask_32_bits
    b = (abcdefgh >> 192) & mask_32_bits
    c = (abcdefgh >> 160) & mask_32_bits
    d = (abcdefgh >> 128) & mask_32_bits
    e = (abcdefgh >> 96) & mask_32_bits
    f = (abcdefgh >> 64) & mask_32_bits
    g = (abcdefgh >> 32) & mask_32_bits
    h = abcdefgh & mask_32_bits
    return a, b, c, d, e, f, g, h


def build_256_bit_bloc_from_32_bit_blocs(a, b, c, d, e, f, g, h):
    """
    Эта функция собирает восемь 32-битных блоков в один 256-битный.
    Блоки передаются от старшего к младшему,
    то есть в финальной последовательности слева направо.
    :return: один 256-битный блок в порядке 'abcdefgh'
    """
    return (a << 224) | (b << 192) | (c << 160) | (d << 128) | (e << 96) | (f << 64) | (g << 32) | h


def extract_8bit_blocs_from_32(abcd):
    """
    Эта функция разбивает 32-битное число на четыре 8-битных блока.
    Результирующие блоки расположены от старшего к младшему,
    в том же порядке, как они были собраны: слева направо.
    :param abcd: 32-битный блок
    :return: четыре 8-битных блока a, b, c, d, такие, что 'abcd' — исходный блок
    """
    mask_8_bits = 0xFF
    a = (abcd >> 24) & mask_8_bits
    b = (abcd >> 16) & mask_8_bits
    c = (abcd >> 8) & mask_8_bits
    d = abcd & mask_8_bits
    return a, b, c, d


def shift_left(data, input_size, n_bit):
    """
    Эта функция выполняет циклический сдвиг (barrel shift <<<) числа data влево
    на n_bit бит, при этом учитывая общую длину input_size.
    :param data: число, которое нужно сдвинуть
    :param input_size: длина данных в битах
    :param n_bit: количество бит для сдвига влево
    :return: результат циклического сдвига влево
    """
    n_bit = n_bit % input_size
    shifted_data = (data << n_bit) | (data >> (input_size - n_bit))
    shifted_data &= (1 << input_size) - 1

    return shifted_data
