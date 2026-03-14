// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DonationVault {

    address public owner;
    uint public totalRaised;
    uint public donationCount;

    mapping(address => uint) public donorTotal;

    event DonationReceived(address donor, uint amount, uint timestamp);
    event WithdrawalExecuted(address owner, uint amount);

    constructor() {
        owner = msg.sender;
    }

    function donate() public payable {
        require(msg.value > 0, "Donation must be greater than zero");

        donorTotal[msg.sender] += msg.value;
        totalRaised += msg.value;
        donationCount += 1;

        emit DonationReceived(msg.sender, msg.value, block.timestamp);
    }

    function withdraw(uint amount) public {
        require(msg.sender == owner, "Only owner can withdraw");
        require(amount <= address(this).balance, "Insufficient balance");

        payable(owner).transfer(amount);

        emit WithdrawalExecuted(owner, amount);
    }

    function getContractBalance() public view returns (uint) {
        return address(this).balance;
    }
}
