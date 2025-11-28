// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract Decom {
    enum BountyStatus { Pending, Active, Completed, Cancelled }

    struct Bounty {
        uint256 id;
        address creator;
        string ipfsCid;
        uint256 amount;
        BountyStatus status;
        address assignedWorker;
        string resultHash;
    }

    uint256 private _nextBountyId;
    mapping(uint256 => Bounty) public bounties;

    event BountyCreated(uint256 indexed id, address indexed creator, uint256 amount, string ipfsCid);
    event BidAccepted(uint256 indexed id, address indexed worker);
    event ResultSubmitted(uint256 indexed id, string resultHash);
    event BountyCompleted(uint256 indexed id, address indexed worker, uint256 amount);
    event BountyCancelled(uint256 indexed id);

    function createBounty(string memory ipfsCid) external payable {
        require(msg.value > 0, "Bounty amount must be greater than 0");

        uint256 bountyId = _nextBountyId++;
        bounties[bountyId] = Bounty({
            id: bountyId,
            creator: msg.sender,
            ipfsCid: ipfsCid,
            amount: msg.value,
            status: BountyStatus.Pending,
            assignedWorker: address(0),
            resultHash: ""
        });

        emit BountyCreated(bountyId, msg.sender, msg.value, ipfsCid);
    }

    function acceptBid(uint256 bountyId, address worker) external {
        Bounty storage bounty = bounties[bountyId];
        require(msg.sender == bounty.creator, "Only creator can accept bids");
        require(bounty.status == BountyStatus.Pending, "Bounty not pending");

        bounty.assignedWorker = worker;
        bounty.status = BountyStatus.Active;
        emit BidAccepted(bountyId, worker);
    }

    function submitResult(uint256 bountyId, string memory resultHash) external {
        Bounty storage bounty = bounties[bountyId];
        require(msg.sender == bounty.assignedWorker, "Only assigned worker can submit");
        require(bounty.status == BountyStatus.Active, "Bounty not active");

        bounty.resultHash = resultHash;
        emit ResultSubmitted(bountyId, resultHash);
    }

    function verifyAndRelease(uint256 bountyId, bool success) external {
        Bounty storage bounty = bounties[bountyId];
        require(msg.sender == bounty.creator, "Only creator can verify");
        require(bounty.status == BountyStatus.Active, "Bounty not active");

        if (success) {
            bounty.status = BountyStatus.Completed;
            payable(bounty.assignedWorker).transfer(bounty.amount);
            emit BountyCompleted(bountyId, bounty.assignedWorker, bounty.amount);
        } else {
            // In a real system, this might go to dispute or re-open
            // For MVP, we just reset to Pending or keep Active? 
            // Let's say we cancel/refund for now if verification fails completely
            bounty.status = BountyStatus.Cancelled;
            payable(bounty.creator).transfer(bounty.amount);
            emit BountyCancelled(bountyId);
        }
    }

    function cancelBounty(uint256 bountyId) external {
        Bounty storage bounty = bounties[bountyId];
        require(msg.sender == bounty.creator, "Only creator can cancel");
        require(bounty.status == BountyStatus.Pending, "Cannot cancel active bounty");

        bounty.status = BountyStatus.Cancelled;
        payable(bounty.creator).transfer(bounty.amount);
        emit BountyCancelled(bountyId);
    }
}
