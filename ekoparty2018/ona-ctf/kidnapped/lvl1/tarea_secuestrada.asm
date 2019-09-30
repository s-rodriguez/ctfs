; nasm -f elf64 simd.asm; ld -o simd simd.o
section     .text
global      _start                              

_start:                                         

    movdqu  xmm1, [Parallel_processing]
    movdqu  xmm3, [is_much_faster...You_know?]
    movdqu  xmm5, [but_sometimes_is_difficult]
    movdqu  xmm7, [to_understand_how_it_works.]


    movdqu  xmm10, [Anyways_I_trust_you...]
    
    movdqu  xmm2, xmm1
    movdqu  xmm4, xmm3
    movdqu  xmm6, xmm5
    movdqu  xmm8, xmm7
    movdqu  xmm11, xmm10

    pxor xmm9, xmm9

    punpckhwd xmm1, xmm9   
    punpckhwd xmm2, xmm9   
    punpcklwd xmm3, xmm9   
    punpckhwd xmm4, xmm9   
    punpcklwd xmm5, xmm9   
    punpcklwd xmm6, xmm9   
    punpcklwd xmm7, xmm9   
    punpckhwd xmm8, xmm9
    punpcklwd xmm10, xmm9
    punpckhwd xmm9 ,xmm11


    psubw xmm1, xmm10
    psubw xmm2, xmm11
    psubw xmm3, xmm10
    psubw xmm4, xmm11
    psubw xmm5, xmm10
    psubw xmm6, xmm11
    psubw xmm7, xmm10
    psubw xmm8, xmm11

    packuswb xmm1, xmm2 
    packuswb xmm3, xmm4 
    packuswb xmm5, xmm6 
    packuswb xmm7, xmm8 


    movdqu [Parallel_processing], xmm1
    movdqu [is_much_faster...You_know?], xmm3
    movdqu [but_sometimes_is_difficult], xmm5
    movdqu [to_understand_how_it_works.], xmm7

    mov     ecx, Parallel_processing  
    mov     edx, 0x40
    mov     ebx,1                               
    mov     eax,4                               
    int     0x80                                

    mov     eax,1                               
    int     0x80                                


section     .data
Parallel_processing dq 0x7e7618131b332312, 0xb5db2d5e4333690e
is_much_faster...You_know? dq 0x487bdfe02d301eee, 0x9db0232038f9321e
but_sometimes_is_difficult dq 0x4a47dbdf5e07f2f5, 0x6caaef1f3ef1312f
to_understand_how_it_works. dq 0x5078dd0e61071ff0, 0x5a9adf0f28e0206b
Anyways_I_trust_you... dq 0x1715ABADFACEBABE
Whats_wrong_in_this_code? dq 0x3A7ABEEF08C0FFEE 

