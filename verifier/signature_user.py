import json

from web3 import Web3
from eth_abi import encode
from eth_account import Account
from eth_account.messages import encode_defunct

# Configuration
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# User  address: 0x25a0fEC55dD7cc314A8Bb00e666489524b7d9cB9
keyUser = "0xfa25c75192e85a56820acaf74a6157d2bb3a5df7ac23b7e025340f87b38d3def"
user = Account.from_key(keyUser)
print(f"addr user: {user.address}")

data = {
      'user': '0x25a0fEC55dD7cc314A8Bb00e666489524b7d9cB9',
    'tStart': 1755555555,
      'tEnd': 1755559155,
  'assetENS': 'room123.hotel.eth',
      'sign':'0x50b985ba21094dce584b288d2726ddaf185675c80f955df07d956784b0f97d8d18dae37032c182b3196e4bd4a41796ebb8719ec97f1fd525d12a76da60419ab51b'
}

# Run the encryption forward.

# Step 1: ABI-encode the data
abi_encoded = encode(
    ["address", "uint64", "uint64", "string", "string"],
    [data["user"], data["tStart"], data["tEnd"], data["assetENS"], data["sign"]]
)
print(f"ABI encoded: 0x{abi_encoded.hex()}")  # Matches ethers.AbiCoder.encode

# Step 2: Hash the encoded data with keccak256
hashed = Web3.keccak(abi_encoded)
print(f"Keccak: 0x{hashed.hex()}")

# Step 3: Sign the hash with Ethereum's signed message prefix
eth_encoded = encode_defunct(hexstr=hashed.hex())
print(f"Hashed: {eth_encoded}")

signed_message = user.sign_message(eth_encoded)
signature = signed_message.signature
print(f"Signed: 0x{signature.hex()}")

# Step 4: Verify the signature
recovered_address = w3.eth.account.recover_message(eth_encoded, signature=signature)
print(f"Recovered Address: {recovered_address}")

# Optional: Compare with expected owner address
assert recovered_address.lower() == user.address.lower(), "Signature verification failed"
print("Signature verification successful.")

keyAccess = data
keyAccess.update({'key': signature.hex()})
print("KeyAccess:")
print(json.dumps(keyAccess, indent=2))
