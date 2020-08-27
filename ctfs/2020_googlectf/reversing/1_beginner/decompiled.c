
ulong main(void)

{
  int iVar1;
  uint uVar2;
  undefined auVar3 [16];
  undefined local_38 [16];
  undefined4 local_28;
  undefined4 uStack36;
  undefined4 uStack32;
  undefined4 uStack28;
  
  printf("Flag: ");
  __isoc99_scanf(&DAT_0010200b,local_38);
  auVar3 = pshufb(local_38,SHUFFLE);
  auVar3 = CONCAT412(SUB164(auVar3 >> 0x60,0) + ADD32._12_4_,
                     CONCAT48(SUB164(auVar3 >> 0x40,0) + ADD32._8_4_,
                              CONCAT44(SUB164(auVar3 >> 0x20,0) + ADD32._4_4_,
                                       SUB164(auVar3,0) + ADD32._0_4_))) ^ XOR;
  local_28 = SUB164(auVar3,0);
  uStack36 = SUB164(auVar3 >> 0x20,0);
  uStack32 = SUB164(XOR >> 0x40,0);
  uStack28 = SUB164(XOR >> 0x60,0);
  iVar1 = strncmp(local_38,(char *)&local_28,0x10);
  if (iVar1 == 0) {
    uVar2 = strncmp((char *)&local_28,EXPECTED_PREFIX,4);
    if (uVar2 == 0) {
      puts("SUCCESS");
      goto LAB_00101112;
    }
  }
  uVar2 = 1;
  puts("FAILURE");
LAB_00101112:
  return (ulong)uVar2;
}



SHUFFLE[16]
[0] -  02
[1] -  06
[2] -  07
[3] -  01
[4] -  05
[5] -  0b
[6] -  09
[7] -  0e
[8] -  03
[9] -  0f
[10] - 04
[11] - 08
[12] - 0a
[13] - 0c
[14] - 0d
[15] - 00


ADD32[16]
[0]  - ef
[1]  - be
[2]  - ad
[3]  - de
[4]  - ad
[5]  - de
[6]  - e1
[7]  - fe
[8]  - 37
[9]  - 13
[10] - 37
[11] - 13
[12] - 66
[13] - 74
[14] - 63
[15] - 67


-----

PSHUFB — Packed Shuffle Bytes


ulong main(void)

{
  int iVar1;
  uint uVar2;

  undefined input [16];
  undefined auxVariable [16];
  undefined4 result;

  SHUFFLE = [0x02,0x06,0x07,0x01,0x05,0x0b,0x09,0x0e,0x03,0x0f,0x04,0x08,0x0a,0x0c,0x0d,0x00]
  ADD32 = [0xef,0xbe,0xad,0xde,0xad,0xde,0xe1,0xfe,0x37,0x13,0x37,0x13,0x66,0x74,0x63,0x67]
  XOR = [0x76,0x58,0xb4,0x49,0x8d,0x1a,0x5f,0x38,0xd4,0x23,0xf8,0x34,0xeb,0x86,0xf9,0xaa]
  EXPECTED_PREFIX = 'CTF{'

  
  // ------------------

  printf("Flag: ");
  input = scanf();

  auxVariable = pshufb(input, SHUFFLE);
  auxVariable += ADD32
  auxVariable = auxVariable ^ XOR

  result = auxVariable

  iVar1 = strncmp(input, result, 16); //Compare first 16 (0x10) characters
  if (iVar1 == 0) {
    uVar2 = strncmp(result, EXPECTED_PREFIX, 4); // Compare first 4 chars
    if (uVar2 == 0) {
      puts("SUCCESS");
      goto LAB_00101112;
    }
  }
  uVar2 = 1;
  puts("FAILURE");
LAB_00101112:
  return (ulong)uVar2;
}

