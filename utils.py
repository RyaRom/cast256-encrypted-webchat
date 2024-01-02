"""
Ce fichier comprend une série de fonctions utiles qui effectuent des opérations basiques arithmétiques et binaires.
"""


def sum_mod_232(a, b):
    """
    Cette fonction effectue une somme dans un espace modulo 2 puissance 32
    :param a: premier terme
    :param b: second terme
    :return: la somme modulo 2 puissance 32
    """
    return (a + b) % (2 ** 32)


def diff_mod_232(a, b):
    """
    Cette fonction effectue une différence dans un espace modulo 2 puissance 32
    :param a: premier terme
    :param b: second terme
    :return: la différence entre me premier et le second terme modulo 2 puissance 32
    """
    return (a - b) % (2 ** 32)


def build_128_bit_bloc_from_32_bit_blocs(a, b, c, d):
    """
    Cette fonction assemble des blocs de 32bits en un seul bloc de 128 bit. Les blocs en paramètres sont ordonnées
    du plus fort au plus faible, c'est-à-dire, dans l'odre d'apparition final de gauche à droite.
    :param a: 1er bloc de 32bits
    :param b: 2ème bloc de 32bits
    :param c: 3ème bloc de 32 bits
    :param d: 4ème bloc de 32bits
    :return: un bloc de 128 bits correspondant à l'ordre 'abcd'
    """
    """
    Pour se faire, j'ai décalé les block a la position attendue grâce à un shift left.
    Et pour regrouper les blocks, j'ai simplement utilisé l'opérateur 'OR' car lors
    du shift left, tous les bits a droites sont initialisé a 0.
    """
    return (a << 96) | (b << 64) | (c << 32) | d


def extract_32bit_bloc_from_128(abcd):
    """
    Cette fonction décompose un bloc de 128 bits en 4 blocs de 32bits. Les blocs de sortie sont sont ordonnées
    du plus fort au plus faible, c'est-à-dire, dans l'odre d'apparition de départ de gauche à droite
    :param abcd: bloc de 128 bits
    :return: 4 blocs de 32 bits a, b, c, d tel que abcd soit le bloc de départ
    """
    """
    Pour ce faire, j'ai créé un masque de 32 bits initialisé à 1.
    Ensuite, j'ai utilisé un shift right permettant de décaler mes 32 bits à droite.
    Pour enfin, leur appliquer mon masque
    et grace à l'opérateur "AND'" récupérer les valeurs des bits du bloc.
    """
    # Masque pour extraire 32 bits
    mask_32_bits = 0xFFFFFFFF
    # Extraction des blocs a, b, c et d.
    a = (abcd >> 96) & mask_32_bits
    b = (abcd >> 64) & mask_32_bits
    c = (abcd >> 32) & mask_32_bits
    d = abcd & mask_32_bits
    return a, b, c, d


def extract_32bit_bloc_from_256(abcdefgh):
    """
    Cette fonction décompose un bloc de 256 bits en 8 blocs de 32bits. Les blocs de sortie sont sont ordonnées
    du plus fort au plus faible, c'est-à-dire, dans l'odre d'apparition de départ de gauche à droite
    :param abcdefgh: bloc de 128 bits
    :return: 8 blocs de 32 bits a, b, c, d, e, f, g, h tel que abcdefgh soit le bloc de départ
    """
    """
    Même procéder que pour les blocs de 128 bits.
    """
    # Masque pour extraire 32 bits
    mask_32_bits = 0xFFFFFFFF
    # Extraction des blocs a, b, c, d, e, f, g et h.
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
    Cette fonction assemble des blocs de 32bits en un seul bloc de 256 bit. Les blocs en paramètres sont ordonnées
    du plus fort au plus faible, c'est-à-dire, dans l'odre d'apparition final de gauche à droite
    :param a: 1er bloc de 32bits
    :param b: 2ème bloc de 32bits
    :param c: 3ème bloc de 32 bits
    :param d: 4ème bloc de 32bits
    :param e: 5ème bloc de 32bits
    :param f: 6ème bloc de 32bits
    :param g: 7ème bloc de 32 bits
    :param h: 8ème bloc de 32bits
    :return: un bloc de 256 bits correspondant à l'ordre 'abcdefgh'
    """
    """
    Même procéder que pour les blocs de 128 bits.
    """
    return (a << 224) | (b << 192) | (c << 160) | (d << 128) | (e << 96) | (f << 64) | (g << 32) | h


def extract_8bit_blocs_from_32(abcd):
    """
    Cette fonction décompose un bloc de 32 bits en 4 blocs de 8bits. Les blocs de sortie sont sont ordonnées
    du plus fort au plus faible, c'est-à-dire, dans l'odre d'apparition de départ de gauche à droite
    :param abcd: bloc de 32 bits
    :return: 4 blocs de 8 bits a, b, c, d tel que abcd soit le bloc de départ
    """
    """
    Pour ce faire, j'ai créé un masque de 8 bits initialisé à 1.
    Ensuite, j'ai utilisé un shift right permettant de décaler mes 8 bits à droite.
    Pour enfin, leur appliquer mon masque
    et grace à l'opérateur "AND'" récupérer les valeurs des bits du bloc.
    """
    # Masque pour extraire 8 bits
    mask_8_bits = 0xFF
    # Extraction des blocs a, b, c et d
    a = (abcd >> 24) & mask_8_bits
    b = (abcd >> 16) & mask_8_bits
    c = (abcd >> 8) & mask_8_bits
    d = abcd & mask_8_bits
    return a, b, c, d


def shift_left(data, input_size, n_bit):
    """
    Cette fonction doit être capable de barrel-shifter vers la gauche de n_bit éléments
    l'argument data de taille input_size
    :param data: L'entier à shifter.
    :param input_size: La taille en bits de data.
    :param n_bit: nombre de bit à shifter
    :return: L'entier data shifté de n-bit vers la gauche
    """
    """
    Pour ce faire, j'effectue le décalage de n bit sur la gauche.
    Ensuite, j'effectue un décalage de data de la taille de l'input size moins n bit.
    Pour finir, par les regrouper grace à l'opérateur "OR'".
    Et finalement, vérifier que le résultat reste dans les limites de l'input size.
    """
    n_bit = n_bit % input_size
    # Décalage
    shifted_data = (data << n_bit) | (data >> (input_size - n_bit))
    # Vérification que le résultat reste dans les limites de 'input_size'
    shifted_data &= (1 << input_size) - 1

    return shifted_data
