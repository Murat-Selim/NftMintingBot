from web3 import Web3 
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv('.env')

# Ethereum network connection
alchemy_url = os.environ['ALCHEMY_API_URL']
web3 = Web3(Web3.HTTPProvider(alchemy_url))

# Wallet information
private_key = os.environ['PRIVATE_KEY']

# Smart contract information
contract_address =  Web3.to_checksum_address("0xC8894fB6721FB234E6256a0c12C62BE43F0C2ABE")
contract_abi = os.environ['CONTRACT_ABI']

# Mint Processing
def mint_nft(to_address, token_uri):

    # Create contract instance
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    # Perform minting transaction
    txn = contract.functions.mintItem(to_address, token_uri).build_transaction({
        'from': to_address,
        'gas': 300_000,  # Adjust the gas limit as per your requirement
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(to_address), # type: ignore
    })

    signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    print("Minting transaction sent. Transaction hash:", tx_hash.hex())

to_address = Web3.to_checksum_address("0x000000000000000000000000000")
token_uri = "https://ipfs.io/ipfs/QmVHi3c4qkZcH3cJynzDXRm5n7dzc9R9TUtUcfnWQvhdcw"

# minting nft
try:
    mint_nft(to_address, token_uri)
except Exception as e:
    print("Error:", e)
