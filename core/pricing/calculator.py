import ast
import os

class CostCalculator(ast.NodeVisitor):
    def __init__(self):
        self.complexity_score = 0
        self.loop_weight = 5
        self.conditional_weight = 2
        self.call_weight = 1
        self.base_cost = 0.001  # Base cost per complexity unit

    def visit_For(self, node):
        self.complexity_score += self.loop_weight
        self.generic_visit(node)

    def visit_While(self, node):
        self.complexity_score += self.loop_weight
        self.generic_visit(node)

    def visit_If(self, node):
        self.complexity_score += self.conditional_weight
        self.generic_visit(node)

    def visit_Call(self, node):
        self.complexity_score += self.call_weight
        self.generic_visit(node)

    def calculate(self, file_path: str) -> dict:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "r") as source:
            tree = ast.parse(source.read())
        
        self.complexity_score = 0
        self.visit(tree)
        
        estimated_cost = self.complexity_score * self.base_cost
        
        return {
            "complexity_score": self.complexity_score,
            "estimated_cost": round(estimated_cost, 4),
            "details": {
                "loops_weight": self.loop_weight,
                "conditionals_weight": self.conditional_weight,
                "calls_weight": self.call_weight
            }
        }
