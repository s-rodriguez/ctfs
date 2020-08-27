## Beginner

### Flag

```
CTF{S1MDf0rM3!}
```

### Analysis

We are provided with a small elf file
```
$ file a.out 
a.out: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=e3a5d8dc3eee0e960c602b9b2207150c91dc9dff, for GNU/Linux 3.2.0, not stripped
```

When we execute it we see that it asks for the flag, and when we place a test text it prints `FAILURE`

```
$ ./a.out 
Flag: test123
FAILURE
```

Time to reverse this!

We can do this using any tool, from gdb up to any graphic tool like Ghidra (after all, it's an easy level)

The main disassemble shows the following:

```
   0x0000000000001080 <+0>:     push   %r12
   0x0000000000001082 <+2>:     lea    0xf7b(%rip),%rdi        # 0x2004
   0x0000000000001089 <+9>:     xor    %eax,%eax
   0x000000000000108b <+11>:    push   %rbp
   0x000000000000108c <+12>:    sub    $0x28,%rsp
   0x0000000000001090 <+16>:    callq  0x1050 <printf@plt>
   0x0000000000001095 <+21>:    mov    %rsp,%r12
   0x0000000000001098 <+24>:    xor    %eax,%eax
   0x000000000000109a <+26>:    lea    0x10(%rsp),%rbp
   0x000000000000109f <+31>:    mov    %r12,%rsi
   0x00000000000010a2 <+34>:    lea    0xf62(%rip),%rdi        # 0x200b
   0x00000000000010a9 <+41>:    callq  0x1060 <__isoc99_scanf@plt>
   0x00000000000010ae <+46>:    movdqa (%rsp),%xmm0
   0x00000000000010b3 <+51>:    mov    %rbp,%rsi
   0x00000000000010b6 <+54>:    mov    %r12,%rdi
   0x00000000000010b9 <+57>:    mov    $0x10,%edx
   0x00000000000010be <+62>:    pshufb 0x2fa9(%rip),%xmm0        # 0x4070 <SHUFFLE>
   0x00000000000010c7 <+71>:    paddd  0x2f91(%rip),%xmm0        # 0x4060 <ADD32>
   0x00000000000010cf <+79>:    pxor   0x2f79(%rip),%xmm0        # 0x4050 <XOR>
   0x00000000000010d7 <+87>:    movaps %xmm0,0x10(%rsp)
   0x00000000000010dc <+92>:    callq  0x1030 <strncmp@plt>
   0x00000000000010e1 <+97>:    test   %eax,%eax
   0x00000000000010e3 <+99>:    jne    0x1100 <main+128>
   0x00000000000010e5 <+101>:   mov    0x2f94(%rip),%rsi        # 0x4080 <EXPECTED_PREFIX>
   0x00000000000010ec <+108>:   mov    $0x4,%edx
   0x00000000000010f1 <+113>:   mov    %rbp,%rdi
   0x00000000000010f4 <+116>:   callq  0x1030 <strncmp@plt>
   0x00000000000010f9 <+121>:   mov    %eax,%r12d
   0x00000000000010fc <+124>:   test   %eax,%eax
   0x00000000000010fe <+126>:   je     0x111d <main+157>
   0x0000000000001100 <+128>:   lea    0xf11(%rip),%rdi        # 0x2018
   0x0000000000001107 <+135>:   mov    $0x1,%r12d
   0x000000000000110d <+141>:   callq  0x1040 <puts@plt>
   0x0000000000001112 <+146>:   add    $0x28,%rsp
   0x0000000000001116 <+150>:   mov    %r12d,%eax
   0x0000000000001119 <+153>:   pop    %rbp
   0x000000000000111a <+154>:   pop    %r12
   0x000000000000111c <+156>:   retq   
   0x000000000000111d <+157>:   lea    0xeec(%rip),%rdi        # 0x2010
   0x0000000000001124 <+164>:   callq  0x1040 <puts@plt>
   0x0000000000001129 <+169>:   jmp    0x1112 <main+146>
```

Basically, the program is:

1. Asking for an input `<+41>:  callq  0x1060 <__isoc99_scanf@plt>`
2. It performs a shuffle of the input using PSHUFB `<+62>:  pshufb 0x2fa9(%rip),%xmm0  # 0x4070 <SHUFFLE>`. The mask for the operation is stored in `SHUFFLE`
3. It performs an addition to the result of the shuffle, using PADDD `<+71>:  paddd  0x2f91(%rip),%xmm0  # 0x4060 <ADD32>`. The value added is stored in `ADD32`
4. Finally, it will do an XOR operation `<+79>:  pxor   0x2f79(%rip),%xmm0  # 0x4050 <XOR>` (And it will use the value stored in `XOR`)