from smolagents import Tool
import RPi.GPIO as GPIO

class LightControlTool(Tool):
    name = "light_control"
    description = "Contrôle une lumière via un relais connecté au GPIO."
    inputs = {
        "action": {
            "type": "string",
            "description": "Action à effectuer sur la lumière. Peut être 'on' ou 'off'."
        }
    }
    output_type = "string"

    def __init__(self):
        self.relay_pin = 17  # GPIO utilisé pour le relais
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.relay_pin, GPIO.OUT)
        GPIO.output(self.relay_pin, GPIO.HIGH)  # lumière éteinte au démarrage

    def forward(self, action: str) -> str:
        action = action.lower()
        if action == 'on':
            GPIO.output(self.relay_pin, GPIO.LOW)
            return "Lumière allumée."
        elif action == 'off':
            GPIO.output(self.relay_pin, GPIO.HIGH)
            return "Lumière éteinte."
        else:
            return "Erreur : action invalide. Utilisez 'on' ou 'off'."
