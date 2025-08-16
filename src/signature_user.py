#!/usr/bin/env bash

import json
from shared import *


def sign_user(data):
    # Step 1: ABI-encode the data.
    abi_encoded = encode(
        ["address", "uint64", "uint64", "string", "string"],
        [data["user"], data["tstart"], data["tend"], data["ens"], data["sig1"]]
    )
    print(f"ABI encoded: 0x{abi_encoded.hex()}")

    # Step 2: Hash the encoded data with keccak256.
    hashed = Web3.keccak(abi_encoded)
    print(f"Keccak: 0x{hashed.hex()}")

    # Step 3: Sign the hash with Ethereum's signed message prefix.
    eth_encoded = encode_defunct(hexstr=hashed.hex())
    print(f"Hashed: {eth_encoded}")

    signed_message = user.sign_message(eth_encoded)
    signature = signed_message.signature
    print(f"Signed: 0x{signature.hex()}")

    # Step 4: Verify the signature.
    recovered_address = w3.eth.account.recover_message(eth_encoded, signature=signature)
    print(f"Recovered Address: {recovered_address}")

    # Optional: Compare with expected owner address.
    assert recovered_address.lower() == user.address.lower(), "Signature verification failed"
    print("Signature verification successful.")

    keyAccess = data
    keyAccess.update({'sig2': signature.hex()})
    return keyAccess


def example():
    data = {
          'user': '0x25a0fEC55dD7cc314A8Bb00e666489524b7d9cB9',
        'tstart': 1755555555,
          'tend': 1755559155,
           'ens': 'room123.hotel.eth',
          'sig1':'0x50b985ba21094dce584b288d2726ddaf185675c80f955df07d956784b0f97d8d18dae37032c182b3196e4bd4a41796ebb8719ec97f1fd525d12a76da60419ab51b'
    }

    key_access = sign_user(data)
    print("KeyAccess:")
    print(json.dumps(key_access, indent=2))


if __name__ == "__main__":
    example()

