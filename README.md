# RWAccess - Real World Access

**RWAccess** is a Proof-of-Concept (PoC) demonstrating secure, decentralized access control for real-world assets using blockchain, cryptography, and QR codes. 

This project leverages a Solidity smart contract to manage access rights, powered by PayPal's PYUSD stablecoin, with ENS names for user-friendly asset identification. 

Access is granted via QR codes containing cryptographically signed messages, replacing traditional keys or passes.

This innovative system has the potential to transform access control across industries, enabling secure, scalable, and seamless solutions for physical and digital assets.

## Overview

RWAccess enables secure access to real-world assets (e.g., hotel rooms, vehicles, gyms, or event venues) through a blockchain-based system.

Users pay for time-bound access using PYUSD, defined by `tstart` and `tend` in Unix time. The smart contract generates a signed message, encoded into a QR code, which is verified by a grantor to grant or deny access.

### Key Features
- **Solidity Smart Contract**: Manages access rights, ensuring no double-booking by tracking `tstart` and `tend`.
- **PYUSD Payments**: Access is paid in PayPal's PYUSD stablecoin, with a configurable price-per-second set by the contract owner.
- **ENS Integration**: Uses ENS names for human-readable, upgradable, and compact asset identification in QR codes.
- **Signed QR Codes**: Logs a structure `[user, tstart, tend, asset, signature]` after payment; an external process signs it for secure verification.
- **Offline Operation**: Designed for minimal dependencies, allowing requestors and grantors to operate without internet access.

## Applications
RWAccess can replace or complement traditional access methods, such as:
- **Physical Keys/Passes**: Hotel keycards, car keys, gym passes, plane tickets, or event badges.
- **Advanced Use Cases**:
  - **Gamification**: Integrate with loyalty programs or token-based rewards for seamless user engagement.
  - **Easy Recovery**: Recover lost access credentials via blockchain-based identity.
  - **Scalable Access**: Enable shared access for rentals, co-working spaces, or community resources.

## Why ENS?
1. **Human-Readable**: Simplifies user experience with names like `room123.hotel.eth` instead of cryptic addresses. It can also easily point to which access it refers to, for example: `branchX.club.eth`, `license.car.eth`, `ticketX.concert.eth`, etc.

1. **Security**: The ens can resolve to address that is expected as the owner (i.e. _sig1_ must resolve to that same address)

1. **Compact QR Codes**: Reduces QR code density for better machine readability.
1. **Transparent Upgrades**: Allows seamless updates to the coordinator address via ENS.

## How It Works
1. **Asset Setup**: The contract owner assigns an ENS name to the asset (visible only to them).
2. **Payment**: Users pay in PYUSD for access between `tstart` and `tend`. The contract validates availability and logs the booking.
3. **Signed Message**: A structure `[tstart, tend, asset, user, sig1, sig2]` is logged (initially with an empty signature) and signed externally.
4. **QR Code Generation**: The signed message is encoded into a QR code.
5. **Access Verification**: The grantor scans the QR code, verifies the signature, and grants access if valid and within the time window.

## Trade-offs
To ensure simplicity and offline compatibility, RWAccess prioritizes minimal dependencies, which limits features like:
- Real-time access revocation.
- Complex scheduling or dynamic verification.

## Potential Improvements
As a minimal PoC, RWAccess can be extended with:
- **Access Tracking**: Count asset usage for analytics or billing.
- **Revocation**: Enable grantors to revoke access via contract queries.
- **Refunds**: Automatically revoke access upon refund initiation.
- **Granular Scheduling**: Restrict access to specific daily time slots (e.g., 1 PM–2 PM).
- **Nonce-Based Security**: Use nonces and random generators for real-time, secure challenge-response verification.
- **Bi-Directional Authentication**: Implement proprietary protocols for enhanced security.