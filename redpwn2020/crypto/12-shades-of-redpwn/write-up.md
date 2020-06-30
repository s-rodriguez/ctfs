# 12 Shades of Redpwn

## Flag
flag{9u3ss0o9_1s_4n_4rt}

## Introduction
We are handed to image files:
- `chipertext.jpg`
- `color-wheel.jpg`

## Analysis done
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
