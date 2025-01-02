# agent_sdk/blockchain.py
import json
from typing import Dict
from web3 import Web3, HTTPProvider
from eth_account import Account
from eth_account.messages import encode_defunct
import os

class AIPNContract:
    def __init__(self, network_config: Dict):
        self.web3 = Web3(HTTPProvider(network_config["provider_url"]))
        if not self.web3.is_connected():
            raise ConnectionError("Failed to connect to Ethereum provider.")

        self.contract_address = network_config["contract_address"]

        # Construct the path to the ABI file
        current_dir = os.path.dirname(__file__)
        abi_path = os.path.join(current_dir, 'artifacts', 'contracts', 'aipn_contract.sol', 'AgentIDProviderNetwork.json')

        # Check if the ABI file exists
        if not os.path.exists(abi_path):
            raise FileNotFoundError(f"ABI file not found at {abi_path}")

        with open(abi_path, "r") as f:
            contract_abi = json.load(f)["abi"]  # Load only the 'abi' part
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=contract_abi)
        self.signer_address = network_config["signer_address"]

    def register_did(self, did: str, did_document_json: str) -> bool:
        """Registers a DID and its document on the AIPN contract."""
        try:
            # Use Hardhat's provider and signer (or configured account)
            tx_hash = self.contract.functions.registerDID(did, did_document_json).transact({"from": self.signer_address})
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            if receipt.status == 1:
                print(f"DID registered successfully: {did}")
                print(f"Transaction Hash: {tx_hash.hex()}")
                return True
            else:
                print(f"DID registration failed: {did}")
                print(f"Transaction Hash: {tx_hash.hex()}")
                return False
        except Exception as e:
            print(f"Error registering DID: {e}")
            return False

    def resolve_did(self, did: str) -> Dict:
        """Resolves a DID from the AIPN contract."""
        try:
            did_document_json = self.contract.functions.resolveDID(did).call()
            if did_document_json:
                return json.loads(did_document_json)
            else:
                return {}  # Return empty dict if DID not found
        except Exception as e:
            print(f"Error resolving DID: {e}")
            return {}

    def sign_message(self, message: str, private_key: str):
        """Signs a message using the provided private key."""
        account = Account.from_key(private_key)
        message_hash = encode_defunct(text=message)
        signed_message = account.sign_message(message_hash)
        return signed_message.signature.hex()

    def verify_signature(self, message: str, signature: str, address: str) -> bool:
        """Verifies a message signature."""
        message_hash = encode_defunct(text=message)
        try:
            signer = Account.recover_message(message_hash, signature=signature)
            return signer.lower() == address.lower()
        except Exception as e:
            print(f"Error verifying signature: {e}")
            return False