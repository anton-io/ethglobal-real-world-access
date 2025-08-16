const hre = require("hardhat");

async function main() {
  const [owner, _] = await hre.ethers.getSigners();

  const MockPYUSD = await hre.ethers.getContractFactory("MockPYUSD");
  const PYUSD = await MockPYUSD.deploy(hre.ethers.parseUnits("1000000", 6));
  await PYUSD.waitForDeployment();

  const RWAcess = await hre.ethers.getContractFactory("RWAcess");
  const rwaccess = await RWAcess.deploy(
    await PYUSD.getAddress(),
    1000, // pricePerSecond = 0.001 PYUSD/sec
    "room.hotel.eth"
  );
  await rwaccess.waitForDeployment();

  console.log("PYUSD:", await PYUSD.getAddress());
  console.log("RWAcess:", await rwaccess.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});