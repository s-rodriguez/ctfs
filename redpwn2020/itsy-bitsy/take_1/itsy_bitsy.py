#!/usr/bin/env python3
import enchant
from Crypto.Random.random import randint

ENG_DICT = enchant.Dict("en_US")

def str_to_bits(s):
    bit_str = ''
    for c in s:
        i = ord(c)
        bit_str += bin(i)[2:]
    return bit_str

def bits_to_str(bits):
    groups = [bits[i:i+7] for i in range(0, len(bits), 7)]
    chars = [chr(int(i, 2)) for i in groups]
    return ''.join(chars)

def recv_input():
    i = input('Enter an integer i such that i > 0: ')
    j = input('Enter an integer j such that j > i > 0: ')
    try:
        i = int(i)
        j = int(j)
        if i <= 0 or j <= i:
            raise Exception
    except:
        print('Error! You must adhere to the restrictions!')
        exit()
    return i,j

def generate_random_bits(lower_bound, upper_bound, number_of_bits):
    #bit_str = '1010111111111011101110111011' # flag
    bit_str = '101011111111101110111011101110111110' # flag{

    while len(bit_str) < number_of_bits:
        r = randint(lower_bound, upper_bound)
        bit_str += bin(r)[2:]
    return bit_str[:number_of_bits]

def generate_random_bits_with_history(lb,ub,n, existent_random_bits):
    rb = generate_random_bits(lb, ub, n)
    while rb in existent_random_bits:
        rb = generate_random_bits(lb, ub, n)
    return rb

def bit_str_xor(bit_str_1, bit_str_2):
    xor_res = ''
    for i in range(len(bit_str_1)):
        bit_1 = bit_str_1[i]
        bit_2 = bit_str_2[i]
        xor_res += str(int(bit_1) ^ int(bit_2))
    return xor_res

def contains_possible_chars(text):
    for c in text:
        i = ord(c)
        assert i in range(2**6,2**7)

def main():
    with open('flag.txt','r') as f:
        flag = f.read().rstrip()
    for c in flag:
        i = ord(c)
        assert i in range(2**6,2**7)
    flag_bits = str_to_bits(flag)
    i,j = recv_input()
    lb = 2**i
    ub = 2**j - 1
    n = len(flag_bits)
    random_bits = generate_random_bits(lb,ub,n)
    encrypted_bits = bit_str_xor(flag_bits,random_bits)
    print(f'Ciphertext: {encrypted_bits}')

def generate_random_bits_v2(perm, number_of_bits):
    bit_str = '10101111111110111011101110111011111' # flag{
    bit_str += perm
    return bit_str[:number_of_bits]


#def main3():
#    cipher = '0110001001001000101101011100010010010111010011100101111001011000110001'
#    lb = 2
#    ub = 3
#    n = len(cipher)
#
#    decrypted_str = ''
#    existent_rb = set()
#    while True:
#        random_bits = generate_random_bits_with_history(lb,ub,n,existent_rb)
#        existent_rb.add(random_bits)
#        decrypted_bits = bit_str_xor(cipher, random_bits)
#        decrypted_str = bits_to_str(decrypted_bits)
#        try:
#            contains_possible_chars(decrypted_str)
#            #print(f'{decrypted_str}')
#            print(f'{decrypted_str}\tRandom bits: {random_bits}')
#        except AssertionError:
#            pass
#    #print(f'Found! Random bits: {random_bits}')

def main4():
    cipher = '0110001001001000101101011100010010010111010011100101111001011000110001011000100011100110100100000000111100010001001000011000000111010101111000010111110000011001100000000100000101010001000001001111001110100011100000000101100001101000001011001101000110000100000000100100011111000000010101000110100000000'

    f = ''
    for i in range(len(cipher)):
        if i % 2 == 0:
            f += bit_str_xor(cipher[i], '1')
        else:
            f += '?'

    print(f)

FILTERED_CANDIDATES = set()
POTENTIAL_FLAGS = set()

def build_candidate(potential_letters, candidate=''):
    if not potential_letters:
        #poss_cand = candidate.split('flag{')[1].lower()
        poss_cand = candidate.lower()
        #if ENG_DICT.check(poss_cand):
        #    FILTERED_CANDIDATES.add(poss_cand)
        if poss_cand in ('bits','fucking','get','down','the','water','spout'):
            FILTERED_CANDIDATES.add(candidate)

    else:
        letters = potential_letters[0]
        for letter in letters:
            cd = candidate + letter
            build_candidate(potential_letters[1:], cd)

def build_potential_flags(potential_words, flag=''):
    if not potential_words:
        POTENTIAL_FLAGS.add('flag{' + flag[:-1] + '}')
    else:
        words = potential_words[0]
        for word in words:
            fl = flag + word + '_'
            build_potential_flags(potential_words[1:], fl)

def print_set(some_set):
    for c in sorted(some_set):
        print(c)


