# SCTF 2018 : Through The Router

**Category:** Attack
**Difficulty:** Easy
**Points:** 140pts
**Description:** 

You are an industrial spy hiding in the SCTF company.
You have found the secret recipe, but could not send any packet to your home.
That is because SCTF's corporate network is configured with SDN,
and that these rules are installed at all routers in the network.

Craft a packet that satisfies:

It is a UDP packet
It arrives at 10.0.0.1:22136.
Its body is a 6-byte string 'secret'.
Your packet will be sent using this python code:

```python
s = socket(AF_INET, SOCK_RAW, IPPROTO_UDP)
s.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)
s.sendto(packet, ('10.0.0.1', 0))
```
Therefore the packet must include IP and UDP headers.

## Write-up (KO)

해당 문제는 IP와 UDP 구조 프레임을 만들어서 rule의 필터링에 걸리지 않고 10.0.0.1:22136에 secret이라는 문자열을 보내는 문제이다.

rule을 살펴보면 Treatment Instructions에 immediate:NOACTION일 경우 해당 패킷은 블락되고 immediate:OUTPUT:FLOOD일 경우 정상적으로 패킷이 보내짐을 알 수 있다.

살펴봐야 할 점은 PRIORITY인데 이 값이 높을수록 우선적으로 필터 비교를 하게 된다.

가장 높은 0x780000523999fb는 UDP_DST가 1111일 경우가 포함되므로 사용할 수 없다.

다음 필터인 0x7800003a89fac6일 경우에는 우리가 사용할 수 있다. UDP이므로 IPV4_SRC와 UDP_SRC는 우리와 아무런 관계가 없다. 따라서

>IPV4_SRC : 10.1.7.2
>UDP_SRC : 5555
>IPV4_DST : 10.0.0.1
>UDP_DST : 22136
>PACKET HEX : 450000023CB04000401100000A0107080A00000115b35678000E3c51736563726574

물론 IP 헤더와 UDP 헤더의 Checksum 값을 정확하게 맞춰야 한다.

### FLAG

SCTF{Sp00f_7h3_p4ck3t_70_dr1ll_pr1v4t3_n37w0rk}

