# Setup and Testing Guide

## Current Status (Phases 1-3)
The core logic for the Decentralized Compute Network is implemented, including:
- **CLI**: Bounty management, bidding, worker control.
- **Coordinator**: In-memory bounty and bid management.
- **Worker**: RestrictedPython executor.
- **Storage**: IPFS integration (with mock fallback).
- **Marketplace**: Bidding, pricing, and consensus logic.

## Prerequisites
For the current MVP state, **no external services are strictly required** to run the basic tests and CLI commands. The system includes fallbacks:
- **Database**: Uses in-memory storage for bounties and bids.
- **IPFS**: Falls back to mock CIDs if no IPFS node is found.
- **Wallet**: Uses in-memory balance tracking.

### Optional (For "Real" Mode)
To test with actual external services:
1. **IPFS**: Install and start an IPFS daemon (`ipfs daemon`).
2. **PostgreSQL**: Required only when we switch `bounty_manager.py` to use SQLAlchemy (currently in-memory).

## Running Tests
Run the end-to-end integration workflow:
```bash
python -m decom.tests.integration.test_workflow
```
Expected output: `Workflow test passed!`

## Using the CLI
The CLI is the main entry point. Ensure you are in the project root (`c:/Development/projects/Distributed-systems`).

### 1. Help
```bash
python -m decom.cli.main --help
```

### 2. Bounty Management
```bash
# List bounties
python -m decom.cli.main bounty list

# Raise a bounty (mock)
python -m decom.cli.main bounty raise my_script.py --budget 100
```

### 3. Worker
```bash
# Check worker status
python -m decom.cli.main worker status
```

## Next Steps (Phase 4)
Before moving to Blockchain integration, ensure:
1. You can run the workflow test successfully.
2. You understand that data is currently **ephemeral** (lost on restart).
