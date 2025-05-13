from smolagents import Tool
import requests

class LightControlTool(Tool):
    name = "light_control"
    description = "Controls the state of a smart light (on or off) via OpenHAB REST API."
    inputs = {
        "action": {
            "type": "string",
            "description": "Action to perform on the light. Can be 'on' or 'off'."
        }
    }
    output_type = "string"

    def forward(self, action: str) -> str:
        action = action.lower()
        if action not in ['on', 'off']:
            return "Error: Invalid action. Please use 'on' or 'off'."

        url = "http://192.168.188.80:8080/rest/items/Lampe"
        try:
            response = requests.post(
                url,
                headers={"Content-Type": "text/plain"},
                data=action.upper(),
                timeout=5
            )
            if response.status_code == 202:
                return f"Light turned {action}."
            else:
                return f"Failed to turn {action} the light. Status code: {response.status_code}"
        except requests.RequestException as e:
            return f"Error: {e}"
