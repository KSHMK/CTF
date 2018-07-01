# SCTF 2018 : BankRobber

**Category:** Defense

**Difficulty:** Easy

**Points:** 103pts

**Description:** 



SCTFBank looks vulnerable...

Patch and protect it from Bankrobbers!



nc bankrobber.eatpwnnosleep.com 4567



SCTFBank.sol

## Write-up (KO)

이더리움 소스인 solidity소스이다. 취약점을 막는 문제였는데 [Ethereum Known Attacks](https://consensys.github.io/smart-contract-best-practices/known_attacks/) 사이트를 참고하여 패치를 하였더니 문제가 풀렸다.

ALPHA 공격은 레이스 컨디션 문제였을 것이다. 그래서 MUTEX를 추가하였고, BRAVO 공격은 Integer Overflow 문제였다. 그래서 require 추가를 통해 방어하였다.

### FLAG

SCTF{sorry_this_transaction_was_sent_by_my_cat}

