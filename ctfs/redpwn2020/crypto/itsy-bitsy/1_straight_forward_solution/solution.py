from pwn import remote

def bit_str_xor(bit_str_1, bit_str_2):
    xor_res = ''
    for i in range(len(bit_str_1)):
        bit_1 = bit_str_1[i]
        bit_2 = bit_str_2[i]
        xor_res += str(int(bit_1) ^ int(bit_2))
    return xor_res


def get_cipher(prime):
    conn = remote("2020.redpwnc.tf", 31284)
    conn.sendline(str(prime-1))
    conn.sendline(str(prime))
    conn.readuntil("Ciphertext: ")
    cipher = conn.read().strip().decode('utf-8')
    return (prime, cipher)


def obtain_ciphers():
    primes = [2,3,5,7,9,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,293,307,311,313]
    return [get_cipher(prime) for prime in primes]  # Returns a list of tuples [(prime, ciphertext)]


def change_bits(cipher, n):
    f = ''
    for i in range(len(cipher)):
        if i % n == 0:
            f += bit_str_xor(cipher[i], '1')
        else:
            f += '?'

    return(f)


def get_partial_flags(ciphers):
    partial_flags = []
    for n, cipher in ciphers:
        partial_flags.append(change_bits(cipher, n))
    return partial_flags


def build_final_flag_bits(partial_flags):
    final_flag_bits = ''
    for i in range(len(partial_flags[0])):
        bit = '?'
        for f in partial_flags:
            if f[i] in ('0', '1'):
                bit = f[i]
                break

        final_flag_bits += bit

    return final_flag_bits


def decode_flag_bits(flag_bits):
    final_flag = ''
    groups = [flag_bits[i:i+7] for i in range(0, len(flag_bits), 7)]
    for g in groups:
        if '?' in g:
            final_flag += '?'
        else:
            final_flag += chr(int(g, 2))
    return final_flag


def decipher_itsy_bitsy():
    ciphers = obtain_ciphers()

    partial_flags = get_partial_flags(ciphers)

    flag_bits = build_final_flag_bits(partial_flags)

    final_flag = decode_flag_bits(flag_bits)

    print(final_flag)

if __name__ == "__main__":
    decipher_itsy_bitsy()

