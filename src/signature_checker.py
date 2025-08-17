#!/usr/bin/env python3
from shared import *


def _signature_check_abi(abi_encoded, signature, addr_expected):
    hashed = Web3.keccak(abi_encoded)
    eth_encoded = encode_defunct(hexstr=hashed.hex())
    recovered_address = w3.eth.account.recover_message(eth_encoded, signature=signature)
    return recovered_address.lower() == addr_expected.lower()


def signature_check(data):
    # Check owner has signed correctly.
    abi_encoded_1 = encode(
        ["address", "uint64", "uint64", "string"],
        [data["user"], data["tstart"], data["tend"], data["ens"]]
    )
    if not _signature_check_abi(abi_encoded_1, data['sig1'], owner.address):
        print("error: signature 1 unsuccessful")
        return False

    # Check user has signed correctly.
    abi_encoded_2 = encode(
        ["address", "uint64", "uint64", "string", "string"],
        [data["user"], data["tstart"], data["tend"], data["ens"], data["sig1"]]
    )
    if not _signature_check_abi(abi_encoded_2, data['sig2'], data['user']):
        print("error: signature 2 unsuccessful")
        return False

    return True


def example():
    data = {
        'user': '0x25a0fEC55dD7cc314A8Bb00e666489524b7d9cB9',
        'tstart': 1755555555,
        'tend': 1755559155,
        'ens': 'room123.hotel.eth',
        'sig1': '0x50b985ba21094dce584b288d2726ddaf185675c80f955df07d956784b0f97d8d18dae37032c182b3196e4bd4a41796ebb8719ec97f1fd525d12a76da60419ab51b',
        "sig2": "0x8169b59a86b3b752a858d14b05c2751679b50d925d23b835ad63cee7352b65ae310dac6268266e5aabb1e7b52164ce95bbccebc10a1490d36563a9ba8f61081b1b"
    }
    if signature_check(data):
        print("Success! Signatures are both valid!")


if __name__ == "__main__":
    example()
