# Secure DID Authentication with Verifiable Credentials

## Project Overview

This project demonstrates a secure authentication system using Decentralized Identifiers (DIDs) and Verifiable Credentials (VCs) with Zero-Knowledge Proofs (ZKPs). It implements a client-server architecture to showcase how these technologies can be used to create a privacy-preserving authentication flow.

## Features

- DID generation and management
- Verifiable Credential issuance and verification
- Zero-Knowledge Proof generation and validation
- Secure token exchange (JWT and OAuth)
- Resource access based on verified credentials

## Components

1. **Server (`mock_op.py`)**: A Flask-based OpenID Connect Provider (OP) that handles authentication requests, verifies ZKPs, and issues tokens.

2. **Client (`vc.py`)**: A Python script that simulates a client application, generating DIDs, creating VCs, and authenticating with the server.

## Prerequisites

- Python 3.12+
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/kenhuangus/agent-id-sdk.git
   cd agent-id-sdk
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install flask pyjwt cryptography requests
   ```

## Usage

1. Start the server:
   ```
   python mock_op.py
   ```
   The server will run on `https://localhost:5000`.

2. In a new terminal, run the client:
   ```
   python vc.py
   ```

The client will generate a DID, create a VC, authenticate with the server using ZKP, and receive an OAuth token to access a protected resource.

## The following is an example of output. Your result maybe different ##
### Step 1: Generating DID
DID generated: `did:example:4a9e67cd8acb972da62d39c20bde34fb`

### Step 2: Creating Verifiable Credential
- VC created for subject: `did:example:4a9e67cd8acb972da62d39c20bde34fb`
- VC claims: `{'access': 'Ken'}`

### Step 3: Registering public key with OP
- OP URL: `https://localhost:5000`
- Request data:
  ```
  {
    "did": "did:example:4a9e67cd8acb972da62d39c20bde34fb",
    "public_key": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArbldwS2z3KG0gDlcwHCY\nIdWZrf/bLl1oXXCzFJcvsqD6pUfz6RXqW+DtO11h/F1yBEv+Eiy3wIKoqNyeOghH\nqE1Ut7gV2q06ndflU4TFTRqOOej19/HY2GZyJo9NTRBSNvyLy95LLtwQfA2xFvh7\nUUxoAVgCo7vpdQ4TX/KO5eJeQEL39rwcL5I0huVUB+CgYvySvOUB4Mn3nbl9lJuh\nI6nYP7zP5Y34mh+HhT2i/H51yNZhBdlb0dCuYMdbBMDHL9a1eB0B8/CiqD45pM6n\nQ6X4PV90v7H8ndGYrsGZuIU5b2etksKBVG4O9nynKg5g5av5G50DZBhtQ9W6W/k8\nHwIDAQAB\n-----END PUBLIC KEY-----\n"
  }
  ```
- Response status: 200
- Response body:
  ```
  {
    "message": "Public key registered successfully"
  }
  ```
- Public key registered successfully

### Step 4: Starting authentication with OP
- OP URL: `https://localhost:5000`

#### Step 4.1: Requesting challenge
- Challenge response status: 200
- Challenge response body:
  ```
  {
    "challenge": "7b3ce0c4523086cb0957f4cbd18f327716d212288898a4927b6e550ef15864bc"
  }
  ```

#### Step 4.2: Generating ZKP
- Generating ZKP for challenge: `7b3ce0c4523086cb0957f4cbd18f327716d212288898a4927b6e550ef15864bc`
- ZKP generated: `a08489b867b98cdecfb8...`

#### Step 4.3: Sending authentication request
- Request headers:
  ```
  {
    "X-Challenge": "7b3ce0c4523086cb0957f4cbd18f327716d212288898a4927b6e550ef15864bc"
  }
  ```
- Request data:
  ```
  {
    "did": "did:example:4a9e67cd8acb972da62d39c20bde34fb",
    "zkp": "a08489b867b98cdecfb840a4ffbbc38b7493386802af657c4accf23731c8ef40e502fb5e4ba730402c7f9d5942309f808e27e9a86330701dcf2e9e77dfa2682b5c17d2a2e37364a98fd93e5498ec2a4ffd4557a97d5ba25d86e1d7845869843a3d081676180681c81475a14b02ff903563a2106feee8a3f0e36e8dfc520bd849ada3116cdf672b7b0341493838069332dca5166d9504223622f3dbdeae793536ed2149e6ea2f825659b29f0ff4d9c08b6f58c6adcb984badc9bb0da7503b766e5d7158b89966d0f06410ea51c685bd7aed9d6244e3d39012212735310d8725dc9c93b1311763cb20dfcc315c27a6bbb16d0d449e35c04aa60a80f58c4c638cd5",
    "vc_claims": {
      "access": "Ken"
    }
  }
  ```
- Authentication response status: 200
- Authentication response body:
  ```
  {
    "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXhhbXBsZTo0YTllNjdjZDhhY2I5NzJkYTYyZDM5YzIwYmRlMzRmYiIsInNjb3BlIjoiS2VuIiwiZXhwIjoxNzM2MTM2NzcwfQ.sWTKVajciAit5dYNQ4vL2YC9dM2Vrz0exolw3WS9UFE"
  }
  ```
- Received JWT: `eyJhbGciOiJIUzI1NiIs...`

### Step 5: Exchanging JWT for OAuth token
- Request data:
  ```
  {
    "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXhhbXBsZTo0YTllNjdjZDhhY2I5NzJkYTYyZDM5YzIwYmRlMzRmYiIsInNjb3BlIjoiS2VuIiwiZXhwIjoxNzM2MTM2NzcwfQ.sWTKVajciAit5dYNQ4vL2YC9dM2Vrz0exolw3WS9UFE"
  }
  ```
- Token response status: 200
- Token response body:
  ```
  {
    "access_token": "97ebe64a6b326d3a7433226b267c3dc3",
    "resource": "Ken resource"
  }
  ```

### Step 6: Final Results
- OAuth Token: `97ebe64a6b326d3a7433226b267c3dc3`
- Accessed Resource: `Ken resource`

## Security Considerations

This project implements several security measures, including:

- Secure random number generation
- Challenge-response mechanism to prevent replay attacks
- Short-lived JWTs
- HTTPS communication (using self-signed certificates for demonstration)
- Input validation and error handling

However, for production use, additional security measures should be implemented, such as:

- Proper certificate management
- Secure key storage
- Comprehensive logging and monitoring
- Rate limiting and additional anti-DoS measures


## Disclaimer

This project is for educational purposes and should not be used in production without thorough security audits and enhancements.

## Contributing

Contributions to improve the security, functionality, or documentation of this project are welcome. Please submit a pull request or open an issue to discuss proposed changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
