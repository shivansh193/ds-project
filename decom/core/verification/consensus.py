from typing import List, Any, Dict
from collections import Counter

class ConsensusVerifier:
    def __init__(self, threshold: float = 0.66):
        self.threshold = threshold

    def verify_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Verify results using majority consensus.
        results: List of dicts, e.g., [{'worker_id': 'w1', 'output': '123'}, ...]
        """
        if not results:
            return {"status": "failed", "reason": "No results submitted"}

        total_workers = len(results)
        # Extract outputs to compare
        outputs = [str(r['output']) for r in results]
        
        # Count occurrences of each output
        counts = Counter(outputs)
        most_common_output, count = counts.most_common(1)[0]
        
        consensus_ratio = count / total_workers
        
        if consensus_ratio >= self.threshold:
            return {
                "status": "verified",
                "consensus_output": most_common_output,
                "confidence": consensus_ratio,
                "matching_workers": [r['worker_id'] for r in results if str(r['output']) == most_common_output]
            }
        else:
            return {
                "status": "disputed",
                "reason": "Consensus threshold not met",
                "confidence": consensus_ratio,
                "details": dict(counts)
            }
