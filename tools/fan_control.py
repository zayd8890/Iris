from smolagents import Tool

class FanControlTool(Tool):
    name = "fan_control"
    description = "Controls the state of a smart fan (on or off)."
    inputs = {
        "action": {
            "type": "string",
            "description": "Action to perform on the fan. Can be 'on' or 'off'."
        }
    }
    output_type = "string"

    def forward(self, action: str) -> str:
        action = action.lower()
        if action == 'on':
            print("I turned on the fan.")
            return "Fan turned on."
        elif action == 'off':
            print("I turned off the fan.")
            return "Fan turned off."
        else:
            return "Error: Invalid action. Please use 'on' or 'off'."
