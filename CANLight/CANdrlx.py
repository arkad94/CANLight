import time
import can
from rpi_ws281x import PixelStrip, Color

# LED strip configuration
LED_COUNT = 16
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 15
LED_INVERT = False

# CAN configuration
CAN_CHANNEL = 'can0'
ARB_ID_TO_LISTEN = 0x007  # Arbitration ID to trigger the animation

# User input for CAN bitrate
bitrate_options = {1: 500000, 2: 1000000}  # Mapping of user input to bitrate
user_choice = int(input("Enter the CAN bitrate (1 for 500KHz, 2 for 1MHz): "))
CAN_BITRATE = bitrate_options.get(user_choice, 500000)  # Default to 500KHz if invalid input

# Create PixelStrip object
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()

# Function definitions for the LED animations
def welcome_animation():
    white = Color(255, 235, 200)

    # Light up 2-3
    for i in range(1, 3):
        strip.setPixelColor(i, white)
        strip.show()
        time.sleep(0.1)

    # Light up 5,12
    corners = [4, 11]
    for i in corners:
        strip.setPixelColor(i, white)
        strip.show()
        time.sleep(0.1)

    # Light up 14,15
    for i in range(13, 15):
        strip.setPixelColor(i, white)
        strip.show()
        time.sleep(0.1)

    # Light up 9,8
    sequence = [8, 7]
    for i in sequence:
        strip.setPixelColor(i, white)
        strip.show()
        time.sleep(0.1)

    # Blink "X" pattern
    for _ in range(4):  # Blink 4 times
        for i in [0, 6, 10, 12, 3, 5, 9, 15]:
            strip.setPixelColor(i, white)
        strip.show()
        time.sleep(0.25)  # Blink every 0.25 seconds
        for i in [0, 6, 10, 12, 3, 5, 9, 15]:
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(0.25)  # Off for 0.25 seconds

    # Transition to Part 2
    transition_to_drl()

def transition_to_drl():
    white = Color(255, 235, 200)
    # Turn off all LEDs except 1,2,3,4,5,12,13,14,15,16,9,8
    drl_leds = [0, 1, 2, 3, 4, 7, 8, 11, 12, 13, 14, 15]  # Corrected list of LEDs for DRL
    for i in range(LED_COUNT):
        if i in drl_leds:
            strip.setPixelColor(i, white)  # Ensure these LEDs are on
        else:
            strip.setPixelColor(i, Color(0, 0, 0))  # Turn off other LEDs
    strip.show()

# Initialize CAN interface
bus = can.interface.Bus(CAN_CHANNEL, bustype='socketcan', bitrate=CAN_BITRATE)

def receive_can_message():
    while True:
        message = bus.recv()  # Blocking call
        if message.arbitration_id == ARB_ID_TO_LISTEN and message.data[0] == 0x01:
            return True

try:
    # Wait for a specific CAN message to trigger the animation
    if receive_can_message():
        welcome_animation()
        # Keep DRLs on until script is closed
        while True:
            time.sleep(1)

except KeyboardInterrupt:
    # Turn off all LEDs on Ctrl+C
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

except Exception as e:
    print(f"An error occurred: {e}")
