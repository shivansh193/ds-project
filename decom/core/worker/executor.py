import RestrictedPython
from RestrictedPython import compile_restricted, safe_globals

class Executor:
    def __init__(self):
        self.globals = safe_globals.copy()
        self.globals['__builtins__'] = safe_globals

    def execute(self, code: str, input_data: dict = None):
        """Execute Python code in a restricted environment."""
        try:
            byte_code = compile_restricted(code, '<string>', 'exec')
            local_scope = {}
            if input_data:
                local_scope.update(input_data)
            
            exec(byte_code, self.globals, local_scope)
            
            # Assuming the script defines a 'result' variable or function
            result = local_scope.get('result', None)
            return {"status": "success", "output": result}
        except Exception as e:
            return {"status": "error", "error": str(e)}
