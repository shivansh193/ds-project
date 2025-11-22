import os
import shutil
import time
import json
from decom.core.coordinator.bounty_manager import BountyCreate
from decom.core.coordinator.bid_manager import BidManager
from decom.core.worker.executor import Executor
from decom.core.pricing.calculator import PricingCalculator
from decom.core.verification.consensus import ConsensusVerifier

# Setup directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(BASE_DIR, "demo_storage")
WORKER_DIR = os.path.join(BASE_DIR, "demo_worker")

def log(actor, message):
    print(f"[{actor}] {message}")

def demo():
    # Clean up previous runs
    if os.path.exists(STORAGE_DIR): shutil.rmtree(STORAGE_DIR)
    if os.path.exists(WORKER_DIR): shutil.rmtree(WORKER_DIR)
    os.makedirs(STORAGE_DIR, exist_ok=True)
    os.makedirs(WORKER_DIR, exist_ok=True)

    log("SYSTEM", "Starting End-to-End Demo with Local Storage")

    # 1. Create Sample Task
    task_filename = "sample_calc.py"
    task_file_path = os.path.join(BASE_DIR, task_filename)
    with open(task_file_path, "w") as f:
        f.write("""
# Simple Calculation Task
a = 10
b = 20
result = a * b
""")
    log("USER", f"Created sample task: {task_file_path}")

    # 2. 'Upload' to Storage (Mock IPFS)
    # In a real scenario, this returns a CID. Here we use the filename as CID.
    cid = task_filename
    stored_path = os.path.join(STORAGE_DIR, cid)
    shutil.copy(task_file_path, stored_path)
    log("STORAGE", f"File uploaded to simulated IPFS: {stored_path}")

    # 3. Raise Bounty
    bounty_data = BountyCreate(file_path=cid, budget=50.0)
    log("COORDINATOR", f"Bounty raised for CID: {cid} with budget {bounty_data.budget}")

    # 4. Worker Analysis & Bid
    # Worker downloads code to analyze
    worker_download_path = os.path.join(WORKER_DIR, cid)
    shutil.copy(stored_path, worker_download_path)
    log("WORKER", f"Downloaded code for analysis to {worker_download_path}")

    with open(worker_download_path, "r") as f:
        code_content = f.read()

    calculator = PricingCalculator()
    cost_est = calculator.estimate_cost(code_content)
    log("WORKER", f"Estimated cost: {cost_est['estimated_cost']:.4f}")

    bid_manager = BidManager()
    bid = bid_manager.place_bid("bounty_1", "worker_node_1", 45.0, 1) # Bid slightly under budget
    log("WORKER", f"Placed bid: {bid.price}")

    # 5. Coordinator Accepts Bid
    accepted_bid = bid_manager.accept_bid(bid.id)
    if accepted_bid:
        log("COORDINATOR", f"Accepted bid from {accepted_bid.worker_id}")
    else:
        log("COORDINATOR", "Failed to accept bid")
        return

    # 6. Worker Execution
    log("WORKER", "Starting execution...")
    executor = Executor()
    # In reality, worker decrypts here. We skip encryption for this simple demo.
    exec_result = executor.execute(code_content)
    log("WORKER", f"Execution finished. Result: {exec_result}")

    if exec_result["status"] == "error":
        log("WORKER", f"Execution failed: {exec_result.get('error')}")
        return

    # 7. Submit & Verify
    # Worker submits result
    submission = {
        "worker_id": accepted_bid.worker_id,
        "output": exec_result["output"],
        "status": exec_result["status"]
    }
    log("WORKER", f"Submitted result: {submission}")

    # Coordinator Verifies
    verifier = ConsensusVerifier(threshold=0.5) # Lower threshold for single worker demo
    verification = verifier.verify_results([submission])
    
    log("COORDINATOR", f"Verification Result: {verification}")

    log("SYSTEM", "Demo Completed")

if __name__ == "__main__":
    demo()
