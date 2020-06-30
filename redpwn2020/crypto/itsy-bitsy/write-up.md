# Itsy Bitsy

## Flag
```
flag{bits_leaking_out_down_the_water_spout}
```

## Introduction
Uppon connection, we are requested to inputs (i, j) and then the Ciphertext is printed:

```
$ nc 2020.redpwnc.tf 31284
Enter an integer i such that i > 0: 1
Enter an integer j such that j > i > 0: 2
Ciphertext: 0010001100001000111101011000000111010011000111100100101101011100110000011101110111100111100000010101101001000101001000011001010011010000101101010011110000011001110100000000000001000101000000001111011111110011100100010001100101111100011111011000010011000100010100100000001110000001010100010111110101010
```

## Analysis of the provided source code
Looking at the code provided, we see that those (i,j) inputs are being to calculate a `lower_bound` and an `uper_bound`:

```python
    ...
    lb = 2**i
    ub = 2**j - 1
```

And that those bounds are then used to generate a kind of "OTP" key, which is basically a random int between the bounds. In our first attempt (see above), with an input of (1,2) the key will be composed of `2s` and `3s`

```python
def generate_random_bits(lower_bound, upper_bound, number_of_bits):
    bit_str = ''
    while len(bit_str) < number_of_bits:
        r = randint(lower_bound, upper_bound)
        bit_str += bin(r)[2:]
    return bit_str[:number_of_bits]
```

Which is later XORed against the flag to generate the ciphertext:

```python
    ...
    encrypted_bits = bit_str_xor(flag_bits,random_bits)
    print(f'Ciphertext: {encrypted_bits}')
```

## Solution (The straightforward way)
There are two things to notice:
1. The ciphertext will probably begin with `flag{` and finish with `}`
1. When we used the inputs (1,2), the key was composed by `2s` and `3s`, so basically `10` and `11`, which we could say that is a string of `1X`s. This means that all even positions will always have a `1`

Now, the key to the challenge is basically in the second one, since it's how the xorKey is being built (Initially I didn't spend more time thinking on it and I basically jumped into a hurricane that took me to Oz)

So, when we think some more on how the xorKey is being built and what we can know from the input we send,what we do is request for the ciphertext using different `(i,j)`s variations up until the length of the ciphertext. For each new ciphertext we'll know how the key was conformed:

| j | key_format |
|---:|------------:|
| 2 | 1X |
| 3 | 1XX |
| 4 | 1XXX |
| 5 | 1XXXX |

We can even see that there is no need to ask for all j's less than the length of the ciphertext, we can ask only for those j's that are prime. (j=2 will cover for j=4 for example).

| j | key_format |
|---:|------------:|
| 2 | 1X |
| 3 | 1XX |
| 5 | 1XXXX |
| 7 | 1XXXXXX |
| ... | ... |

For each obtained ciphertext, we can XOR the bits we know and build the complete flag.

This can look like:

```python

def decipher():
    # list for illustration. no need to manually call for each prime number, can be done automatically
    ciphers = [
        #(j, ciphertext_obtained)
        (2, '00100111010110001011......'),
        (3, '01011011010110000011......'),
        (5, '00110011110100000011......'),
        (7, '00111110001110000101......'),
        (9, '01100000111101001010......'),
        ...
    ]

    partial_flags = []
    for n, cipher in ciphers:
        partial_flags.append(change_bits(cipher, n))
    
    final_flag = build_flag(partial_flags)
    print(final_flag)

# Aux methods
def change_bits(cipher, n):
    """For every known bit of the key (which is if the position is module of n) do the XOR against the cipher. For the rest of them, just leave a ? as placeholder"""
    f = ''
    for i in range(len(cipher)):
        if i % n == 0:
            f += bit_str_xor(cipher[i], '1')
        else:
            f += '?'

    return(f)

def build_flag(partial_flags):
    """Build final flag based on the known bits of the different partial flags"""
    final_flag = ''
    for i in range(len(flags[0])):
        bit = '?'
        for f in flags:
            if f[i] in ('0', '1'):
                bit = f[i]
                break

        final_flag += bit
```

Running this, we'll decipher the flag:

```
flag{bits_leaking_out_down_the_water_spout}
```

### Obtain the ciphers automatically
```python
from pwn import *

def get_cipher(prime):
    conn = remote("2020.redpwnc.tf", 31284)
    conn.sendline(str(prime-1))
    conn.sendline(str(prime))
    conn.readuntil("Ciphertext: ")
    cipher = conn.read().strip()
    return (prime, cipher)

def obtain_ciphers():
    primes = [2, 3, 5, 7, 11, 13, 17, ...]
    return [get_cipher(prime) for prime in primes]  # Returns a list of tuples [(prime, ciphertext)]
```

## Kind of a Solution (The jump into a hurricane that got me to Oz)
Ok, even though this is not the correct way to solve the challenge, it's the path that I took until I realized I messed up at some point along the way.
It's manual and it doesn't really get you the flag, more of like a possible combinations of flag.
Since I really enjoyed doing this, I might as well place this crazy kind of a solution here.

So, as I said earlier, if we looked at how the xorKey was being built and think some more, we would be able to then go asking for different `(i,j)`s variations, and therefore extending our "bit" knowledge of the flag. Well, that part is exatly were I messed up (ouch, so early in the game). I did saw that with `i: 1 & j: 2` the key was `1X`, but I stopped thinking there and went straightahead with that small piece of info.

