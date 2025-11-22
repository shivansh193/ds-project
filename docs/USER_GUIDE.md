# Decentralized Compute Network - User Guide

This guide covers everything from setting up the project to running a full compute lifecycle.

## 1. Setup & Installation
**Prerequisites:** Python 3.10+

1.  **Navigate to Project Root:**
    ```powershell
    cd c:\Development\projects\Distributed-systems\decom
    ```
2.  **Install Dependencies:**
    ```powershell
    pip install -r requirements.txt
    ```
3.  **Install Package (Crucial):**
    ```powershell
    pip install -e .
    ```
4.  **Verify Installation:**
    ```powershell
    decom --help
    ```

---

## 2. Worker Operations
If you want to contribute compute power to the network:

**Start a Worker Node:**
```powershell
decom worker start
```

**Check Worker Status:**
```powershell
decom worker status
```

---

## 3. User Operations (Requester)
If you want to get a task executed:

### Step 1: Raise a Bounty
Submit a Python script for execution.
```powershell
# Syntax: decom bounty raise <file_path> --budget <amount>
decom bounty raise scripts/sample_fib.py --budget 50
```

### Step 2: Monitor Bids
Check if workers have bid on your task.
```powershell
decom bid list
```

### Step 3: Accept a Bid
Select the best bid to start execution.
```powershell
# Syntax: decom bid accept <bid_id>
decom bid accept 1
```

---

## 4. Worker Operations (Bidder)
If you are a worker looking for tasks:

### Step 1: Find Bounties
List available tasks.
```powershell
decom bounty list
```

### Step 2: Place a Bid
Offer to do the work for a specific price.
```powershell
# Syntax: decom bid place <bounty_id> <price> <eta_minutes>
decom bid place 1 45 10
```

### Step 3: Check Your Bids
```powershell
decom bid list --mine
```

---

## 5. Quick Start Demo
Run the automated script to see the entire flow in action (Task -> Bid -> Execute -> Verify).
```powershell
python -m decom.scripts.demo_full_flow
```
