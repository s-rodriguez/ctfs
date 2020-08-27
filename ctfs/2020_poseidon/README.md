# Poseidon 2020

- [Poseidon 2020](#poseidon-2020)
- [Forensics](#forensics)
  - [Gallery](#gallery)

# Forensics

## Gallery

### Flag
```
```


### Analysis & Solution

Mount ewf image
https://www.andreafortuna.org/2018/04/11/how-to-mount-an-ewf-image-file-e01-on-linux/

There is a folder with the name `steghide` -> hint to use it

Steghide works on JPG files only, and from the images in the disk there are only 2 of them which correspond to that

On the recycle bin of the mounted image there is a text file containing 666 lines of "garbage" -> lines of 26 chars

Using a tool to perform bruteforce and steghide, and having the garbage file as input for the passwords we can extract the flag