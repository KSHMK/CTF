# SCTF 2018 : CowBoy

**Category:** Attack

**Difficulty:** Easy

**Points:** 109pts

**Description:** 



I made a new heap allocator.

Would you test this one?



nc cowboy.eatpwnnosleep.com 14697



CowBoy, CowBoy_libc

## Write-up (KO)

문제에서 Alloc을 하게 되면 16byte 메모리를 할당받는다. 

이를 이용해 BIN Chunk를 만드는데 앞 8byte는 내용 저장 mmap 주소가 저장되고 다음 8byte는 다음 Chunk를 가리킨다. 

문제를 실행하던 도중 2개의 BIN Chunk가 서로를 가리키는 버그를 발견했다. 

이를 이용하여 2번째 청크를 Free 하면 FillData에서 데이터 입력을 받기 위해 malloc을 하면서 2번째 Chunk의 주소에다 할당받게 되고 이를 이용해 LIBC leak과 GOT overriding을 수행하였다.

### FLAG

SCTF{H4v3_y0u_ev3r_seen_CowBoy_B1B0P?}

