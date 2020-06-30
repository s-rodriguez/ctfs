# Ugly Bash

## Flag
flag{us3_zsh,_dummy}

## Introduction
We are given a `.sh` script and the hint:

```
This bash script evaluates to echo dont just run it, dummy # flag{...} where the flag is in the comments.
```

## Solution
If we open the script, it's basically obfuscated code, so it'll be impossible to simply find the flag.

However, we can run the script in `DEBUG` mode with `-x` and it will print every line evaluation, along with the flag!

```
bash -x ugly-bash.sh
```

```
flag{us3_zsh,_dummy}
```