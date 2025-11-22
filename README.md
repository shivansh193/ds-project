# Decentralized Compute Network (DeCom)

A CLI-based distributed computing marketplace where users can post compute tasks with bounties, workers can bid and execute them, with IPFS for code storage and built-in verification mechanisms.

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

## Usage

### Coordinator
Start the coordinator server:
```bash
uvicorn decom.core.coordinator.server:app --reload
```

### Worker
Start a worker node:
```bash
decom start-worker
```

### CLI
Raise a bounty:
```bash
decom raise-bounty my_script.py --budget 100
```
