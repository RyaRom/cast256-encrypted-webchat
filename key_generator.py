from cast256_kernel import *


def forward_octave(abcdefgh, tr, tm):
    """
    Эта функция реализует "прямую октаву" (forward octave) алгоритма CAST-256.
    Она разбивает 256-битный входной блок на восемь 32-битных блоков (A, B, C, D, E, F, G, H),
    и применяет к ним последовательность функций f1, f2 и f3, используя заданные ключи поворота (tr)
    и маскирующие ключи (tm).

    :param abcdefgh: входной 256-битный блок
    :param tr: список из 8 ключей поворота (по 8 бит)
    :param tm: список из 8 масок (по 32 бита)
    :return: модифицированный 256-битный блок
    """
    a, b, c, d, e, f, g, h = utils.extract_32bit_bloc_from_256(abcdefgh)

    g = g ^ function1(h, tr[0], tm[0])
    f = f ^ function2(g, tr[1], tm[1])
    e = e ^ function3(f, tr[2], tm[2])
    d = d ^ function1(e, tr[3], tm[3])
    c = c ^ function2(d, tr[4], tm[4])
    b = b ^ function3(c, tr[5], tm[5])
    a = a ^ function1(b, tr[6], tm[6])
    h = h ^ function2(a, tr[7], tm[7])

    return utils.build_256_bit_bloc_from_32_bit_blocs(a, b, c, d, e, f, g, h)


def initialization():
    """
    Инициализирует таблицы ключей поворота (tr) и масок (tm),
    необходимые для генерации ключей CAST-256.

    Возвращает два двумерных списка 24x8:
    - tr: 24 строки по 8 ключей поворота
    - tm: 24 строки по 8 масок
    """

    cm = 0x5A827999
    cr = 19
    mm = 0x6ED9EBA1
    mr = 17

    tr = [[0] * 8 for _ in range(24)]
    tm = [[0] * 8 for _ in range(24)]

    for i in range(24):
        for j in range(8):
            tm[i][j] = cm
            cm = utils.sum_mod_232(cm, mm)
            tr[i][j] = cr
            cr = (cr + mr) % 32

    return tr, tm


def key_generator(key):
    """
    Генерирует раундовые ключи (kr, km) из основной 256-битной ключа для CAST-256.

    :param key: основной ключ шифрования (256 бит)
    :return: два списка:
        - kr: список из 12 строк по 4 ключа поворота
        - km: список из 12 строк по 4 маски
    """
    kr = []
    km = []

    tr, tm = initialization()

    for i in range(12):
        key = forward_octave(key, tr[2 * i], tm[2 * i])
        key = forward_octave(key, tr[(2 * i) + 1], tm[(2 * i) + 1])

        a, b, c, d, e, f, g, h = utils.extract_32bit_bloc_from_256(key)

        kr.append([
            a & 0b11111,
            c & 0b11111,
            e & 0b11111,
            g & 0b11111
        ])

        km.append([h, f, d, b])

    return kr, km