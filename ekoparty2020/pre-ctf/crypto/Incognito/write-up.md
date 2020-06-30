## Flag
flag EKO{B91_just_another_encoder}

## Steps
checked file
```
$ file Incognito 
Incognito: gzip compressed data, was "Incognito", last modified: Fri Jun 26 18:00:51 2020, from Unix, original size modulo 2^32 825959
```

try to decompress using gzip
```
wololo@wololo:~/ctfs/prectf-eko2020$ gzip -d Incognito
gzip: Incognito: unknown suffix -- ignored
```

added .gz suffix and decompressed
```
wololo@wololo:~/ctfs/prectf-eko2020$ mv Incognito Incognito.gz
wololo@wololo:~/ctfs/prectf-eko2020$ gzip -d Incognito.gz 
```

new file Incognito is decompressed. type ASCII
```
wololo@wololo:~/ctfs/prectf-eko2020/crypto/Incognito$ file Incognito
Incognito: ASCII text
```

open file and see "gibberish"
```
vuk:eJs4+BAAN/<MCG4DC"hgBAi"WGEAAAl%W>,SAA:CL3OypB2evoWKAA5F,PPb%AXLwy[>KfBA
AAkA)5U.BA@wSA*hwz8M5wo_AAr([ZzDlHo&e>)B}q5Uo[,}/P6,M9A&.qQd{gN(271,O14pY,R!
iN!nRSSR%W`ppDqN>j.IfBsj`j4>x[DSf:"Zo%dC|Z4[2y"C:INv>j2w>Q8|sB_vYY73HO)skY+"
yW9R<y~~E/o[k>K|Odi8B%HP`36|2QLs~{Ch2.7o`r2.hU!;6zP]{zG3s@*NLUT]o2iO3bWo[zG3
s@=lZo&WLU|+wbWok:tY*cT3s@*NLU|+$;y@ptWo[zG3s@+6Axv5kU|+wbWo[zk9I,^"Wo[zG3s@
```

checked different encodings with the first sentence, until I arrived to base91
using [Base91 online tool](https://www.better-converter.com/Encoders-Decoders/Base91-Decode) we see some PNG text   
```
�PNG

���
IHDR��W�������л����sRGB�������gAMA�����a�
```

decoded the file in base91, wrote it to another file, and voila, new png image containing the flag
(see python code)