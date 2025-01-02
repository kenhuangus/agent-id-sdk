# examples.py
from agent_sdk import AgentIdProvider, DID, VerifiableCredential
from agent_sdk.blockchain import AIPNContract
import json
import os
from eth_account import Account

# Fetch the private key from the environment variable
private_key = os.environ.get("PRIVATE_KEY")
if not private_key:
    raise ValueError("PRIVATE_KEY environment variable not set.")

# Derive the corresponding Ethereum address from the private key
account = Account.from_key(private_key)
public_address = account.address

# Hardhat network configuration
network_config = {
    "network_name": "hardhat",
    "provider_url": "http://localhost:8545",
    "contract_address": "0x5FbDB2315678afecb367f032d93F642f64180aa3",  # **Replace with your deployed contract address**
    "signer_address": public_address
}

# Create an Agent ID Provider instance
provider = AgentIdProvider(network_config)

# Example Usage
if __name__ == "__main__":
    print("Starting examples...")

    # 1. Create a new DID using the private key from environment variable
    print("\n1. Creating a new DID...")
    agent_did = DID(private_key=private_key)
    print(f"Generated DID: {agent_did.did}")
    print(f"Public Key: {agent_did.public_key}")
    print("DID created successfully.")

    # 2. Create a DID document
    print("\n2. Creating a DID document...")
    service_endpoints = [
        {
            "id": f"{agent_did.did}#agent-info",
            "type": "AgentProfile",
            "serviceEndpoint": {
                "scopeOfBehavior": ["e-commerce", "product-recommendation"],
                "toolset": [{"name": "web-search", "version": "1.0"}],
            }
        }
    ]
    did_document = agent_did.create_did_document(service_endpoints)
    print("Generated DID Document:")
    print(json.dumps(did_document, indent=2))
    print("DID document created successfully.")

    # 3. Register the DID and DID document with the AIPN
    print("\n3. Registering the DID and DID document with the AIPN...")
    aipn_contract = AIPNContract(network_config)

    print(f"  Calling registerDID({agent_did.did}, {json.dumps(did_document)})")
    success = aipn_contract.register_did(agent_did.did, json.dumps(did_document))
    if success:
        print("  DID registration successful.")
    else:
        print("  DID registration failed.")

    # 4. Resolve DID
    print("\n4. Resolving DID...")
    print(f"  Calling resolveDID({agent_did.did})")
    resolved_did_document = aipn_contract.resolve_did(agent_did.did)

    if resolved_did_document:
        print(f"  Resolved DID Document: {json.dumps(resolved_did_document, indent=2)}")
        print("  DID resolved successfully.")
    else:
        print(f"  Could not resolve DID: {agent_did.did}")

    # 5. Create a Verifiable Credential
    print("\n5. Creating a Verifiable Credential...")
    issuer_private_key = os.environ.get("ISSUER_PRIVATE_KEY")
    if not issuer_private_key:
        raise ValueError("ISSUER_PRIVATE_KEY environment variable not set.")
    issuer_account = Account.from_key(issuer_private_key)
    issuer_address = issuer_account.address
    issuer_did = DID(private_key=issuer_private_key)

    vc = provider.create_verifiable_credential(
        issuer_did=issuer_did.did,
        subject_did=agent_did.did,
        claims={
            "certification": "Certified AI Agent",
            "compliance": "GDPR"
        }
    )
    print("  Verifiable Credential created.")

    # 6. Sign the credential
    print("\n6. Signing the credential...")
    signature = aipn_contract.sign_message(json.dumps(vc.to_json()), issuer_private_key)
    vc.proof = {
        "type": "EcdsaSecp256k1Signature2019",
        "created": "2024-10-27T14:00:00Z",
        "verificationMethod": f"{issuer_did.did}#key1",
        "proofPurpose": "assertionMethod",
        "jws": signature
    }
    print("  Credential signed successfully.")
    print(f"  Verifiable Credential: {json.dumps(vc.to_json(), indent=2)}")

    # 7. Verify the credential
    print("\n7. Verifying the credential...")
    is_valid = aipn_contract.verify_signature(json.dumps(vc.to_json()), signature, issuer_address)
    print(f"  Credential Verification: {'Valid' if is_valid else 'Invalid'}")

    print("\nExamples completed.")