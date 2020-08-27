# EkoParty 2020 - PreCTF Write Ups

# Table of Contents
- [EkoParty 2020 - PreCTF Write Ups](#ekoparty-2020---prectf-write-ups)
- [Table of Contents](#table-of-contents)
- [crypto](#crypto)
  - [Incognito](#incognito)
  - [Esrom](#esrom)
  - [!OK](#ok)
- [forensics](#forensics)
  - [2Much](#2much)
  - [Logs](#logs)
  - [Meta](#meta)
  - [R-Bomb](#r-bomb)
- [misc](#misc)
  - [Welcome](#welcome)
  - [Anon](#anon)
  - [Deep](#deep)


# crypto

## Incognito

### Flag
flag EKO{B91_just_another_encoder}

### Analysis & Solution
We check the given file [Incognito](./crypto/Incognito/Incognito)
```
$ file Incognito 
Incognito: gzip compressed data, was "Incognito", last modified: Fri Jun 26 18:00:51 2020, from Unix, original size modulo 2^32 825959
```

Try to decompress using gzip
```
wololo@wololo:~/ctfs/prectf-eko2020$ gzip -d Incognito
gzip: Incognito: unknown suffix -- ignored
```

Added .gz suffix and decompressed
```
wololo@wololo:~/ctfs/prectf-eko2020$ mv Incognito Incognito.gz
wololo@wololo:~/ctfs/prectf-eko2020$ gzip -d Incognito.gz 
```

New file Incognito is decompressed. Checking for the type gives: ASCII
```
wololo@wololo:~/ctfs/prectf-eko2020/crypto/Incognito$ file Incognito
Incognito: ASCII text
```

When opening file at first we see "gibberish"
```
vuk:eJs4+BAAN/<MCG4DC"hgBAi"WGEAAAl%W>,SAA:CL3OypB2evoWKAA5F,PPb%AXLwy[>KfBA
AAkA)5U.BA@wSA*hwz8M5wo_AAr([ZzDlHo&e>)B}q5Uo[,}/P6,M9A&.qQd{gN(271,O14pY,R!
iN!nRSSR%W`ppDqN>j.IfBsj`j4>x[DSf:"Zo%dC|Z4[2y"C:INv>j2w>Q8|sB_vYY73HO)skY+"
yW9R<y~~E/o[k>K|Odi8B%HP`36|2QLs~{Ch2.7o`r2.hU!;6zP]{zG3s@*NLUT]o2iO3bWo[zG3
s@=lZo&WLU|+wbWok:tY*cT3s@*NLU|+$;y@ptWo[zG3s@+6Axv5kU|+wbWo[zk9I,^"Wo[zG3s@
```

The content of the file probably is encoded. So I checked different encodings with the first sentence, until I arrived to base91
using [Base91 online tool](https://www.better-converter.com/Encoders-Decoders/Base91-Decode) we see some PNG text   
```
�PNG

���
IHDR��W�������л����sRGB�������gAMA�����a�
```

We [decode the file](crypto/Incognito/test.py) in base91, wrote it to another file, and voila, new png image containing the flag

## Esrom

### Flag

```
EKO{morsemorse}
```

### Analysis & Solution

We are given the following encoded text:

```
. ---- -- --- / -- --- / . ---- - / --.- -.-- -. ..- / .-.. ... --. / -. -.- - / -.-- ... ... .-. -- .- ..- / --.- ... -.- ...--- / .. ... -.- --- - .. ... -.- --- - 
```

So this is basically morse code. The only difference is that short and long chars are encoded somewhat different as usual

Luckily we can use this [online tool](https://www.dcode.fr/morse-code) that we'll try different combinations and print possible results:
```
(.- )⇔ (-. )	THIS IS THE FLAG YOU ARE LOOKING FOR: MORSEMORSE
(. -)⇔ (-. )	NEEE EEE REE ETETEYE A�N ENTEE ET�NAWE ET�TJE �TEE�TEEE
( .-)⇔ (-. )	ATTT TTT KTT TETETLT N�A TAETT TE�ANDT TE=EBT �ETT�ETTT
( -.)⇔ (-. )	� � T� DRFTA TETDT NN� NUTTEXAA DANAV TTN�TN�
(-. )⇔ (-. )	E�MO MO E�T QYNU LSG NKT YSSRMAU QSK� ISKOTISKOT
(- .)⇔ (-. )	� � E� WKQEN ETEWE AAC AGEETPNN WNAN� EEA�EA�
```

First line has the flag that we need to submit in lowercase
```
MORSEMORSE
```

## !OK

### Flag

```
EKO{NOT_OK!}
```

### Analysis & Solution
We are given [some kind of encoding](./crypto/ok/not_ok) that looks like:

```
Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook.
Ook. Ook! Ook? Ook! Ook! Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook.
...
```

With a simple google we'll find that this is an [esoteric language](https://esolangs.org/wiki/Ook!) similar to brainfuck

We then look if there is an online translator, and we found the [same tool](https://www.dcode.fr/ook-language) as for Esrom

Translating the decoded message gives us the flag:

```
EKO{NOT_OK!}
```

# forensics

## 2Much

### Flag
```
EKO{Do_you_check_extended_attributes?}
```

### Solution
We obtain a zipped image

```
$ file 2Much 
2Much: gzip compressed data, was "for0.img", last modified: Thu Jun 25 02:45:23 2020, from Unix, original size modulo 2^32 20971520
```

We extract it and mount it to the `data` folder

```
$ mv 2Much 2Much.gz
$ gunzip 2Much.gz 
$ mkdir data
$ file 2Much
2Much: SGI XFS filesystem data (blksz 4096, inosz 256, v2 dirs)
$ sudo mount 2Much data/
```

Checking for the extended attributes returns a Base64 string:

```
$ sudo getfattr -d -R --only-values data/
RUtPe0RvX3lvdV9jaGVja19leHRlbmRlZF9hdHRyaWJ1dGVzP30=
```

Decoding it will give us the flag

```
$ echo -n "RUtPe0RvX3lvdV9jaGVja19leHRlbmRlZF9hdHRyaWJ1dGVzP30=" | base64 -d
EKO{Do_you_check_extended_attributes?}
```

## Logs

### Flag

```
EKO{207.136.9.198}
```

### Solution
We are given a file containing logs, and the flag is the first IP that appears trying to exploit a vuln found by Roberto Paleari

If we look through the advisories reported by Roberto, we'll eventually find one related to `Unauthenticated command execution on Netgear DGN devices`

- [Advisory](http://roberto.greyhats.it/advisories/20130603-netgear-dgn.txt)
- [Exploit](https://packetstormsecurity.com/files/144725/Netgear-DGN1000-Setup.cgi-Remote-Command-Execution.html)

Looking through the logs, we find the exploit attempt:

```
207.136.9.198 - - [02/Aug/2020:15:38:47 -0300] "GET /setup.cgi?next_file=netgear.cfg&todo=syscmd&cmd=busybox&curpath=/&currentsetting.htm=1 HTTP/1.1" 400 0 "-" "Mozilla/5.0"
```

So the IP for the flag is `207.136.9.198`

## Meta

### Flag
```
EKO{C4nt_t0uch_th1s}
```

### Solution
Decompress [Meta file](./forensics/meta/Meta) with 7z

```
$ 7z e Meta

7-Zip [64] 16.02 : Copyright (c) 1999-2016 Igor Pavlov : 2016-05-21
p7zip Version 16.02 (locale=en_US.utf8,Utf16=on,HugeFiles=on,64 bits,1 CPU Intel(R) Core(TM) m3-6Y30 CPU @ 0.90GHz (406E3),ASM,AES-NI)

Scanning the drive for archives:
1 file, 525142 bytes (513 KiB)

Extracting archive: Meta
--
Path = Meta
Type = 7z
Physical Size = 525142
Headers Size = 130
Method = LZMA2:768k
Solid = -
Blocks = 1

Everything is Ok

Size:       525153
Compressed: 525142
```

Examine [.jpg](./forensics/meta/ekoctf.jpg) file extracted with `exiftool`. Flag is in metadata

```
$ exiftool ekoctf.jpg 
ExifTool Version Number         : 12.00
File Name                       : ekoctf.jpg
Directory                       : .
File Size                       : 513 kB
File Modification Date/Time     : 2020:07:03 14:30:20-07:00
File Access Date/Time           : 2020:07:04 08:01:21-07:00
File Inode Change Date/Time     : 2020:07:04 08:01:21-07:00
File Permissions                : rw-r--r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Resolution Unit                 : None
X Resolution                    : 1
Y Resolution                    : 1
Comment                         : EKO{C4nt_t0uch_th1s}
Image Width                     : 2592
Image Height                    : 1728
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 2592x1728
Megapixels                      : 4.5
```

## R-Bomb

### Flag

```
EKO{RarrrRRrr!}
```

### Analysis & Solution

We are given a file named [R-Bomb](./forensics/r-bomb/R-Bomb) and the following hint:

```
This is a corrupted bomb file, be careful or the disk will fill up! 
```

When inspecting the file we see:

```
$ file R-Bomb 
R-Bomb: data
```

When opening it with bless or xxd, we can observe the following:

1) On the first bytes we can see there is a `flag.txt` being printed
```
00000000: 1a07 0100 c9bd e4fa 1001 050c 000b 0101  ................
00000010: bbd2 8580 8080 8080 0048 3570 ec2f 0203  .........H5p./..
00000020: 0bf2 d185 8080 8000 04b0 9c91 b486 8000  ................
00000030: a010 2ddc 823a 8043 0008 666c 6167 2e74  ..-..:.C..flag.t
00000040: 7874 0a03 029e e4d4 b77c 51d6 0189 be63  xt.......|Q....c
00000050: 0e33 5504 02f8 324b 0983 2302 4e41 885e  .3U...2K..#.NA.^
00000060: d483 e2ff 013f ec2e 157b 53f7 cfaf 7f79  .....?...{S....y
00000070: f3bd ef39 fde3 f5ff c000 0000 6f42 ffe0  ...9........oB..
```

2) After that there is a block of gibberish being repeated

```
00000080: 0000 0037 bf7f f000 0000 1bdf bff8 0000  ...7............
00000090: 000d efdf fc00 0000 06f7 effe 0000 0003  ................
000000a0: 7bf7 ff00 0000 01bd fbff 8000 0000 defd  {...............
000000b0: ffc0 0000 006f 7eff e000 0000 37bf 7ff0  .....o~.....7...
```

3) And another bigger block of gibberish being repeated

```
00000eb0: ff80 0000 89d1 0c0e 023f d317 f6cb 11eb  .........?......
...
00001ca0: 0000 bdff ff80 0000 00bd ffff 8000 0000  ................
00001cb0: bdff ff80 0000 00bd ffff 8000 0000 bdff  ................
00001cc0: ff80 0000 89d1 0c0e 023f d317 f6cb 11eb  .........?......
```

4) The file then ends with another `flag.txt` printed

```
00016900: fc00 0000 05ef fffc 26ef ffc2 6eff fc26  ........&...n..&
00016910: efff c26e fffc 26ef ffc2 6eff fc26 efff  ...n..&...n..&..
00016920: c26e fffc 26ef ffc2 6eff fc26 efff c26e  .n..&...n..&...n
00016930: fffc 26ef ffc2 6eff fc26 efff c26e 80c3  ..&...n..&...n..
00016940: 80aa a30e 0306 be00 00be 0000 8000 0002  ................
00016950: 514f e6b0 9e0b 3900 a6d2 0534 4835 70ec  QO....9....4H5p.
00016960: 2f02 030b f2d1 8580 8080 0004 b09c 91b4  /...............
00016970: 8680 00a0 102d dc82 3a80 4300 0866 6c61  .....-..:.C..fla
00016980: 672e 7478 740a 0302 9ee4 d4b7 7c51 d601  g.txt.......|Q..
00016990: 1d77 5651 0305 0400                      .wVQ....
```

Looking once again at the keywords of the hint, we could assume that this challenge could be a zip-bomb, but instead of a zip it's a rar (`R-Bomb`) that has corrupted headers.
- `corrupted`
- `bomb`
- `disk will fill up`

So we run the `rar` tool to fix it:

```
$ rar r R-Bomb

RAR 5.50   Copyright (c) 1993-2017 Alexander Roshal   11 Aug 2017
Trial version             Type 'rar -?' for help

Building fixed.R-Bomb
Scanning...
Unexpected end of archive 100%
Data recovery record not found
Scanning...
Unexpected end of archive
Corrupt header is found
Data recovery record not found
Reconstructing R-Bomb
Building rebuilt.R-Bomb
Found  flag.txt
Done
```

We see that in fact it was a RAR file, and it has a `flag.txt`!!. Before extracting it, we check the content:

```
$ rar l rebuilt.R-Bomb 

RAR 5.50   Copyright (c) 1993-2017 Alexander Roshal   11 Aug 2017
Trial version             Type 'rar -?' for help

Archive: rebuilt.R-Bomb
Details: RAR 5

 Attributes      Size     Date    Time   Name
----------- ---------  ---------- -----  ----
    .CA.... 1719946800  2020-07-03 13:58  flag.txt
----------- ---------  ---------- -----  ----
           1719946800                    1

```

So, there is only one file inside the RAR and pretty big ().
Instead of extracting the file, we can use the `i[par]=<str>` command for `rar` that looks for a string within the files. 
Considering the flag is built with the prefix `EKO` we look for that:

```
 rar i[par]=EKO rebuilt.R-Bomb 

RAR 5.50   Copyright (c) 1993-2017 Alexander Roshal   11 Aug 2017
Trial version             Type 'rar -?' for help

Found  rebuilt.R-Bomb / flag.txt
  EKO{RarrrRRrr!}EKO{RarrrRRrr!}EKO{RarrrRRrr!}EKO{RarrrRRrr!}EKO{Rarrr^C
User break

Program aborted
```

And there we have it. Flag being repeated, probably for the whole content of the `flag.txt` file.

# misc

## Welcome

### Flag
```
EKO{Hi_HTML_H4X0r}
```

### Analysis & Solution
This was a simple challenge to warm-up.

When clicking on the challenge and inspecting the request that is made, the response payload contains the flag:

```          
<p>
    Welcome to EKOPARTY PRECTF 2020! <span class="d-none">EKO{Hi_HTML_H4X0r}</span>
</p>
          
```

## Anon

### Flag

```
EKO{pastepastepaste...paste...sux}
```

### Analysis & Solution
A [link](http://paste.ubuntu.com/p/HnGHwGk4rQ/) is given to us. When opening it, we see that it is a Pastebin containing 5 urls.

```
1- http://paste.ubuntu.com/p/DO8r2xL0oD/
2- http://paste.ubuntu.com/p/KzO5PgXYsE/
3- http://paste.ubuntu.com/p/KpD0XPSZ0s/
4- http://paste.ubuntu.com/p/Qlw5i4zaJd/
5- http://paste.ubuntu.com/p/P5dtwM9vZT/
```

When entering to those links, some do not work (404 status code) and some do.
For those that work, we see again a Pastebin containing 5 new urls in each.

I decided to build a [small script](./solve.py) that goes looking at each working url, and following the urls that the response gives. It will basically be a tree traversal


root_url
    |_url_1
        |_url_1.1
            |_url_1.1.1
            |_url_1.1.2
            |_url_1.1.3
            |_url_1.1.4
            |_url_1.1.5
        |_url_1.2
        |_url_1.3
        |_url_1.4
        |_url_1.5
    |_url_2
        |_url_2.1
        |_url_2.2
        |_url_2.3
        |_url_2.4
        |_url_2.5
    ...

I supposed that eventually we would reach to a page containing the flag... And that's exactly what happens

Eventually we make a request to http://paste.ubuntu.com/p/j7XwD37y8H/ which contents doesn't have 5 urls but:

```
1- http://paste.ubuntu.com/p/p804DB7ddO/
2- http://paste.ubuntu.com/p/ifWqPPi1X3/
3- http://paste.ubuntu.com/p/jdLgsdjsmg/
4- http://paste.ubuntu.com/p/PXkacdF2Bc/
5- UlV0UGUzQmhjM1JsY0dGemRHVndZWE4wWlM0dUxuQmhjM1JsTGk0dWMzVjRmUT09Cg==
```

That 5th item looks like b64. We decode it and we obtain...

```
RUtPe3Bhc3RlcGFzdGVwYXN0ZS4uLnBhc3RlLi4uc3V4fQ==
```

Another b64... Ok. One more time and...
```
EKO{pastepastepaste...paste...sux}
```

Flag found!

### Recursion vs Loop
I initially tried doing this recursively, so basically a DFS (Depth-first-search) algorithm, since I imagined that the flag would be far from the first nodes.
This took approximately 2:35 mins

I did the BFS (Breadth-first-search) algorithm just for fun and to check if my initial theory was correct or not, and as expected the approximate time it takes to find the flag is 4:15 mins


## Deep

### Flag

```
EKO{H1DD3N^2}
```

### Analysis & Solution

First image named [Deep](./misc/deep/Deep) contained the following binary in it:

```
01001000
01101001
01011111
01000010
01100001
01100010
01111001
```

that translated into: `Hi_Baby`

Using steghide over the given image, without passphrase, recovers a file [flag.enc](./misc/deep/flag.enc):

```
root@f56e903fb2de:/data/pepe# steghide extract -sf Deep
Enter passphrase:
wrote extracted data to "flag.enc".
```

Looking at the content of the extracted file, we see base64 encoding:

```
root@f56e903fb2de:/data/pepe# head flag.enc
/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcG
BwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwM
DAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCADTAPcDASIA
AhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQA
AAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3
ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWm
p6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEA
AwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSEx
BhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElK
U1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3
```

We decode flag.enc into [flag.dec](./misc/deep/flag.dec) and, checking the file type, we see that the file is another image

```
root@f56e903fb2de:/data/pepe# base64 -d flag.enc > flag.dec
root@f56e903fb2de:/data/pepe# file flag.dec
flag.dec: JPEG image data, JFIF standard 1.01, resolution (DPI), density 96x96, segment length 16, baseline, precision 8, 247x211, frames 3
```

We try to use steghide once again, but it seems this needs a passphrase to extract the content:
```
root@f56e903fb2de:/data/pepe# steghide extract -sf flag.dec
Enter passphrase:
steghide: could not extract any data with that passphrase!
```

The passphrase is probably what was in binary in the first image, so we try again:
```
root@f56e903fb2de:/data/pepe# steghide extract -sf flag.dec -p Hi_Baby
wrote extracted data to "flag.txt
```

And we get a [flag.txt](./misc/deep/flag.txt) file containing the flag inside:

```
root@f56e903fb2de:/data/pepe# cat flag.txt
EKO{H1DD3N^2}
```
