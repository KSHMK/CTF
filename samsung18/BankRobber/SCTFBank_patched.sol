pragma solidity ^0.4.18;

contract SCTFBank{
    event LogBalance(address addr, uint256 value);
    mapping (address => uint256) private balance;
    uint256 private donation_deposit;
    address private owner;
    bool private lockBalances;

    //constructor
    constructor() public{
        owner = msg.sender;
    }
    
    //logging balance of requested address
    function showBalance(address addr) public {
        emit LogBalance(addr, balance[addr]);
    }

    //withdraw my balance
    function withdraw(uint256 value) public{
        require(!lockBalances && balance[msg.sender] >= value);
        lockBalances = true;
        balance[msg.sender] -= value;
        require(msg.sender.send(value));
        lockBalances = false;
    }
    
    //transfer my balance to other
    function transfer(address to, uint256 value) public {
        require(!lockBalances && balance[msg.sender] >= value && balance[to] + value >= balance[to]);
        lockBalances = true;
        balance[msg.sender] -= value;
        balance[to]+=value;
        lockBalances = false;
    }

    //transfer my balance to others
    function multiTransfer(address[] to_list, uint256 value) public {
        require(!lockBalances && balance[msg.sender] >= value*to_list.length && value > 0 &&  value*to_list.length > 0);
        lockBalances = true;
        balance[msg.sender] -= value*to_list.length;
        for(uint i=0; i < to_list.length; i++){
            require(balance[to_list[i]] + value >= balance[to_list[i]]);
            balance[to_list[i]] += value;
        }
        lockBalances = false;
    }
    
    //donate my balance
    function donate(uint256 value) public {
    	require(!lockBalances && balance[msg.sender] >= value && donation_deposit + value >= donation_deposit );
        lockBalances = true;
        balance[msg.sender] -= value;
        donation_deposit += value;
        lockBalances = false;
    }

    //Only bank owner can deliver donations to anywhere he want.
    function deliver(address to) public {
        require(!lockBalances && msg.sender == owner);
        lockBalances = true;
        to.transfer(donation_deposit);
        donation_deposit = 0;
        lockBalances = false;
    }
    
    //balance deposit, simple fallback function
    function () payable public {
        require(!lockBalances);
        lockBalances = true;
        balance[msg.sender]+=msg.value;
        lockBalances = false;
    }
}
//END

