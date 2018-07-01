# SCTF 2018 : dingJMax

**Category:** Reversing
**Difficulty:** Easy
**Points:** 106pts
**Description:** 

I prepared the Rhythm game "dingJMax" for you.
This is really hard... Can you get prefect score for flag?

dingJMax

## Write-up (KO)

DJMax 리듬게임이라는 컨셉을 맞춘 문제이다.

모든 노드를 PERFECT로 맞춰야 플레그를 준다.

그래서 바이너리 안의 노드 정보를 긁어 오고 PERFECT가 나오는 프레임을 찾았다.

바이너리는 20 Frame 주기를 가졌고, 문자열 연산 루틴을 그냥 복사하여 사용하였다.

### FLAG

SCTF{I_w0u1d_l1k3_70_d3v3l0p_GUI_v3rs10n_n3x7_t1m3}

