from smolagents import Tool

class LightControlTool(Tool):
    name = "light_control"
    description = "Controls the state of a smart light (on or off)."
    inputs = {
        "action": {
            "type": "string",
            "description": "Action to perform on the light. Can be 'on' or 'off'."
        }
    }
    output_type = "string"

    def forward(self, action: str) -> str:
        action = action.lower()
        if action == 'on':
            print("I turned on the light.")
            return "Light turned on."
        elif action == 'off':
            print("I turned off the light.")
            return "Light turned off."
        else:
            return "Error: Invalid action. Please use 'on' or 'off'."
