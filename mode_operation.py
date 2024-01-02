from os import urandom
import cast256

def rdm_iv_generator():
    """
    Cette fonction doit pouvoir générer un nombre aléatoire de 128bits
    :return: un entier représenté sur 128 bits généré de manière aléatoire.
    """
    return int.from_bytes(urandom(16), byteorder="big")


def encrypt_ecb(blocks, key):
    """
    Cette fonction applique le chiffrement CAST256 à une liste de blocs de 128 bits suivant le mode d'opération ECB.
    :param blocks: Liste de blocs (128bits) à chiffrer.
    :param key: clé de chiffrement 256 bits
    :return: la liste de blocs chiffrés.
    """
    return [cast256.encrypt_block(block, key) for block in blocks]


def decrypt_ecb(blocks, key):
    """
    Cette fonction dé-chiffre une liste de blocs de 128 bits qui a été préalablement chiffrée
    avec la méthode CAST256 suivant le mode d'opération ECB.
    :param blocks: Liste de blocs à déchiffrer.
    :param key: clé de chiffrement 256 bits
    Identique à celle utilisée pour le chiffrement.
    :return: la liste de blocs déchiffrés.
    """
    return [cast256.decrypt_block(block, key) for block in blocks]


def encrypt_cbc(blocks, key):
    """
    Cette fonction applique le chiffrement CAST256 à une liste de blocs de 128 bits suivant le mode d'opération CBC.
    :param blocks: Liste de blocs à chiffrer.
    :param key: clé de chiffrement 256 bits
    :return: la liste de blocs chiffrés avec le vecteur initial utilisé en première position.
    """
    iv = rdm_iv_generator()
    encrypted_blocks = [iv]

    temp = iv

    for block in blocks:
        temp = cast256.encrypt_block(block ^ temp, key)
        encrypted_blocks.append(temp)

    return encrypted_blocks


def decrypt_cbc(blocks, key):
    """
    Cette fonction dé-chiffre une liste de blocs de 128 bits qui a été préalablement chiffrée
    avec la méthode CAST256 suivant le mode d'opération CBC.
    :param blocks: Liste de blocs à déchiffrer.
    :param key: clé de chiffrement 256 bits
    Identique à celle utilisée pour le chiffrement.
    :return: la liste de blocs déchiffrés.
    """
    temp = blocks.pop(0)

    decrypted_blocks = []

    for block in blocks:
        decrypted_blocks.append(cast256.decrypt_block(block, key) ^ temp)
        temp = block

    return decrypted_blocks


def decrypt(blocks, key, operation_mode="ECB"):
    """
    Cette fonction dé-chiffre une liste de blocs de 128 bits qui a été préalablement chiffrée
    avec la méthode CAST256 suivant le mode d'opération CBC ou ECB.
    :param blocks: Liste de blocs à déchiffrer.
    :param key: la clé de chiffrement 256 bit
    :param operation_mode: string spécifiant le mode d'opération ("ECB" ou "CBC")
    :return: la liste de blocs déchiffrés.
    """
    return decrypt_ecb(blocks, key) if operation_mode == "ECB" else decrypt_cbc(blocks, key)


def encrypt(blocks, key, operation_mode="ECB"):
    """
    Cette fonction applique le chiffrement CAST256 à une liste de blocs de 128 bits.
    :param blocks: Liste de blocs à chiffrer.
    :param key: la clé de chiffrement 256 bit
    :param operation_mode: string spécifiant le mode d'opération ("ECB" ou "CBC")
    :return: la liste de blocs chiffrés avec le vecteur initial utilisé en première position.
    """
    return encrypt_ecb(blocks, key) if operation_mode == "ECB" else encrypt_cbc(blocks, key)
