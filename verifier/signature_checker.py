from web3 import Web3
from eth_abi import encode
from eth_account import Account
from eth_account.messages import encode_defunct

# Configuration
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Owner address: 0x8163a3415402B498c7441D0D19DDe724E104Ab82
# User  address: 0x25a0fEC55dD7cc314A8Bb00e666489524b7d9cB9

keyOwner = "0xa4cb42b54fa055392dafbda0f70f9e4d075b77eff4c988011341674740acd733";
owner = Account.from_key(keyOwner)
print(f"addr owner: {owner.address}")

# User  address: 0x25a0fEC55dD7cc314A8Bb00e666489524b7d9cB9
keyUser = "0xfa25c75192e85a56820acaf74a6157d2bb3a5df7ac23b7e025340f87b38d3def"
user = Account.from_key(keyUser)
print(f"addr user: {user.address}")

data = {
      'user': '0x25a0fEC55dD7cc314A8Bb00e666489524b7d9cB9',
    'tStart': 1755555555,
      'tEnd': 1755559155,
  'assetENS': 'room123.hotel.eth',
      'sign':'0x50b985ba21094dce584b288d2726ddaf185675c80f955df07d956784b0f97d8d18dae37032c182b3196e4bd4a41796ebb8719ec97f1fd525d12a76da60419ab51b',
       "key": "8169b59a86b3b752a858d14b05c2751679b50d925d23b835ad63cee7352b65ae310dac6268266e5aabb1e7b52164ce95bbccebc10a1490d36563a9ba8f61081b1b"
}

# Run the encryption forward.

# Step 1: ABI-encode access data.
abi_encoded = encode(
    ["address", "uint64", "uint64", "string"],
    [data["user"], data["tStart"], data["tEnd"], data["assetENS"]]
)
print(f"ABI encoded: 0x{abi_encoded.hex()}")  # Matches ethers.AbiCoder.encode

# Step 2: Hash the encoded data with keccak256
hashed = Web3.keccak(abi_encoded)
print(f"Keccak: 0x{hashed.hex()}")

# Step 3: Sign the hash with Ethereum's signed message prefix
eth_encoded = encode_defunct(hexstr=hashed.hex())
print(f"Hashed: {eth_encoded}")

signed_message = owner.sign_message(eth_encoded)
signature = signed_message.signature
print(f"Signed: 0x{signature.hex()}")

# Step 4: Verify the signature
recovered_address = w3.eth.account.recover_message(eth_encoded, signature=signature)
print(f"Recovered Address: {recovered_address}")

# Optional: Compare with expected owner address
assert recovered_address.lower() == owner.address.lower(), "Signature verification failed"
print("Signature verification successful")