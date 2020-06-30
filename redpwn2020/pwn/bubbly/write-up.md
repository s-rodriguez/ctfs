# Bubbly

## Flag

## Introduction
We are provided with an ELF file

```
$ file bubbly
bubbly: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked
```

And connecting to the specified remote prints:
```
$ nc 2020.redpwnc.tf 31039
I hate my data structures class! Why can't I just sort by hand?
```

## Solution
Time to understand what that bubbly file is doing.

After opening it with Ghidra, we can check the dissasembly code provided, in particular for the main function:

```c
int main(void)
{
  uint32_t i;
  int unused;
  _Bool pass;
  
  setbuf(stdout,(char *)0x0);
  setbuf(stdin,(char *)0x0);
  setbuf(stderr,(char *)0x0);
  puts("I hate my data structures class! Why can\'t I just sort by hand?");
  pass = false;
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
