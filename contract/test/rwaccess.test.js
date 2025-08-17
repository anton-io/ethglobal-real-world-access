const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("RWAccess", function () {
  let rwaccess;
  let owner, user;

  // Define the private keys (TODO: use env variable).
  const keyOwner = "0xa4cb42b54fa055392dafbda0f70f9e4d075b77eff4c988011341674740acd733";
  const keyUser  = "0xfa25c75192e85a56820acaf74a6157d2bb3a5df7ac23b7e025340f87b38d3def";

  beforeEach(async function () {
    // Create wallet instances from private keys, connected to Hardhat's provider.
    owner = new ethers.Wallet(keyOwner, ethers.provider);
    user = new ethers.Wallet(keyUser, ethers.provider);

    // Use the signers (owner and user) as needed.
    console.log("Owner address:", owner.address);
    console.log("User address:", user.address);

    // Deploy mock PYUSD.
    console.log("Deploying MockUSD");
    const MockPYUSD = await ethers.getContractFactory("MockPYUSD", owner);
    pyusd = await MockPYUSD.deploy(ethers.parseUnits("1000000", 6)); // 1M mPYUSD to deployer.
    await pyusd.waitForDeployment();
    console.log("Deployed MockUSD at", await pyusd.getAddress());


    // Deploy RWAccess.
    console.log("Deploying RWAccess contract.");
    const RWAccess = await ethers.getContractFactory("RWAccess", owner);
    rwaccess = await RWAccess.deploy(
      await pyusd.getAddress(),
      1000, // pricePerSecond = 0.001 PYUSD/sec.
      "room123.hotel.eth"
    );
    await rwaccess.waitForDeployment();
    console.log("Deployed RWAccess at", await rwaccess.getAddress());


    // Give user PYUSD.
    await pyusd.transfer(user.address, ethers.parseUnits("1000", 6));
    console.log("Transfered USD ", ethers.parseUnits("1000", 6),  " to user ", user.address);
  });
const { expect } = require("chai");
const { ethers } = require("hardhat");

  it("should allow access and reject overlaps", async function () {
    // const tstart = Math.floor(Date.now() / 1000) + 60; // 1 min from now.
    const tstart = 1755555555;  // 2025/08/18 22:19:15
    const tend = tstart + 3600; // 1h access

    // Approve payment.
    const cost = BigInt(tend - tstart) * 1000n; // pricePerSecond=1000.
    console.log("Approving RWAaccess to spend user's USD");
    await pyusd.connect(user).approve(await rwaccess.getAddress(), cost);

    // Pay for new access.
    console.log(`Paying for Access from ${tstart} to ${tend}`);
    const tx = await rwaccess.connect(user).pay(tstart, tend);
    const receipt = await tx.wait();

    // Parse AccessCreated event
    console.log(`Signer waiting for AccessCreated event`);
    const accessCreatedLog = receipt.logs
      .map(log => {
        try {
          return rwaccess.interface.parseLog(log);
        } catch (e) {
          return null;
        }
      })
      .find(parsed => parsed && parsed.name === "AccessCreated");

    expect(accessCreatedLog).to.not.be.null;
    console.log(`AccessCreated event created: ${accessCreatedLog.args}`);

    const accessId = accessCreatedLog.args.accessId;

    // Try overlapping access (should fail).
    console.log(`Check overlapping access cannot be created`);
    await pyusd.connect(user).approve(await rwaccess.getAddress(), cost);
    await expect(
      rwaccess.connect(user).pay(tstart + 1800, tend + 1800)
    ).to.be.revertedWith("Interval overlaps existing access");

    // Fulfill signature (simulate external signer).
    // ABI-encode the event data and sign it.
    console.log(`Signer creating transaction to sign/validate access.`);

    const abiCoder = new ethers.AbiCoder();
    const abi_encoded = abiCoder.encode(
        ["address", "uint64", "uint64", "string"],
        [
          accessCreatedLog.args.user,
          accessCreatedLog.args.tstart,
          accessCreatedLog.args.tend,
          accessCreatedLog.args.ens
        ]
    );

    const hashed = ethers.keccak256(abi_encoded);
    console.log("Keccak:", hashed);
    const bytesConverter = ethers.getBytes || ethers.utils.arrayify;
    const signed = await owner.signMessage(bytesConverter(hashed));
    console.log("Access validated and signed: ", signed);

    const tx2 = await rwaccess.connect(owner).fulfillSignature(accessId, signed);
    const receipt2 = await tx2.wait();

    console.log("Expecting AccessSigned event.");
    // Parse AccessSigned event
    const accessSignedLog = receipt2.logs
      .map(log => {
        try {
          return rwaccess.interface.parseLog(log);
        } catch (e) {
          return null;
        }
      })
      .find(parsed => parsed && parsed.name === "AccessSigned");

    expect(accessSignedLog).to.not.be.null;
    console.log("AccessSigned event created:", accessSignedLog.args);
  });
});


/*************************************************************************
 * This test was used to test various core functionalities.

describe("Message Encoding, Signing, and Verification", function () {
  it("should encode, sign, and verify a message with address, uint64, and string", async function () {
    // Get signer (first account from Hardhat's default accounts).
    const [signer] = await ethers.getSigners();
    const senderAddress = signer.address;

    // Message components.
    const address = "0x1234567890abcdef1234567890abcdef12345678"; // Example address
    const uint64Value = BigInt(1234567890); // Example uint64
    const stringValue = "Hello, World!";

    // Step 1: Encode the message (address, uint64, string) using ABI encoding
    // Use ethers.AbiCoder for v6 compatibility, fallback to utils for v5
    const abiCoder = ethers.AbiCoder ? new ethers.AbiCoder() : ethers.utils;
    const encodedMessage = abiCoder.encode(
      ["address", "uint64", "string"],
      [address, uint64Value, stringValue]
    );
    console.log("Encoded Message (hex):", encodedMessage);

    // Step 2: Create a hash of the encoded message for signing
    const messageHash = ethers.keccak256(encodedMessage);
    console.log("Message Hash:", messageHash);

    // Step 3: Sign the message (using Ethereum personal sign format)
    // Use ethers.getBytes for v6, fallback to ethers.utils.arrayify for v5
    const bytesConverter = ethers.getBytes || ethers.utils.arrayify;
    const signature = await signer.signMessage(bytesConverter(messageHash));
    console.log("Signature:", signature);

    // Step 4: Verify the signature
    const recoveredAddress = ethers.verifyMessage(bytesConverter(messageHash), signature);
    console.log("Recovered Address:", recoveredAddress);

    // Decode the message to confirm correctness
    const decodedMessage = abiCoder.decode(
      ["address", "uint64", "string"],
      encodedMessage
    );
    console.log("Decoded Message:", decodedMessage);

    // Log results
    console.log("Original Address:", address);
    console.log("Original Uint64:", uint64Value.toString());
    console.log("Original String:", stringValue);

    // Assertions
    expect(recoveredAddress.toLowerCase()).to.equal(senderAddress.toLowerCase(), "Signature verification failed");
    expect(decodedMessage[0].toLowerCase()).to.equal(address.toLowerCase(), "Decoded address does not match");
    expect(decodedMessage[1]).to.equal(uint64Value, "Decoded uint64 does not match");
    expect(decodedMessage[2]).to.equal(stringValue, "Decoded string does not match");
  });
});

*************************************************************************/