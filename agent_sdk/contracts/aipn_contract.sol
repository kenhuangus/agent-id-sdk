// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AgentIDProviderNetwork {
    mapping(string => string) public didRegistry;

    event DIDRegistered(string did, string didDocument);
    event DIDUpdated(string did, string didDocument);

    function registerDID(string memory did, string memory didDocument) public {
        require(bytes(didRegistry[did]).length == 0, "DID already registered");
        didRegistry[did] = didDocument;
        emit DIDRegistered(did, didDocument);
    }

    function updateDIDDocument(string memory did, string memory didDocument) public {
        // In a real implementation, you would need to add authentication and authorization here
        // to ensure that only the owner of the DID can update it.
        require(bytes(didRegistry[did]).length > 0, "DID cannot be found");
        didRegistry[did] = didDocument;
        emit DIDUpdated(did, didDocument);
    }

    function resolveDID(string memory did) public view returns (string memory) {
        return didRegistry[did];
    }
}