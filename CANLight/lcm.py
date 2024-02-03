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

def welcome_animation():
    white = Color(255, 235, 200)

    for i in range(1, 3):
        strip.setPixelColor(i, white)
        strip.show()
        time.sleep(0.1)

    corners = [4, 11]
    for i in corners:
        strip.setPixelColor(i, white)
        strip.show()
        time.sleep(0.1)

    for i in range(13, 15):
        strip.setPixelColor(i, white)
        strip.show()
        time.sleep(0.1)

    sequence = [8, 7]
    for i in sequence:
        strip.setPixelColor(i, white)
        strip.show()
        time.sleep(0.1)

    for _ in range(4):
        for i in [0, 6, 10, 12, 3, 5, 9, 15]:
            strip.setPixelColor(i, white)
        strip.show()
        time.sleep(0.25)
        for i in [0, 6, 10, 12, 3, 5, 9, 15]:
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(0.25)

    transition_to_drl()

def transition_to_drl():
    white = Color(255, 235, 200)
    drl_leds = [0, 1, 2, 3, 4, 7, 8, 11, 12, 13, 14, 15]
    for i in range(LED_COUNT):
        if i in drl_leds:
            strip.setPixelColor(i, white)
        else:
            strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def welcome_tail():
    deep_red = Color(139, 0, 0)
    amber = Color(255, 96, 0)

    for i in range(1, 3):
        strip.setPixelColor(i, deep_red)
        strip.show()
        time.sleep(0.1)

    corners = [4, 11]
    for i in corners:
        strip.setPixelColor(i, deep_red)
        strip.show()
        time.sleep(0.1)

    for i in range(13, 15):
        strip.setPixelColor(i, deep_red)
        strip.show()
        time.sleep(0.1)

    sequence = [8, 7]
    for i in sequence:
        strip.setPixelColor(i, deep_red)
        strip.show()
        time.sleep(0.1)

    x_pattern = [0, 6, 10, 12, 3, 5, 9, 15]
    for _ in range(4):
        for i in x_pattern:
            strip.setPixelColor(i, amber)
        strip.show()
        time.sleep(0.25)
        for i in x_pattern:
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(0.25)

    transition_to_tail()

def transition_to_tail():
    deep_red = Color(139, 0, 0)
    for i in range(LED_COUNT):
        if i in [1, 2, 7, 11, 14, 13, 8, 4]:
            strip.setPixelColor(i, deep_red)
        else:
            strip.setPixelColor(i, Color(0, 0, 0))
    strip.setBrightness(15)
    strip.show()

def handle_brake():
    deep_red_max = Color(255, 0, 0)
    brake_leds = [5, 6, 9, 10]
    for led in brake_leds:
        strip.setPixelColor(led, deep_red_max)
    strip.setBrightness(255)
    strip.show()

def turn_off_brake_leds():
    for led in [5, 6, 9, 10]:
        strip.setPixelColor(led, Color(0, 0, 0))
    strip.show()

def amber_red_animation():
    try:
        for i in range(4):
            strip.setPixelColor(i, Color(255, 0, 0))
            strip.setPixelColor(15 - i, Color(255, 0, 0))
        strip.show()

        while True:
            for i in range(4):
                strip.setPixelColor(8 + i, Color(255, 96, 0))
                strip.setPixelColor(7 - i, Color(255, 96, 0))

                strip.show()
                time.sleep(0.2)

            for i in range(4, 12):
                strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Animation interrupted")

bus = can.interface.Bus(CAN_CHANNEL, bustype='socketcan', bitrate=CAN_BITRATE)

def receive_can_message(bus):
    while True:
        message = bus.recv(7 / 1000)
        if message is None:
            turn_off_brake_leds()
            return "check_again"
        elif message.arbitration_id == 0x007:
            if message.data == b'\x01\x00\x00\x00\x00':
                return "start_animation"
            elif message.data == b'\x00\x00\x00\x00\x01':
                return "welcome_tail"
            elif message.data == b'\x00\x00\x00\x00\x00':
                return "turn_off"
        elif message.arbitration_id == 0x002:
            if message.data == b'\x00\x00\x00\x00\x01\x01':
                return "amber_red_animation"
        elif message.arbitration_id == 0x001:
            if message.data == b'\x01\x01\x01\x01\x01':
                handle_brake()
                return "brake_on"

try:
    while True:
        action = receive_can_message(bus)
        if action == "start_animation":
            welcome_animation()
        elif action == "welcome_tail":
            welcome_tail()
        elif action == "amber_red_animation":
            amber_red_animation()
        elif action == "turn_off":
            turn_off_leds()
        elif action == "brake_on":
            continue
except KeyboardInterrupt:
    print("CAN bus shutdown gracefully")
finally:
    turn_off_leds()
    bus.shutdown()