def potential_flag():
    potential_flag = '1100110110110011000011100111111101111?0?1?1?0?0?111?0?0?1?1?0?110?1?1?1?0?1?011?0?0?1?0?0?111?1?1?1?0?0?111?1?1?1?0?1?110?1?1?1?0?1?111?0?0?1?1?1?010?1?1?1?0?1?011?1?1?1?1?1?111?1?1?1?1?1?111?0?0?1?0?0?011?0?0?1?1?1?111?0?1?1?0?0?111?0?0?1?0?1?111?0?1?1?1?1?111?0?1?1?1?0?011?1?1?1?1?1?111?0?0?1111101'

    possible_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.,'
    perms = (
        ('0','0','0'),
        ('1','0','0'),
        ('0','1','0'),
        ('1','1','0'),
        ('0','0','1'),
        ('1','0','1'),
        ('0','1','1'),
        ('1','1','1'),
    )

    groups = [potential_flag[i:i+7] for i in range(0, len(potential_flag), 7)]

    potential_letters = []

    for pos, group in enumerate(groups):
        #print(f'======Pos {pos}======')

        if '?' in group:
            letters = []
            for p in perms:
                letter_bit = group.replace('?', p[0], 1).replace('?', p[1], 1).replace('?', p[2], 1)
                letter = bits_to_str(letter_bit)
                if letter in possible_letters:
                    #print(letter, letter_bit)
                    letters.append(letter)
            potential_letters.append(letters)

        else:
            letter = bits_to_str(group)
            #print(letter, group)
            potential_letters.append([letter])

    # underscores - 9 17 21 24 26 30 36 40 42

    build_candidate(potential_letters[5:9])
    w1 = list(FILTERED_CANDIDATES)
    FILTERED_CANDIDATES.clear()

    build_candidate(potential_letters[10:17])
    w2 = list(FILTERED_CANDIDATES)
    FILTERED_CANDIDATES.clear()

    build_candidate(potential_letters[18:21])
    w3 = list(FILTERED_CANDIDATES)
    FILTERED_CANDIDATES.clear()

    build_candidate(potential_letters[22:26])
    w4 = list(FILTERED_CANDIDATES)
    FILTERED_CANDIDATES.clear()

    build_candidate(potential_letters[27:30])
    w5 = list(FILTERED_CANDIDATES)
    FILTERED_CANDIDATES.clear()

    build_candidate(potential_letters[31:36])
    w6 = list(FILTERED_CANDIDATES)
    FILTERED_CANDIDATES.clear()

    build_candidate(potential_letters[37:42])
    w7 = list(FILTERED_CANDIDATES)

    potential_words = [w1, w2, w3, w4, w5, w6, w7]

    build_potential_flags(potential_words, flag='')

    print_set(POTENTIAL_FLAGS)

    #print_candidates()

#    while True:
#        candidate = ''
#        for i in potential_flag:
#            if i == '?':
#                candidate += str(randint(0,1))
#            else:
#                candidate += i
#        print(bits_to_str(candidate))


if __name__ == '__main__':
    potential_flag()


cipher = '0110001001001000101101011100010010010111010011100101111001011000110001011000100011100110100100000000111100010001001000011000000111010101111000010111110000011001100000000100000101010001000001001111001110100011100000000101100001101000001011001101000110000100000000100100011111000000010101000110100000000'

local_rb = '101011101111101110111011101111111010111110111010111110101110111011111010111111111110'
local_cip = '011000110100100010110101110000110111010010001010000111010010001101001001111100011001'


f = '110011011011001100001110011111001101101100110000111001111100110110110011000011100111'
k = '101011101111101110111011101111111010111110111010111110101110111011111010111111111110'

c = '011000110100100010110101110000110111010010001010000111010010001101001001111100011001'

d = '1?0?100?1?1'





c = '0110001001001000101101011100010010010111010011100101111001011000110001011000100011100110100100000000111100010001001000011000000111010101111000010111110000011001100000000100000101010001000001001111001110100011100000000101100001101000001011001101000110000100000000100100011111000000010101000110100000000'
k = '10101111111110111011101110111011111?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1'
f = '11001101101100110000111001111111011?1?0?1?1?0?0?1?1?0?0?1?1?0?1?0?1?1?1?0?1?0?1?0?0?1?0?0?1?1?1?1?1?0?0?1?1?1?1?1?0?1?1?0?1?1?1?0?1?1?1?0?0?1?1?1?0?0?1?1?1?0?1?0?1?1?1?1?1?1?1?1?1?1?1?1?1?1?1?0?0?1?0?0?0?1?0?0?1?1?1?1?1?0?1?1?0?0?1?1?0?0?1?0?1?1?1?0?1?1?1?1?1?1?0?1?1?1?0?0?1?1?1?1?1?1?1?1?0?0?1111101'


# for i in range(len(groups)):
#    if groups[i].startswith('?'):
#        groups[i] = '1' + groups[i][1:]
