pragma solidity ^0.4.11;

/// @title Contract to bet Ether for a number and win randomly when the number of bets is met.
contract Casino {

   // The number that won the last game
   uint private seed;
   uint constant MAX_NUM = 30;
   uint winningNumber;
   uint data;

   function Casino() public {
      seed = block.timestamp;
   }

   function placeBet() public {
      winningNumber = generateNumberWinner();
   }

   function generateNumberWinner() private constant returns (uint) {
      uint numberWinner = (block.number + seed) % MAX_NUM + 1; // This isn't secure
      return numberWinner;
   }

   function getWinningNumber() public constant returns (uint) {
     return winningNumber;
   }

   function spam() public {
     data += 1;
   }
}
