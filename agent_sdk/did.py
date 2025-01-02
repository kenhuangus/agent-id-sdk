import json
from hashlib import sha256
from typing import List, Dict, Optional
from .utils import generate_key_pair, sign_data, verify_signature, encode_public_key_to_multibase

class DID:
    def __init__(self, did_string: Optional[str] = None, private_key: Optional[str] = None):
        self.private_key, self.public_key = generate_key_pair()
        if did_string:
            self.did = did_string
            # Extract public key from a provided DID (if needed for verification)
            # Assuming the DID string follows a standard format where the public key can be derived
            self.public_key = did_string.split(":")[-1]
            if private_key:
                self.private_key = private_key
        else:
            # Encode public key to Base58 for DID creation
            self.public_key_multibase = encode_public_key_to_multibase(self.public_key)
            self.did = f"did:example:{self.public_key_multibase}"

    def create_did_document(self, service_endpoints: List[Dict] = []) -> Dict:
        did_document = {
            "@context": ["https://www.w3.org/ns/did/v1", "https://example.org/agent-context/v1"],
            "id": self.did,
            "verificationMethod": [
                {
                    "id": f"{self.did}#key1",
                    "type": "Ed25519VerificationKey2018",
                    "controller": self.did,
                    "publicKeyMultibase": self.public_key_multibase,
                }
            ],
            "service": service_endpoints,
        }
        return did_document

    def sign_did_document(self, did_document: Dict) -> str:
        return sign_data(json.dumps(did_document), self.private_key)

    @staticmethod
    def verify_did_document(did_document: Dict, signature: str) -> bool:
        public_key = did_document["verificationMethod"][0]["publicKeyMultibase"]
        return verify_signature(json.dumps(did_document), signature, public_key)