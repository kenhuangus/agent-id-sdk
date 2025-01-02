
# Agentic AI SDK: Decentralized Identifiers and Zero-Knowledge Proofs

This repository contains the Agentic AI SDK, a Python-based toolkit for building agentic applications that leverage decentralized identifiers (DIDs) and zero-knowledge proofs (ZKPs) for enhanced security, privacy, and interoperability. This SDK implements the concepts and architecture outlined in the research paper:

> **Agentic AI: Securing Interactions in Multi-Agent Systems through Decentralized Identifiers and Zero-Knowledge Proofs**

## Research Paper Summary

The paper proposes a novel framework for assigning unique, verifiable, and privacy-preserving identities (IDs) to AI agents, particularly within the context of multi-agent systems (MAS). It argues that decentralized identifiers (DIDs) and zero-knowledge proofs (ZKPs) are essential for mitigating risks associated with malicious or malfunctioning agents, enabling secure interactions, and building trust in complex multi-agent environments.

**Key Concepts:**

*   **Agent Instance:** A specific instantiation of an agent's software, model, state, memory, and interaction history.
*   **Decentralized Identifiers (DIDs):** Globally unique, cryptographically verifiable identifiers that are not tied to any centralized authority.
*   **DID Document:** A document associated with a DID, containing public keys, service endpoints, and other relevant information about the agent, including its capabilities, behavior, and operational parameters.
*   **Zero-Knowledge Proofs (ZKPs):** Cryptographic protocols that allow an agent to prove a statement is true without revealing any information beyond the statement's validity.
*   **Agent ID Provider Network (AIPN):** A proposed decentralized network for managing agent DIDs and associated data.
*   **Verifiable Credentials (VCs):** Digitally signed statements that certify an agent's attributes or capabilities, issued by trusted authorities.

**Motivation:**

The increasing prevalence of AI agents, especially in MAS, necessitates robust mechanisms for ensuring their safety and security. Traditional identity management systems are often centralized and lack the flexibility and privacy features needed for dynamic, decentralized agent interactions. This research addresses these challenges by proposing a DID-based framework that enhances:

*   **Accountability:** Tracing actions back to specific agents.
*   **Trust:** Assessing the trustworthiness of agents before interacting with them.
*   **Security:** Implementing fine-grained access control and secure communication.
*   **Privacy:** Enabling agents to selectively disclose information using ZKPs.

**Applications:**

The paper explores the applications of Agent IDs in various areas, including:

*   **Incident Response:** Real-time identification of agents involved in security events, facilitating efficient tracking and remediation.
*   **Threat Detection:** Precise identification of malicious or compromised agents, improving system-wide threat monitoring.
*   **Identity and Access Management:** Implementing fine-grained access control policies and preventing unauthorized access.
*   **Multi-Agent Systems:** Enabling secure communication, coordination, and conflict resolution in MAS.

## Code Structure

The Agent SDK is organized as follows:

```
agent_sdk_project/
├── agent_sdk/
│   ├── __init__.py
│   ├── agent_id_provider.py
│   ├── blockchain.py
│   ├── did.py
│   ├── utils.py
│   └── verifiable_credentials.py
├── scripts/
│   └── deploy.js
├── examples.py
├── hardhat.config.js
├── aipn_contract.sol
├── .gitignore
└── README.md
```

**Key Components:**

*   **`agent_sdk/did.py`:** Defines the `DID` class for creating and managing DIDs.
*   **`agent_sdk/verifiable_credentials.py`:** Implements the `VerifiableCredential` class for creating, signing, and verifying credentials.
*   **`agent_sdk/agent_id_provider.py`:** Defines the `AgentIdProvider` class, responsible for interacting with the AIPN (simulated in the current example).
*   **`agent_sdk/blockchain.py`:** Contains the `AIPNContract` class for interacting with a simulated Ethereum blockchain using `web3.py`.
*   **`agent_sdk/utils.py`:** Provides utility functions for key generation, signing, verification, and other helper functions.
*   **`examples.py`:** Demonstrates how to use the SDK to create DIDs, register them, create and sign VCs, and verify credentials.
*   **`aipn_contract.sol`:** A simple example of a Solidity smart contract for the AIPN.
*   **`scripts/deploy.js`:** A Hardhat deployment script for the `aipn_contract.sol` smart contract.
*   **`hardhat.config.js`:** Hardhat configuration file.

## Getting Started

**Prerequisites:**

