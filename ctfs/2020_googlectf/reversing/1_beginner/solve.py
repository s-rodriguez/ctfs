from copy import deepcopy

_MAX_LEN = 16

_ADDR32 = [0xef,0xbe,0xad,0xde,0xad,0xde,0xe1,0xfe,0x37,0x13,0x37,0x13,0x66,0x74,0x63,0x67]

_SHUFFLE = [2, 6, 7, 1, 5, 11, 9, 14, 3, 15, 4, 8, 10, 12, 13, 0]
_SHUFFLE_MAP = {  # From index key to inxed value
    0: 15,
    1: 3,
    2: 0,
    3: 8,
    4: 10,
    5: 4,
    6: 1,
    7: 2,
    8: 11,
    9: 6,
    10: 12,
    11: 5,
    12: 13,
    13: 14,
    14: 7,
    15: 9,
}

_XOR = [0x76,0x58,0xb4,0x49,0x8d,0x1a,0x5f,0x38,0xd4,0x23,0xf8,0x34,0xeb,0x86,0xf9,0xaa]
_EXPECTED_PREFIX = 'CTF{'


def to_ascii(value):
    return ''.join([chr(i) for i in value])


def shuffle_flag(flag_bytes):
    shuffled = [0 for i in range(_MAX_LEN)]

    for from_idx, to_idx in _SHUFFLE_MAP.items():
        shuffled[to_idx] = deepcopy(flag_bytes[from_idx])
    return shuffled

def do_paddd(shuffled):
    added = [0 for i in range(len(shuffled))]

    for block_id in range(len(shuffled)//4):
        carry = 0
        for index_id in range(4):
            id = block_id*4 + index_id
            aux = shuffled[id] + _ADDR32[id]

            if carry:
                aux += 1
                carry = 0
            
            if len(bin(aux)[2:].zfill(8)) > 8:
                aux = aux & 255
                carry = 1
            #elif bin(aux)[2:].zfill(8).startswith('1'):
            #    aux -= 256

            added[id] = aux

    return added

def perform_xor(padded):
    xored = [0 for i in range(len(padded))]

    for i in range(len(padded)):
        xored[i] = padded[i] ^ _XOR[i]
    
    return xored


def solve(flag):
    flag_bytes = [ord(i) for i in flag]
    while len(flag_bytes) < 16:
        flag_bytes += [0x00]  # Append null byte

    print(f'Flag: \n\t{flag_bytes}\n\t{flag}')

    shuffled = shuffle_flag(flag_bytes)
    print(f'PSHUFB: \n\t{shuffled}\n\t{to_ascii(shuffled)}')

    padded = do_paddd(shuffled)
    print(f'PADDD: \n\t{padded}\n\t{to_ascii(padded)}')

    xored = perform_xor(padded)
    print(f'PXOR: \n\t{xored}\n\t{to_ascii(xored)}\n')

if __name__ == "__main__":
    #flag = 'abcdefghijklmno'
    flag = 'CTF{S1MDf0rM3!}'
    solve(flag)