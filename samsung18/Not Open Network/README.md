# SCTF 2018 : Not Open Network

**Category:** Defense

**Difficulty:** Medium

**Points:** 297pts

**Description:** 



You are the network admin of a black market service.

You want to setup a firewall to protect the servers from hackers and police.

Your servers use IPs in 10.0.0.0/16 range.



- Drop all incoming packets except the ones heading to port 80.

- Drop all packets containing string 'police', case insensitive.

- All other packets are sent to correct destinations.

You may assume that there will be TCP packets only.


## Write-up (KO)

ONOS app을 만들어서 80포트로 오는 패킷을 모두 드랍하고, 패킷 데이터 내부에 police라는 단어가 있으면 드랍하라는 문제이다.

이미 기본 템플릿에 3번째 조건인 정확한 주소로 보내는 조건은 구현되어 있으므로 1, 2번째 조건만 만족시키면 되었다.

아무런 예제가 없었기 때문에 [Source Code](https://github.com/opennetworkinglab/onos/tree/master/utils/misc/src/main/java/org/onlab/packet)와 [ONOS Java API docs](http://api.onosproject.org/1.5.1/overview-summary.html)를 보고 코딩을 하였다.

### FLAG

SCTF{The_B4sic_0f_SDN_4pp}

