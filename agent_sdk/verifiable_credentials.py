
import json
from typing import Dict
from .utils import sign_data, verify_signature

class VerifiableCredential:
    def __init__(self, issuer_did: str, subject_did: str, claims: Dict, proof: Dict = None):
        self.issuer_did = issuer_did
        self.subject_did = subject_did
        self.claims = claims
        self.proof = proof

    def to_json(self):
        return {
            "@context": [
                "https://www.w3.org/2018/credentials/v1",
                "https://example.org/agent-credentials/v1"
            ],
            "type": ["VerifiableCredential", "AgentCredential"],
            "issuer": self.issuer_did,
            "credentialSubject": {
                "id": self.subject_did,
                **self.claims
            },
            "proof": self.proof
        }
    
    def sign_credential(self, private_key):
        unsigned_credential = self.to_json()
        unsigned_credential.pop("proof")
        signature = sign_data(json.dumps(unsigned_credential), private_key)
        self.proof = {
            "type": "Ed25519Signature2018",
            "created": "2024-08-20T12:00:00Z",
            "verificationMethod": f"{self.issuer_did}#key1",
            "proofPurpose": "assertionMethod",
            "jws": signature
        }

    @staticmethod
    def verify_credential(credential: Dict, public_key: str) -> bool:
        signature = credential["proof"]["jws"]
        unsigned_credential = credential.copy()
        unsigned_credential.pop("proof")
        return verify_signature(json.dumps(unsigned_credential), signature, public_key)
        