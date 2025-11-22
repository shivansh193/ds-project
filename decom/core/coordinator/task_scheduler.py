from typing import List, Dict
from decom.core.coordinator.bid_manager import Bid

class TaskScheduler:
    def __init__(self):
        self.assignments: Dict[str, List[str]] = {} # bounty_id -> [worker_ids]

    def assign_task(self, bounty_id: str, accepted_bids: List[Bid]):
        """Assign a task to workers based on accepted bids."""
        worker_ids = [bid.worker_id for bid in accepted_bids]
        self.assignments[bounty_id] = worker_ids
        # In a real system, this would trigger the dispatch logic to the worker nodes
        print(f"Assigned bounty {bounty_id} to workers: {worker_ids}")
        return worker_ids

    def get_assignments(self, bounty_id: str) -> List[str]:
        return self.assignments.get(bounty_id, [])

    def reassign_task(self, bounty_id: str, failed_worker_id: str, new_worker_id: str):
        """Reassign a task from a failed worker to a new one."""
        if bounty_id in self.assignments:
            workers = self.assignments[bounty_id]
            if failed_worker_id in workers:
                workers.remove(failed_worker_id)
                workers.append(new_worker_id)
                print(f"Reassigned bounty {bounty_id} from {failed_worker_id} to {new_worker_id}")
