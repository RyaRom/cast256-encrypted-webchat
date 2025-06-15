import cast256


def concat(decrypted: list[int]):
    to_bytes = map(lambda x: x.to_bytes(4, byteorder='big'), decrypted)
    return b''.join(to_bytes)


def main():
    key = cast256.random_key(32)
    data = 'super secret message woof woof :3 woof woof :3'
    encrypted = cast256.encrypt(data, key)
    print(cast256.decrypt(encrypted, key))


if __name__ == "__main__":
    main()
