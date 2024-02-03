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

def turn_off_leds():
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

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

def welcome_tail():
    deep_red = Color(139, 0, 0)  # Deep red color for the initial sequence
    amber = Color(255, 96, 0)   # Amber color for the "Blink X" pattern    

    # Initial sequence in deep red
    # Light up 2-3
    for i in range(1, 3):
        strip.setPixelColor(i, deep_red)
        strip.show()
        time.sleep(0.1)

    # Light up 5, 12
    corners = [4, 11]
    for i in corners:
        strip.setPixelColor(i, deep_red)
        strip.show()
        time.sleep(0.1)

    # Light up 14, 15
    for i in range(13, 15):
        strip.setPixelColor(i, deep_red)
        strip.show()
        time.sleep(0.1)

    # Light up 9, 8
    sequence = [8, 7]
    for i in sequence:
        strip.setPixelColor(i, deep_red)
        strip.show()
        time.sleep(0.1)

    # Blink "X" pattern in amber
    x_pattern = [0, 6, 10, 12, 3, 5, 9, 15]
    for _ in range(4):  # Blink 4 times
        for i in x_pattern:
            strip.setPixelColor(i, amber)
        strip.show()
        time.sleep(0.25)  # Blink every 0.25 seconds
        for i in x_pattern:
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(0.25)  # Off for 0.25 seconds

    # Transition to tail light
    transition_to_tail()

def transition_to_tail():
    deep_red = Color(139, 0, 0)  # Deep red color for tail light
    for i in range(LED_COUNT):
        if i in [1, 2, 7, 11, 14, 13, 8, 4]:
            strip.setPixelColor(i, deep_red)
        else:
            strip.setPixelColor(i, Color(0, 0, 0))
    strip.setBrightness(15)  # Set brightness to 15 for specified LEDs
    strip.show()

def handle_brake():
    deep_red_max = Color(255, 0, 0)  # Deep red color for brake light
    brake_leds = [0, 5, 10, 15, 3, 6, 9, 12]
    for led in brake_leds:
        strip.setPixelColor(led, deep_red_max)
    strip.setBrightness(255)  # Max brightness for brake LEDs
    strip.show()    


def turn_off_brake_leds():
    for led in [0, 12, 15, 3,]:
        strip.setPixelColor(led, Color(0, 0, 0))
    strip.show()


# Initialize CAN interface
bus = can.interface.Bus(CAN_CHANNEL, bustype='socketcan', bitrate=CAN_BITRATE)

def receive_can_message(bus):
    while True:
        message = bus.recv(7 / 1000)  # Set timeout to 7ms
        if message is None:  # If no message is received within 7ms
            turn_off_brake_leds()
            return "check_again"  # Return a string to indicate to check again
        elif message.arbitration_id == 0x007:
            if message.data == b'\x01\x00\x00\x00\x00':
                return "start_animation"
            elif message.data == b'\x00\x00\x00\x00\x01':
                return "welcome_tail"
            elif message.data == b'\x00\x00\x00\x00\x00':
                return "turn_off"
        elif message.arbitration_id == 0x001:
            if message.data == b'\x01\x01\x01\x01\x01':
                handle_brake()
                return "brake_on"


# Main loop modified to include welcome_tail action
try:
    while True:
        action = receive_can_message(bus)
        if action == "start_animation":
            welcome_animation()
        elif action == "welcome_tail":
            welcome_tail()
        elif action == "turn_off":
            turn_off_leds()
        elif action == "brake_on":
            continue  # Keep the brake lights on, waiting for the next message
        # No action is needed for "check_again"; it simply continues the loop
except KeyboardInterrupt:
    print("CAN bus shutdown gracefully")
finally:
    turn_off_leds()  # Ensure LEDs are turned off
    bus.shutdown()  # Shutdown CAN bus
