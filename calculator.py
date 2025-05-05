from smolagents import Tool

class CalculatorTool(Tool):
    name = "calculator"
    description = "Performs basic arithmetic operations."
    inputs = {
        "expression": {
            "type": "string",
            "description": "Arithmetic expression to evaluate."
        }
    }
    output_type = "string"

    def forward(self, expression: str) -> str:
        try:
            result = eval(expression)
            return str(result)
        except Exception as e:
            return f"Error: {e}"
