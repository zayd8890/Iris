from smolagents import Tool

class ThermostatControlTool(Tool):
    name = "thermostat_control"
    description = "Controls the temperature of a smart thermostat."
    inputs = {
        "temperature": {
            "type": "number",
            "description": "The temperature to set the thermostat to in Celsius."
        }
    }
    output_type = "string"

    def forward(self, temperature: float) -> str:
        if temperature < -10 or temperature > 40:
            return "Error: Invalid temperature range. Please set a temperature between -10 and 40 °C."
        else:
            print(f"I set the thermostat to {temperature}°C.")
            return f"Thermostat set to {temperature}°C."