*   **Node.js and npm:** Install from [https://nodejs.org/](https://nodejs.org/)
*   **Python 3.7+:** Install from [https://www.python.org/](https://www.python.org/)
*   **Hardhat:** A development environment for Ethereum smart contracts.

**Steps:**

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/kenhuangus/agent-id-sdk.git
    cd agent-id-sdk
    ```

2. **Install Dependencies:**
    ```bash
    npm install --save-dev @nomicfoundation/hardhat-toolbox @openzeppelin/contracts
    pip install web3 cryptography eth-account base58 base64
    ```

3. **Compile and Deploy the Smart Contract:**
    ```bash
    npx hardhat compile
    npx hardhat run scripts/deploy.js --network hardhat
    ```
    *   **Important:** Copy the deployed contract address from the output.

4. **Update `examples.py`:**
    *   Replace `"0x5FbDB2315678afecb367f032d93F642f64180aa3"` in `examples.py` with your deployed contract address.
    *   Set the `PRIVATE_KEY` and `ISSUER_PRIVATE_KEY` environment variables to valid Ethereum private keys. **For testing only**, you can use the private keys generated by the Hardhat node. **Do not use these keys on a real network or with real funds.**

    **Example (macOS/Linux):**

    ```bash
    export PRIVATE_KEY="<your_agent_private_key>"
    export ISSUER_PRIVATE_KEY="<your_issuer_private_key>"
    ```

5. **Run the Example:**

    ```bash
    python examples.py
    ```

**Expected Output:**

The `examples.py` script will demonstrate the following:

*   Generating a new DID.
*   Creating a DID document.
*   Registering the DID and DID document with the simulated AIPN.
*   Resolving the DID document.
*   Creating a Verifiable Credential.
*   Signing the credential with the issuer's private key.
*   Verifying the credential's signature.

You will see output in the console similar to this (the exact values will be different):

```
Starting examples...

1. Creating a new DID...
Generated DID: did:example:z6Mkr7v5...
Public Key: -----BEGIN PUBLIC KEY-----...
DID created successfully.

2. Creating a DID document...
Generated DID Document:
{
  ...
}
DID document created successfully.

3. Registering the DID and DID document with the AIPN...
  Calling registerDID(did:example:z6Mkr7v5..., { ... }) on contract address: 0x...
  Transaction Hash: 0x...
DID registration successful.

4. Resolving DID...
  Calling resolveDID(did:example:z6Mkr7v5...) on contract address: 0x...
  Resolved DID Document: { ... }
  DID resolved successfully.

5. Creating a Verifiable Credential...
  Verifiable Credential created.

6. Signing the credential...
  Verifiable Credential: { ... }
  Credential signed successfully.

7. Verifying the credential...
  Credential Verification: Valid

Examples completed.
```

## Security Considerations

*   **Key Management:** This example uses placeholder methods for handling private keys. **In a production environment, you must use secure key management solutions such as Hardware Security Modules (HSMs), secure enclaves, or specialized key management services.** Never store private keys directly in code or configuration files that are committed to version control.
*   **Smart Contract Security:** The provided `aipn_contract.sol` is a very basic example and lacks essential security features like access control and proper authentication. Before using it in a production setting, it needs to be thoroughly audited and enhanced by experienced Solidity developers.
*   **Error Handling:** The error handling in the example code is minimal. A production-ready SDK would require more comprehensive error handling and exception management.
*   **Testing:** Thorough testing, including unit tests, integration tests, and potentially formal verification, is crucial before deploying any smart contract or SDK code to a live network.

## Future Work

This project serves as a starting point for developing a robust and secure identity framework for agentic AI systems. Future research and development directions include:

*   **Formalizing Interaction Protocols:** Defining message formats, interaction sequences, and security requirements for various use cases.
*   **Scalability and Performance:** Optimizing DID resolution, ZKP generation and verification, and other cryptographic operations for large-scale deployments.
*   **Agent SDK Development:** Building user-friendly and robust SDKs for various agent frameworks and programming languages.
*   **Incentive Mechanisms:** Designing effective mechanisms to encourage participation and honest behavior in the decentralized ID ecosystem.
*   **Privacy-Enhancing Technologies:** Exploring and integrating more efficient ZKP schemes and other privacy-enhancing technologies.
*   **Interoperability and Standardization:** Contributing to the development of common ontologies and standards for agent properties and DID Documents.
*   **Ethical Considerations and Governance:** Addressing potential biases, impacts on agent autonomy, and developing appropriate governance frameworks.
*   **Real-World Pilots and Deployments:** Conducting real-world pilots to validate the architecture and identify practical challenges.
*   **Integration with AI Safety Frameworks:** Exploring how Agent IDs can be integrated with broader AI safety frameworks.
*   **Legal and Regulatory Frameworks:** Researching the legal and regulatory implications of decentralized agent identities.

## Contributing

Contributions to this project are welcome! Please feel free to open issues, submit pull requests, or contact the authors to discuss ideas and improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. (You'll need to create a LICENSE file and choose an appropriate license).

## Acknowledgements
This project is based on research from the paper "Agentic AI: Securing Interactions in Multi-Agent Systems through Decentralized Identifiers and Zero-Knowledge Proofs" and builds upon concepts and technologies from the decentralized identity and blockchain communities, including:
* [Decentralized Identifiers (DIDs) v1.0](https://www.w3.org/TR/did-core/)
* [Verifiable Credentials Data Model 1.0](https://www.w3.org/TR/vc-data-model/)
* [Web3.py](https://web3py.readthedocs.io/)
* [eth-account](https://eth-account.readthedocs.io/)
* [Hardhat](https://hardhat.org/)

## Disclaimer

This project is for research and demonstration purposes. It is not intended for production use without significant modification, security auditing, and thorough testing. The authors are not responsible for any issues or damages arising from the use of this code. Use it at your own risk.
