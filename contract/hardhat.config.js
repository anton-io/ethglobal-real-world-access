require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.20", // Adjust to your contract's Solidity version
  networks: {
    hardhat: {
      accounts: [
        {  // Owner/Signer: 0x8163a3415402B498c7441D0D19DDe724E104Ab82
          privateKey: "0xa4cb42b54fa055392dafbda0f70f9e4d075b77eff4c988011341674740acd733",
          balance: "10000000000000000000000", // 10,000 ETH in wei
        },
        {  // User: 0x25a0fEC55dD7cc314A8Bb00e666489524b7d9cB9
          privateKey: "0xfa25c75192e85a56820acaf74a6157d2bb3a5df7ac23b7e025340f87b38d3def",
          balance: "10000000000000000000000", // 10,000 ETH in wei
        },
      ],
    },
  },
};