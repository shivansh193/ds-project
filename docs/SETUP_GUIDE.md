# Decentralized Compute Network - Setup & Testing Guide

## Project Structure
The project follows a standard Python package layout:
```
decom/                  # Project Root
├── setup.py           # Package installation script
├── requirements.txt   # Dependencies
├── decom/             # Source Code Package
│   ├── __init__.py
│   ├── cli/           # CLI Commands
│   ├── core/          # Core Logic (Coordinator, Worker, etc.)
│   └── ...
└── ...
```

## 1. Installation
**Step 1:** Navigate to the project root directory.
```powershell
cd c:\Development\projects\Distributed-systems\decom
```

**Step 2:** Install dependencies and the package in editable mode.
```powershell
pip install -r requirements.txt
pip install -e .
```
*Note: The `-e .` is crucial. It tells pip to install the current directory as the `decom` package.*

## 2. Verification
**Step 1:** Verify the CLI is installed and working.
```powershell
decom --help
```
*You should see the help menu with commands like `bounty`, `bid`, `worker`, etc.*

**Step 2:** Run the End-to-End Demo.
This script simulates a full workflow (Task Creation -> Upload -> Bid -> Execution -> Verification) using local storage.
```powershell
python -m decom.scripts.demo_full_flow
```
*Expected Output:*
```
[SYSTEM] Starting End-to-End Demo with Local Storage
...
[COORDINATOR] Verification Result: {'status': 'verified', ...}
[SYSTEM] Demo Completed
```

## 3. Manual CLI Usage
You can also interact with the system manually via the CLI.

**Start a Worker:**
```powershell
decom worker start
```

**Check Worker Status:**
```powershell
decom worker status
```

**Create a Wallet:**
```powershell
decom wallet create
```

## Troubleshooting
- **ModuleNotFoundError: No module named 'decom'**:
  - Ensure you ran `pip install -e .` from the project root.
  - Ensure you are running python commands from the project root (`c:\Development\projects\Distributed-systems\decom`).
- **Command not found 'decom'**:
  - Ensure your Python Scripts directory is in your system PATH.
  - Alternatively, use `python -m decom.cli.main` instead of `decom`.
