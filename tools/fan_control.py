from smolagents import Tool
import requests

class FanControlTool(Tool):
    name = "fan_control"
    description = "Controls the state of a smart fan (on or off) via OpenHAB REST API."
    inputs = {
        "action": {
            "type": "string",
            "description": "Action to perform on the fan. Can be 'on' or 'off'."
        }
    }
    output_type = "string"

    def forward(self, action: str) -> str:
        action = action.lower()
        if action not in ['on', 'off']:
            return "Error: Invalid action. Please use 'on' or 'off'."

        url = "http://192.168.188.80:8080/rest/items/Ventilateur"
        try:
            response = requests.post(
                url,
                headers={"Content-Type": "text/plain"},
                data=action.upper(),
                timeout=5
            )
            if response.status_code == 202:
                return f"Fan turned {action}."
            else:
                return f"Failed to turn {action} the fan. Status code: {response.status_code}"
        except requests.RequestException as e:
            return f"Error: {e}"
if __name__ == "__main__":
    tool = FanControlTool()
    print(tool.forward("off"))   # Change "on" to "off" or invalid input to test other cases