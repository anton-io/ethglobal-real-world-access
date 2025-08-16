#!/usr/bin/env bash

from shared import *

CONTRACT_ADDRESS = "0xYourContractAddressHere"

# Contract ABI (simplified for the event and function)
CONTRACT_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "bytes32", "name": "accessId", "type": "bytes32"},
            {"indexed": True, "internalType": "address", "name": "user", "type": "address"},
            {"internalType": "uint64", "name": "tstart", "type": "uint64"},
            {"internalType": "uint64", "name": "tend", "type": "uint64"},
            {"internalType": "string", "name": "ens", "type": "string"},
            {"internalType": "bytes", "name": "signature", "type": "bytes"}
        ],
        "name": "AccessCreated",
        "type": "event"
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "accessId", "type": "bytes32"},
            {"internalType": "bytes", "name": "signature", "type": "bytes"}
        ],
        "name": "fulfillSignature",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Ensure connection
if not w3.is_connected():
    raise Exception("Failed to connect to Ethereum node")

# Initialize contract
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)


# Function to create a signature for the event data
def create_signature(data):
    # Encode the data to be signed (user, tstart, tend, ens)
    # For simplicity, we'll encode as a string, but adjust based on your contract's expected signature format
    message = f"{data['user']}{data['tstart']}{data['tend']}{data['ens']}"
    message_hash = encode_defunct(text=message)
    signed_message = w3.eth.account.sign_message(message_hash, private_key=KEY_OWNER)
    return signed_message.signature.hex()


# Function to call fulfillSignature
def call_fulfill_signature(booking_id, signature):
    # Build transaction
    nonce = w3.eth.get_transaction_count(owner.address)
    tx = contract.functions.fulfillSignature(
        booking_id,
        signature
    ).build_transaction({
        "from": owner.address,
        "nonce": nonce,
        "gas": 200000,  # Adjust gas limit as needed
        "gasPrice": w3.to_wei("20", "gwei")  # Adjust gas price as needed
    })

    # Sign and send transaction
    signed_tx = w3.eth.account.sign_transaction(tx, KEY_OWNER)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"fulfillSignature called. Tx hash: {tx_hash.hex()}")


# Event listener
def handle_event(event):
    try:
        # Extract event data
        event_data = {
            "accessId": event["args"]["accessId"],
            "user": event["args"]["user"],
            "tstart": event["args"]["tstart"],
            "tend": event["args"]["tend"],
            "ens": event["args"]["ens"]
        }
        print(f"New AccessCreated event: {event_data}")

        # Create signature for the data
        data_to_sign = {
            "user": event_data["user"],
            "tstart": event_data["tstart"],
            "tend": event_data["tend"],
            "ens": event_data["ens"]
        }
        signature = create_signature(data_to_sign)
        print(f"Generated signature: {signature}")

        # Call fulfillSignature
        call_fulfill_signature(event_data["accessId"], signature)

    except Exception as e:
        print(f"Error processing event: {e}")


# Main function to listen for events
def listen_for_events():
    print("Listening for AccessCreated events...")
    event_filter = contract.events.AccessCreated.create_filter(fromBlock="latest")

    while True:
        try:
            for event in event_filter.get_new_entries():
                handle_event(event)
        except Exception as e:
            print(f"Error in event loop: {e}")
            # Optionally, add a sleep to avoid hammering the node
            import time
            time.sleep(2)


# Run the listener
if __name__ == "__main__":
    try:
        listen_for_events()
    except KeyboardInterrupt:
        print("Stopped listening for events")