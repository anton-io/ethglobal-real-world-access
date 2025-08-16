from web3 import Web3
from eth_abi import encode
from eth_account import Account
from eth_account.messages import encode_defunct


# Setup logging to stdout.
import logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    handlers=[logging.StreamHandler()]  # Output to stdout
)
# Create a logger.
log = logging.getLogger(__name__)


# RPC Configuration
RPC_URL = "http://127.0.0.1:8545"

# w3 End-point configuration.
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Owner address: 0x8163a3415402B498c7441D0D19DDe724E104Ab82
# User  address: 0x25a0fEC55dD7cc314A8Bb00e666489524b7d9cB9

KEY_OWNER = "0xa4cb42b54fa055392dafbda0f70f9e4d075b77eff4c988011341674740acd733"
KEY_USER  = "0xfa25c75192e85a56820acaf74a6157d2bb3a5df7ac23b7e025340f87b38d3def"
owner = Account.from_key(KEY_OWNER)
user = Account.from_key(KEY_USER)


