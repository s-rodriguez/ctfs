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
    bit_str = '101011111111101110111011101110111110' # flag{

    while len(bit_str) < number_of_bits:
        r = randint(lower_bound, upper_bound)
        bit_str += bin(r)[2:]
    return bit_str[:number_of_bits]

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

FILTERED_CANDIDATES = set()

def _build_candidate(potential_letters, candidate=''):
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

def build_candidate(potential_letters, candidate=''):
    FILTERED_CANDIDATES.clear()
    _build_candidate(potential_letters, '')
    candidates = list(FILTERED_CANDIDATES)
    return candidates


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
    intervals = (
        (5, 9),
        (10, 17),
        (18, 21),
        (22, 26),
        (27, 30),
        (31, 36),
        (37, 42),
    )

    potential_words = []
    for i, j in intervals:
        interval_words = build_candidate(potential_letters[i:j])
        potential_words.append(interval_words)

    print(potential_words)


if __name__ == '__main__':
    potential_flag()
