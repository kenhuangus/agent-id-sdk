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
