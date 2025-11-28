import { ethers } from "hardhat";

async function main() {
    const Decom = await ethers.getContractFactory("Decom");
    const decom = await Decom.deploy();

    await decom.waitForDeployment();

    console.log("Decom deployed to:", await decom.getAddress());
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
