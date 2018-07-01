# SCTF 2018 : HideInSSL

**Category:** Coding
**Difficulty:** Easy
**Points:** 121pts
**Description:** 

Hacker stole the flag through the SSL protocol.

HideInSSL.zip

## Write-up (KO)

HideInSSL.pcap이라는 파일을 준다. 이 파일을 보면 Client Hello와 Continuation Data이라는 TLS 패킷이 많다.

그래서 살펴보던 도중 No.33 패킷에서 TLS Handshake protocol 헤더 안 Random Bytes에 JFIF이 있는 것을 보고 python의 DPKT 모듈을 사용하여 뽑아내었다.

하지만 파일이 깨졌었는데 hex editer로 보니 파일이 깨져있거나 중복되는 문자열이 보였다. 그래서 다시 보니 Continuation Data에 "1", "0"이라는 응답이 있었다. "1"이 정상 수신, "0"은 수신 실패라는 의미였고 이를 이용하여 다시 뽑으니 정상적으로 파일이 나왔다.

### FLAG

SCTF{H3llo_Cov3rt_S5L}

