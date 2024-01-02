from  utils import *
from functions_cast256 import *


def forward_octave(abcdefgh, tr, tm):
    """
      Cette fonction correspond à la forward_octave du cast-256. Elle décompose le bloc d'entrée 256bits en
      blocs de 32bits. Ces blocs sont transformés par l'utilisation des fonctions f1, f2 et f3 du cast-256 en utilisant
      les clés de rotation et de masque. Les blocs obtenus sont recomposés en un bloc de 256bits.
      !!! ATTENTION A L'ORDRE DES OPERATIONS INDIQUE DANS LA DOCUMENTATION !!!
      :param abcdefgh: le bloc à traité (256bits)
      :param tr: tableau de 8 clés de rotation (8bits)
      :param tm: tableau de 8 clés de masque (32bits)
      :return: le résultat des opérations (256bits)
      """

    """
    Let "KAPPA <- Wi(KAPPA)" be short-hand notation for the following:
    G = G ^ f1(H, Tr0_(i), Tm0_(i))
    F = F ^ f2(G, Tr1_(i), Tm1_(i))
    E = E ^ f3(F, Tr2_(i), Tm2_(i))
    D = D ^ f1(E, Tr3_(i), Tm3_(i))
    C = C ^ f2(D, Tr4_(i), Tm4_(i))
    B = B ^ f3(C, Tr5_(i), Tm5_(i))
    A = A ^ f1(B, Tr6_(i), Tm6_(i))
    H = H ^ f2(A, Tr7_(i), Tm7_(i))
    (W(*) is called a "forward octave".)
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
    Cette fonction crée les clés de rotation tr et de masque tm utiles à la génération des clés du cast-256.
    :return: deux tableaux à deux dimensions 8x24 (24 lignes et 8 colonnes) contenant respectivement
    les clés de rotation tr et de masque tm.
    """
    """
    Initialization:
    Cm = 2**30 * SQRT(2) = 5A827999 (base 16)
    Mm = 2**30 * SQRT(3) = 6ED9EBA1 (base 16)
    Cr = 19
    Mr = 17
    for (i=0; i<24; i++)
    {
        for (j=0; j<8; j++)
        {
            Tmj_(i) = Cm
            Cm = (Cm + Mm) mod 2**32
            Trj_(i) = Cr
            Cr = (Cr + Mr) mod 32
        }
    }
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
    Cette fonction génère les clés de rotation kr et de masque km pour le chiffrement cast-256 à partir de la clé 256bits
    de chiffrement et des clés de rotation tr et de masque tm.
    :param key: la clé de chiffrement (256bits)
    :return: deux tableaux à deux dimensions 12x4 (12 lignes et 4 colonnes) contenant respectivement
    les clés de rotation kr et de masque km.
    """

    """
    Key Schedule:
    KAPPA = ABCDEFGH = 256 bit of primary key, K.
    for (i=0; i<12; i++)
    {
    KAPPA <- W2i(KAPPA)
    KAPPA <- W2i+1(KAPPA)
    Kr_(i) <- KAPPA
    Km_(i) <- KAPPA
    }

    """
    kr = []
    km = []

    tr, tm = initialization()

    for i in range(12):
        key = forward_octave(key, tr[2*i], tm[2*i])
        key = forward_octave(key, tr[(2*i)+1], tm[(2*i)+1])

        a, b, c, d, e, f, g, h = utils.extract_32bit_bloc_from_256(key)

        kr.append([
            a & 0b11111,
            c & 0b11111,
            e & 0b11111,
            g & 0b11111
        ])

        km.append([h, f, d, b])

    return kr, km