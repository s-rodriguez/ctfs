import hashlib

MD5_SUM = '080d5caaed95af9ab072c41de3a73c24'

ASCII = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-{}[].,'

def get_possible_combinations(cipher_bytes):
    combinations = []
    for cb in cipher_bytes:
        cb_comb = []
        for i in range(256):
            xor_res = int(cb, 16) ^ i
            if 32 <= xor_res <= 126:
                cb_comb.append(chr(xor_res))
        combinations.append(cb_comb)
    return combinations


def build_potential_flags(combinations, flag=''):
    if not combinations:
        hash_flag = hashlib.md5(flag.encode()).hexdigest()
        if hash_flag == MD5_SUM:
            print(flag, hash_flag)
            raise Exception()
    else:
        letters = combinations[0]
        for l in letters:
            fl = flag + l
            build_potential_flags(combinations[1:], fl)


def decipher(cipher, flag):
    cipher_bytes = [cipher[i:i+2] for i in range(0, len(cipher), 2)]

    print(cipher_bytes)

    combinations = get_possible_combinations(cipher_bytes)

    build_potential_flags(combinations, flag)


if __name__ == "__main__":
    cipher = '607f78fbffe520efc7caebd2137940ddb26c30c2fd37ed743b77038d326a9c7e7e80'
    flag='EKO{'
    decipher(cipher, flag)

    ## si llego aca, no encontro con el shortcut, pruebo cipher completo
    print("fallo shortcut, probando completo")
    cipher = 'd740a5dc607f78fbffe520efc7caebd2137940ddb26c30c2fd37ed743b77038d326a9c7e7e80'
    flag = ''
    decipher(cipher, flag)

    print("no encontre nada che")