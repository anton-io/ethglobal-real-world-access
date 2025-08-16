from web3 import Web3
from eth_account.messages import encode_defunct
import eth_abi

# Connect to an Ethereum node (replace with your provider, e.g., Infura).
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))  # Local node or Infura URL.

# Sender's private key and address (replace with your own for testing)
private_key = '0xa4cb42b54fa055392dafbda0f70f9e4d075b77eff4c988011341674740acd733'
account = w3.eth.account.from_key(private_key)
sender_address = account.address
print(f"Sender address: {sender_address}")

# Message components
address = '0x1234567890abcdef1234567890abcdef12345678'  # Example address
uint64_value = 1234567890  # Example uint64
string_value = 'Hello, World!'

# Step 1: Encode the message (address, uint64, string) using ABI encoding
encoded_message = eth_abi.encode(['address', 'uint64', 'string'], [address, uint64_value, string_value])

# Step 2: Create a hash of the encoded message for signing (EIP-191 compliant)
message_hash = Web3.keccak(encoded_message)
signable_message = encode_defunct(hexstr=message_hash.hex())

# Step 3: Sign the message
signed_message = w3.eth.account.sign_message(signable_message, private_key=private_key)
signature = signed_message.signature.hex()

# Step 4: Verify the signature
recovered_address = w3.eth.account.recover_message(signable_message, signature=signature)

# Output results
print(f"Original Address: {address}")
print(f"Original Uint64: {uint64_value}")
print(f"Original String: {string_value}")
print(f"Encoded Message (hex): {encoded_message.hex()}")
print(f"Message Hash: {message_hash.hex()}")
print(f"Sender Address: {sender_address}")
print(f"Signature: {signature}")
print(f"Recovered Address: {recovered_address}")
print(f"Signature Valid: {recovered_address.lower() == sender_address.lower()}")

# Decode the original message to confirm correctness
decoded_message = eth_abi.decode(['address', 'uint64', 'string'], encoded_message)
print(f"Decoded Message: {decoded_message}")