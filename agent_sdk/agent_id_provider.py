
import json
from typing import Dict
from web3 import Web3, HTTPProvider
from eth_account import Account
from .blockchain import AIPNContract
from .did import DID
from .verifiable_credentials import VerifiableCredential
from .utils import is_valid_did

class AgentIdProvider:
    def __init__(self, network_config: Dict):
        self.network_config = network_config  # e.g., blockchain node URLs, contract addresses
        self.aipn_contract = AIPNContract(network_config)
    
    def register_agent_did(self, did: "DID", did_document: Dict) -> bool:
        return self.aipn_contract.register_did(did.did, json.dumps(did_document))

    def resolve_agent_did(self, did_string: str) -> Dict:
        return self.aipn_contract.resolve_did(did_string)
    
    def create_verifiable_credential(self, issuer_did, subject_did, claims):
        return VerifiableCredential(issuer_did, subject_did, claims)
        