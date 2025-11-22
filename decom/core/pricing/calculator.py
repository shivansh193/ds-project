import ast

class PricingCalculator:
    def __init__(self, base_rate_cpu: float = 0.001, base_rate_memory: float = 0.0001):
        self.base_rate_cpu = base_rate_cpu
        self.base_rate_memory = base_rate_memory

    def analyze_code(self, code: str) -> dict:
        """Static analysis of Python code to estimate complexity."""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return {"error": "Invalid Python code"}

        loc = len(code.splitlines())
        loops = 0
        functions = 0
        imports = 0

        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                loops += 1
            elif isinstance(node, ast.FunctionDef):
                functions += 1
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                imports += 1

        return {
            "loc": loc,
            "loops": loops,
            "functions": functions,
            "imports": imports,
            "complexity_score": loc + (loops * 5) + (functions * 2)
        }

    def estimate_cost(self, code: str) -> dict:
        """Estimate execution cost based on code analysis."""
        analysis = self.analyze_code(code)
        if "error" in analysis:
            return analysis

        complexity = analysis["complexity_score"]
        
        # Rough estimation logic
        estimated_cpu_time = complexity * 0.01  # seconds
        estimated_memory = 50 + (analysis["imports"] * 10)  # MB

        cost = (estimated_cpu_time * self.base_rate_cpu) + (estimated_memory * self.base_rate_memory)
        
        return {
            "analysis": analysis,
            "estimated_cpu_time": estimated_cpu_time,
            "estimated_memory_mb": estimated_memory,
            "estimated_cost": max(cost, 0.01) # Minimum cost
        }
