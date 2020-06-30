check file
wololo@wololo:~/ctfs/prectf-eko2020$ file forensics/2much/2Much.bk 
forensics/2much/2Much.bk: gzip compressed data, was "for0.img", last modified: Thu Jun 25 02:45:23 2020, from Unix, original size modulo 2^32 20971520

binwalk or decompress img
wololo@wololo:~/ctfs/prectf-eko2020$ file forensics/2much/_2Much.bk.extracted/for0.img
forensics/2much/_2Much.bk.extracted/for0.img: SGI XFS filesystem data (blksz 4096, inosz 256, v2 dirs)


mount img
sudo mount _2Much.bk.extracted/for0.img data/

list of data.x files (999)
wololo@wololo:~/ctfs/prectf-eko2020$ ll forensics/2much/data/
total 4000
-rw-r--r-- 1 root root 16 Aug  1  2016 data.1
-rw-r--r-- 1 root root 16 Aug  1  2016 data.10
-rw-r--r-- 1 root root 16 Aug  1  2016 data.100
-rw-r--r-- 1 root root 16 Aug  1  2016 data.1000
-rw-r--r-- 1 root root 16 Aug  1  2016 data.101

check content of files
wololo@wololo:~/ctfs/prectf-eko2020$ cat forensics/2much/data/data.1
ZH8Em5WVmpYfl53B



run bulk_extractor to get info

```
bulk_extractor for0.img -o bulk_info
```
nothing useful


run photorec on for0.img
```
photorec for0.img
```

it places 67 .xfs files on the `recup_dir.1`
```
wololo@wololo:~/ctfs/eko2020/pre-ctf/forensics/2much/recup_dir.1$ ll
total 288
-rw-r--r-- 1 wololo wololo  4096 Jun 28 19:20 f0000000.xfs
-rw-r--r-- 1 wololo wololo  4096 Jun 28 19:20 f0000008.xfs
-rw-r--r-- 1 wololo wololo  4096 Jun 28 19:20 f0000016.xfs
-rw-r--r-- 1 wololo wololo  4096 Jun 28 19:20 f0009664.xfs
-rw-r--r-- 1 wololo wololo  4096 Jun 28 19:20 f0009672.xfs
-rw-r--r-- 1 wololo wololo  4096 Jun 28 19:20 f0009680.xfs
```

looking at the file type of each one of them:
```
f0000000.xfs: SGI XFS filesystem data (blksz 4096, inosz 256, v2 dirs)
f0000008.xfs: data
f0000016.xfs: data
f0009664.xfs: data
f0009672.xfs: dBase III DBT, version number 0, next free block index 2759937609, 1st item "IN\201\244\002\002"
f0009680.xfs: dBase III DBT, version number 0, next free block index 2759937609, 1st item "IN\201\244\002\002"
f0009688.xfs: dBase III DBT, version number 0, next free block index 2759937609, 1st item "IN\201\244\002\002"
```

first file looks like the header of the FS
followed by 3 data files
followed by the rest of the files which all give a `dBase III DBT`... is it possible that this is a DB?