import { loadFixture } from "@nomicfoundation/hardhat-toolbox/network-helpers";
import { expect } from "chai";
import { ethers } from "hardhat";

describe("Decom", function () {
    async function deployDecomFixture() {
        const [owner, worker, otherAccount] = await ethers.getSigners();
        const Decom = await ethers.getContractFactory("Decom");
        const decom = await Decom.deploy();
        return { decom, owner, worker, otherAccount };
    }

    describe("Deployment", function () {
        it("Should deploy successfully", async function () {
            const { decom } = await loadFixture(deployDecomFixture);
            expect(await decom.getAddress()).to.be.properAddress;
        });
    });

    describe("Bounties", function () {
        it("Should create a bounty", async function () {
            const { decom, owner } = await loadFixture(deployDecomFixture);
            const amount = ethers.parseEther("1.0");

            await expect(decom.createBounty("QmTest123", { value: amount }))
                .to.emit(decom, "BountyCreated")
                .withArgs(0, owner.address, amount, "QmTest123");

            const bounty = await decom.bounties(0);
            expect(bounty.creator).to.equal(owner.address);
            expect(bounty.amount).to.equal(amount);
            expect(bounty.status).to.equal(0); // Pending
        });

        it("Should accept a bid", async function () {
            const { decom, owner, worker } = await loadFixture(deployDecomFixture);
            await decom.createBounty("QmTest123", { value: ethers.parseEther("1.0") });

            await expect(decom.acceptBid(0, worker.address))
                .to.emit(decom, "BidAccepted")
                .withArgs(0, worker.address);

            const bounty = await decom.bounties(0);
            expect(bounty.assignedWorker).to.equal(worker.address);
            expect(bounty.status).to.equal(1); // Active
        });
    });
});
