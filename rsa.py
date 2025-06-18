from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def generate_keys(public_exponent=65537, key_size=2048):
    private_key = rsa.generate_private_key(public_exponent=public_exponent, key_size=key_size)
    public_key = private_key.public_key()
    return private_key, public_key


def encrypt(public_key, plaintext: bytes):
    return public_key.encrypt(
        plaintext,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )


def decrypt(private_key, ciphertext: bytes):
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )