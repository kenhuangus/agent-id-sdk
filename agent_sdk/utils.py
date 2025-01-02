
import uuid
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

import base58
import base64

def encode_public_key_to_multibase(public_key_pem: str) -> str:
    """Encodes a public key in PEM format to Base58."""
    # Remove the header and footer lines from the PEM string
    pem_lines = public_key_pem.split('\n')
    base64_encoded = ''.join(pem_lines[1:-1])  # Join the lines without the header and footer

    # Decode the Base64 string to bytes
    public_key_bytes = base64.b64decode(base64_encoded)

    # Encode the public key bytes to Base58
    multibase_encoded = base58.b58encode(public_key_bytes).decode('utf-8')

    return multibase_encoded

def generate_key_pair():
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_pem.decode('utf-8'), public_pem.decode('utf-8')

def sign_data(data: str, private_key_pem: str) -> str:
    private_key = serialization.load_pem_private_key(private_key_pem.encode('utf-8'), password=None)
    if not isinstance(private_key, ec.EllipticCurvePrivateKey):
        raise ValueError("Invalid private key type. Expected ECC private key.")
    
    signature = private_key.sign(
        data.encode('utf-8'),
        ec.ECDSA(hashes.SHA256())
    )
    return signature.hex()

def verify_signature(data: str, signature: str, public_key_pem: str) -> bool:
    public_key = serialization.load_pem_public_key(public_key_pem.encode('utf-8'))

    if not isinstance(public_key, ec.EllipticCurvePublicKey):
        raise ValueError("Invalid public key type. Expected ECC public key.")

    try:
        public_key.verify(
            bytes.fromhex(signature),
            data.encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except InvalidSignature:
        return False

def generate_uuid():
    return str(uuid.uuid4())

def is_valid_did(did_string: str) -> bool:
    parts = did_string.split(":")
    return len(parts) >= 3 and parts[0] == "did"
        