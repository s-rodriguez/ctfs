
/* WARNING: Function: __i686.get_pc_thunk.bx replaced with injection: get_pc_thunk_bx */

undefined4 main(void)

{
  char cVar1;
  uint uVar2;
  undefined4 uVar3;
  int in_GS_OFFSET;
  int local_98;
  char local_94 [128];
  int local_14;
  
  local_14 = *(int *)(in_GS_OFFSET + 0x14);
  srand((uint)main);
  fgets(local_94,0x80,stdin);
  local_98 = 0;
  while ((local_94[local_98] != '\0' && (local_94[local_98] != '\n'))) {
    cVar1 = local_94[local_98];
    uVar2 = rand();
    printf("%02x",(int)cVar1 ^ uVar2 & 0xff);
    local_98 = local_98 + 1;
  }
  putchar(10);
  uVar3 = 0;
  if (local_14 != *(int *)(in_GS_OFFSET + 0x14)) {
    uVar3 = __stack_chk_fail_local();
  }
  return uVar3;
}

