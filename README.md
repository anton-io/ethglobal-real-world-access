# RWAccess - Real World Access

**RWAccess** is a Proof-of-Concept (PoC) demonstrating secure, decentralized access control for real-world assets using blockchain, cryptography, and QR codes. 

By making a stablecoin payment to a smart contract, users receive a QR code that serves as a secure digital key. This key can replace or complement traditional access methods, such as hotel room keys, conference passes, gym memberships, or any system requiring gated access, offering a seamless and versatile solution.

Access is granted via QR codes containing cryptographically signed messages, replacing traditional keys or passes.

This innovative system has the potential to transform access control across industries, enabling secure, scalable, and seamless solutions for physical and digital assets.

This project leverages a Solidity smart contract to manage access rights, powered by __PayPal's PYUSD__ stablecoin, with __ENS__ names for user-friendly asset identification, and it's contract is deployed on __Zircuit__ and Sepolia Testnet at the following addresses:

* Zircuit Contract: [0x6aef6b0b33a4f99cdd4bac962700bf17b700b6b7](https://explorer.zircuit.com/address/0x6aef6b0b33a4f99cdd4bac962700bf17b700b6b7?activeTab=3)
* Sepolia Contract: [0xaf2c722e2f2dd5bedbe7be08043604ce94a00240](https://sepolia.etherscan.io/address/0xaf2c722e2f2dd5bedbe7be08043604ce94a00240#code) 


Both contracts have been deployed and verified.

## Overview

RWAccess enables secure access to real-world assets (e.g., hotel rooms, vehicles, gyms, or event venues) through a blockchain-based system.

Users pay for time-bound access using PYUSD, defined by `tstart` and `tend` in Unix time. After payment, a signature server validates and signs grants access-rights by signing the access request. This signed message, when combined with the user's signature is used to generate a QR code that can be used by any access verifier to grant or deny access.

### Key Features
- **Solidity Smart Contract**: Manages access rights, ensuring no double-booking by tracking `tstart` and `tend`.
- **PYUSD Payments**: Access is paid in PayPal's PYUSD stablecoin, with a configurable price-per-second set by the contract owner.
- **ENS Integration**: Uses ENS names for human-readable, upgradable, and compact asset identification in QR codes, and enhanced security via asset address resolution.
- **Signed QR Codes**: Act as key/pass with the following fields: `[addr, tstart, tend, ens, sig1, sig2]`.
- **Offline Operation**: Designed for minimal dependencies, allowing requestors and grantors to operate without internet access.

## Applications
RWAccess can replace or complement traditional access methods, such as:
- **Physical Keys/Passes**: Hotel keycards, car keys, gym passes, plane tickets, or event badges.
- **Advanced Use Cases**:
  - **Gamification**: Integrate with loyalty programs or token-based rewards for seamless user engagement.
  - **Easy Recovery**: Recover lost access credentials via blockchain-based identity.
  - **Scalable Access**: Enable shared access for rentals, co-working spaces, or community resources.

## Why ENS?

The Ethereum Name Service (ENS) simplifies blockchain interactions by mapping human-readable domain names, like example.eth, to Ethereum addresses, enhancing user experience and security for transactions and dApps.


1. **Human-Readable**: Simplifies user experience with names like `room123.hotel.eth` instead of cryptic addresses. It can also easily point to which access it refers to, for example: `branchX.club.eth`, `license.car.eth`, `ticketX.concert.eth`, etc.
1. **Security**: The ens can resolve to address that is expected as the owner (i.e. _sig1_ must resolve to that same address)
1. **Compact QR Codes**: Reduces QR code density for better machine readability.
1. **Transparent Upgrades**: Allows seamless updates to the coordinator address via ENS.

## Why PayPal USD?

PayPal USD (PYUSD) is a U.S. dollar-pegged stablecoin integrated into PayPal’s vast merchant network, enabling fast, low-cost, and secure digital payments across blockchain and traditional platforms.

1. **Price Predictability**: PYUSD is pegged 1:1 to the U.S. dollar, ensuring stable value and minimizing volatility risks, making it ideal for transactions and financial planning.
1. **Access to PayPal’s Vast Network**: With over 426 million active users and 20 million merchants, PYUSD integrates seamlessly into PayPal’s ecosystem, enabling widespread use for online and point-of-sale transactions.
1. **Fast Transactions**: PYUSD enables near-instant settlements, especially for cross-border payments, compared to traditional banking methods that can take days.
1. **Low Transaction Costs**: PYUSD reduces fees by bypassing intermediaries, offering a cost-effective alternative for international transfers and micro-payments.
1. **Enhanced User Trust**: Backed by PayPal’s established brand and regulatory compliance, PYUSD fosters confidence for businesses and consumers new to crypto.


## Why Zircuit Blockchain?

Zircuit is an Ethereum Layer 2 zk-rollup blockchain leveraging AI-driven security to protect transactions, offering low-cost, high-speed processing ideal for applications like secure QR code-based access systems.

1. **AI-Powered Security for Access Keys**: Zircuit’s Sequencer Level Security (SLS) uses AI to monitor transactions in real-time, detecting and blocking malicious activities like hacks, phishing, or unauthorized access attempts before they are included in a block. This proactive approach ensures that smart contract-based access keys (e.g., QR codes tied to stablecoin payments) are protected from exploits, safeguarding gated access systems for hotels, gyms, or conferences.
1. **Privacy via Zero-Knowledge Proofs**: Zircuit’s zk-rollup architecture ensures transaction privacy by validating transactions without revealing sensitive data, protecting user details tied to access keys while maintaining security and efficiency.
1. **Scalability for Broad Applications**: Zircuit supports high transaction throughput, making it suitable for scaling access control systems across large venues or networks, such as issuing thousands of QR code keys for conferences or memberships without network congestion.


## How It Works?
1. **Access Setup**: A RWAccess contract is deployed with an ENS identifier and price per second.
2. **Payment**: Users pay in PYUSD for access between `tstart` and `tend`. The contract validates availability and logs the booking.
3. **Signed Message**: A structure `[user, tstart, tend, ens, sig1]` is logged (initially with an empty signature) and signed by a validator.
4. **QR Code Generation**: The final signed message with the user's signature is encoded into an access QR code.
5. **Access Verification**: The access grantor scans the QR code, verifies the signatures (one for the validator, and another from the user), and grants access if valid and within the time window.

## Trade-offs

To ensure simplicity and offline compatibility, RWAccess prioritizes minimal dependencies, which limits features including:
- Multi-simultaneous users.
- Real-time access revocation.
- Complex scheduling or dynamic verification.

However, this PoC implementation is easily extensible to be customized for any particular requirements.  

## Potential Improvements

As a minimal PoC, RWAccess can be extended with:
- **Access Tracking**: Count asset usage for analytics or billing.
- **Revocation**: Enable grantors to revoke access via contract queries.
- **Refunds**: Automatically revoke access upon refund initiation.
- **Granular Scheduling**: Restrict access to specific daily time slots (e.g., 1 PM–2 PM).
- **Nonce-Based Security**: Use nonces and random generators for real-time, secure challenge-response verification.
- **Bi-Directional Authentication**: Implement proprietary protocols for enhanced security.