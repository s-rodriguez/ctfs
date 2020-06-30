import base91

def decipher():
    with open('crypto/Incognito/incognito_decompressed') as f:
        content = f.read()

    decode=base91.decode(content)

    with open('crypto/Incognito/base91_dec.png', 'wb') as f:
        f.write(decode)

if __name__ == "__main__":
    decipher()