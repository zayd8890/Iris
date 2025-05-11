import RPi.GPIO as GPIO
import time

# Numéros GPIO BCM correspondants à IN1 → IN4
relays = [17, 18, 27, 22]

GPIO.setmode(GPIO.BCM)

# Initialisation des GPIO : tous désactivés (donc HIGH)
for pin in relays:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # désactive relais au démarrage

# Test relais 1 à 4 avec logique inversée (LOW = ON)
for i, pin in enumerate(relays):
    print(f"Activation du Relais {i+1} (GPIO {pin})")
    GPIO.output(pin, GPIO.LOW)   # ACTIVE le relais
    time.sleep(1)
    GPIO.output(pin, GPIO.HIGH)  # DÉSACTIVE le relais
    time.sleep(0.5)

GPIO.cleanup()
