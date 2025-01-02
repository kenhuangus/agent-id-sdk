// scripts/deploy.js
const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();

  console.log("Deploying contracts with the account:", deployer.address);

  const AgentIDProviderNetwork = await hre.ethers.getContractFactory("AgentIDProviderNetwork");
  const aipn = await AgentIDProviderNetwork.deploy();

  // Get the deployed address
  const aipnAddress = await aipn.getAddress();
  console.log("AgentIDProviderNetwork deployed to:", aipnAddress);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });