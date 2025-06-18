import cast256


def main():
    key = cast256.random_key()
    data = 'Hi:3'
    encrypted = cast256.encrypt(data, key)
    decoded = cast256.decrypt(encrypted, key).decode()
    print(decoded)


if __name__ == "__main__":
    main()
