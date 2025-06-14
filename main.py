import mode_operation


def concat(decrypted: list[int]):
    to_bytes = map(lambda x: x.to_bytes(4, byteorder='big'), decrypted)
    return b''.join(to_bytes)


def main():
    # key = os.urandom(32)
    key = mode_operation.random_key()
    data = 'super secret message woof woof :3 woof woof :3'
    encrypted = mode_operation.encrypt(data, key)
    print(encrypted)
    print(mode_operation.decrypt(encrypted, key))


if __name__ == "__main__":
    main()
