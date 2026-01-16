import logging
import re
from typing import Dict, Any, Callable

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Calculator:
    """
    A basic calculator that can evaluate simple mathematical expressions safely.
    """
    def __init__(self):
        # Allow only numbers, basic operators, and parentheses
        self.allowed_pattern = re.compile(r'^[0-9+\-*/().\s*%^]+$')

    def calculate(self, expression: str) -> str:
        """
        Evaluates a mathematical expression and returns the result as a string.
        
        Args:
            expression (str): The mathematical expression to evaluate (e.g., "2 + 2").
            
        Returns:
            str: The result of the evaluation or an error message.
        """
        # Clean the expression
        expression = expression.strip()
        
        # Security check: only allow pre-defined characters
        if not self.allowed_pattern.match(expression):
            return "Error: Invalid characters in expression. Only numbers and basic operators (+, -, *, /, %, ^) are allowed."

        try:
            # Replace ^ with ** for Python power operator
            safe_expr = expression.replace('^', '**')
            
            # Use eval carefully with no globals and restricted locals
            # Note: For production use, a proper AST-based parser is recommended.
            result = eval(safe_expr, {"__builtins__": {}}, {})
            return str(result)
        except ZeroDivisionError:
            return "Error: Division by zero."
        except Exception as e:
            logger.error(f"Calculator error evaluating '{expression}': {e}")
            return f"Error: Could not evaluate expression. {e}"

def create_calculator_tool() -> Dict[str, Any]:
    """
    Helper function to create a LangChain-compatible tool for a basic calculator.
    
    Returns:
        Dict[str, Any]: A dictionary containing name, description, and the function.
    """
    calc = Calculator()
    
    def run_calculator(expression: str) -> str:
        return calc.calculate(expression)
        
    return {
        "name": "calculator",
        "description": "A basic calculator for mathematical expressions like '10 + 5' or '(50 * 2) / 10'. Supports +, -, *, /, %, and ^.",
        "func": run_calculator
    }