Another thing that I knew was, from the flag sanitization, which characters were allowed in it; and that range always have the first bit in 1. So I split the "potential_flag" in bytes and checked the first bit. For those bytes that I didn't know the bit (`?`) I automatically placed a `1`

Basically, I ended up with a flag that had a little bit more than half the bits uncovered. Something that looked like:
```
potential_flag = '1100110110110011000011100111111101111?0?1?1?0?0?111?0?0?1?1?0?110?1?1?1?0?1?011?0?0?1?0?0?111?1?1?1?0?0?111?1?1?1?0?1?110?1?1?1?0?1?111?0?0?1?1?1?010?1?1?1?0?1?011?1?1?1?1?1?111?1?1?1?1?1?111?0?0?1?0?0?011?0?0?1?1?1?111?0?1?1?0?0?111?0?0?1?0?1?111?0?1?1?1?1?111?0?1?1?1?0?011?1?1?1?1?1?111?0?0?1111101'
```

Looking at the byte groups again, I noticed that at the very most, I was missing 3 bits per byte; and that, again, the byte needed to be under certain range and since it is a flag I could have a "filtered" list of possible chars. So, why not bruteforce it? hehe

For each byte, I run the 8 possible permutations of bits, and checked if the byte was in the possible character range and moreover if it was a letter or a number:

```
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
possible_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.,'
```

Once I finished that evaluation, I had in my possesion all the possible combinations of chars to build the flag.

I noticed the `_` (underscore) in just some of the positions, which is ideal because it's the char used as a space in flags, and from that I tested a couple of intervals.

Now, in order to test the possible intervals, the amount of combinations with the letters was gigantic; however, I did notice that there were no numbers present in the possible chars for any position. This was good, because it meant that words weren't going to be written like `th1s 1s 4 w0rd` but more like `this is a word`.

Doing a little bit of research, I found `enchant`, a python lib that can load dictionaries and which you can check if a word is indeed part of the dictionary.

So with these last two things in mind, I run the combinations, filtering only those which were valid english words. 

Because the list of words was pretty short, it left me with a human-eye possible puzzle to build potential phrases for the flag. This was the final puzzle table I got:

| [5:9] | [10:17] | [18:21] | [22:26] | [27:30] | [31:36] | [37:42] |
|-------|---------|---------|---------|---------|---------|---------|
| baas  | decking | eat     | down    | aha     | bates   | croup   |
| baps  | ducking | get     | noun    | the     | bides   | crowd   |
| bats  | fucking | gut     |         |         | biter   | group   |
| bias  | lacking | guv     |         |         | bites   | grout   |
| bids  | leaking | mat     |         |         | caper   | spout   |
| bits  | leaning | met     |         |         | capes   |         |
| cads  | lucking | oat     |         |         | capos   |         |
| caps  | necking | opt     |         |         | cater   |         |
| cats  |         | out     |         |         | ciaos   |         |
| city  |         |         |         |         | cider   |         |
| fads  |         |         |         |         | cites   |         |
| fats  |         |         |         |         | fades   |         |
| fits  |         |         |         |         | fates   |         |
| gads  |         |         |         |         | gapes   |         |
| gaps  |         |         |         |         | gates   |         |
| gits  |         |         |         |         | gator   |         |
| rads  |         |         |         |         | gites   |         |
| raps  |         |         |         |         | raper   |         |
| rats  |         |         |         |         | rapes   |         |
| rids  |         |         |         |         | rater   |         |
| rips  |         |         |         |         | rates   |         |
| saps  |         |         |         |         | rider   |         |
| sips  |         |         |         |         | rides   |         |
| sits  |         |         |         |         | riper   |         |
| vats  |         |         |         |         | rites   |         |
| vies  |         |         |         |         | sades   |         |
| wads  |         |         |         |         | sates   |         |
| wits  |         |         |         |         | scags   |         |
|       |         |         |         |         | scams   |         |
|       |         |         |         |         | scums   |         |
|       |         |         |         |         | sides   |         |
|       |         |         |         |         | sites   |         |
|       |         |         |         |         | vapes   |         |
|       |         |         |         |         | vapor   |         |
|       |         |         |         |         | viper   |         |
|       |         |         |         |         | wader   |         |
|       |         |         |         |         | wades   |         |
|       |         |         |         |         | water   |         |
|       |         |         |         |         | wider   |         |
|       |         |         |         |         | widow   |         |
|       |         |         |         |         | wiper   |         |
|       |         |         |         |         | wipes   |         |


Considering the challenge was about itsy-bitsy spider, I located a couple of words like `spout` `water` etc, which should have a very high success rate, and for the first word `bits` was there and I thought it was a shortname for our lovely spider.

I ended up building a funny flag, that was incorrect by 2 words:

```
flag{bits_fucking_get_down_the_water_spout}
```

And obviously, as I advanced with this logic I kept thinking "this probably isn't the way to solve it", because even when I reduced it to the last words, I still had to check combinations (because all the even positions could have the letter in minus. or mayus)

And that's when I decided to put a break on this and backtrack my mess up.

Anyway, it was fun :)
