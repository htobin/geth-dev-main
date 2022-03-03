// SPDX-License-Identifier: UNLICENSED
pragma solidity < 0.7.0;

contract Greeter{

    string private _greeting = "Hello, World!";

    function greet() external pure returns(string memory) {
        return "Hello, World!";
    }
}