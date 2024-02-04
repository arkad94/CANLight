import time
import can
import threading
from rpi_ws281x import PixelStrip, Color

# LED strip configuration
LED_COUNT = 16
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 15
LED_INVERT = False

tlright_active = False
frontseqright_active = False
thread_stop = False

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



# Define the new animation function with a new name
amber = Color(255, 96, 0)  # Amber color
white_dim = Color(25, 25, 25)  # Dim white color (brightness reduced)

def set_leds_color(leds, color):
    for i in leds:
        strip.setPixelColor(i, color)
    strip.show()

def frontsequentialright():
    global frontseqright_active
   

    while frontseqright_active:
        set_leds_color(range(LED_COUNT), white_dim)
        time.sleep(0.2)
        set_leds_color([0, 7, 8, 15, 6, 9, 5, 10, 4, 11], amber)
        time.sleep(0.2)
        revert_sequences = [[4, 11], [5, 10], [6, 9], [0, 7, 8, 15]]
        for group in revert_sequences:
            set_leds_color(group, white_dim)
            time.sleep(0.2)

        if not frontseqright_active:
            break


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

def tlright():
    global tlright_active
    tlright_active = True

    # Set top and bottom rows to red
    for i in range(4):
        strip.setPixelColor(i, Color(255, 0, 0))  # Top row red
        strip.setPixelColor(15 - i, Color(255, 0, 0))  # Bottom row red
    strip.show()

    while tlright_active:
        # Amber animation for the middle rows
        for i in range(4):
            strip.setPixelColor(8 + i, Color(255, 96, 0))  # Middle top row
            strip.setPixelColor(7 - i, Color(255, 96, 0))  # Middle bottom row

            strip.show()
            time.sleep(0.2)

            # Check the flag after updating each LED
            if not tlright_active:
                break

        # Check the flag after completing one cycle of updates
        if not tlright_active:
            break

        # Turn off only the amber LEDs
        for i in range(4, 12):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(1)


bus = can.interface.Bus(CAN_CHANNEL, bustype='socketcan', bitrate=CAN_BITRATE)

def can_message_thread():
    global tlright_active, thread_stop, frontseqright_active
    while not thread_stop:
        message = bus.recv(1.0)
        if message:
            if message.arbitration_id == 0x007 and message.data == b'\x01\x00\x00\x00\x00':
                welcome_animation()
            elif message.arbitration_id == 0x007 and message.data == b'\x00\x00\x00\x00\x01':
                welcome_tail()
            elif message.arbitration_id == 0x007 and message.data == b'\x00\x00\x00\x00\x00':
                tlright_active = False
                turn_off_leds()
            elif message.arbitration_id == 0x002 and message.data == b'\x00\x00\x00\x00\x01\x01':
                tlright_active = True
            elif message.arbitration_id == 0x001 and message.data == b'\x01\x01\x01\x01\x01':
                tlright_active = False
                handle_brake()
            elif message.arbitration_id == 0x002 and message.data == b'\x01\x01\x00\x00\x00\x00':
                frontseqright_active = True

        if thread_stop:  # Check if the flag is set to stop
            break

can_thread = threading.Thread(target=can_message_thread)
can_thread.start()

# Main loop
try:
    while True:
        if tlright_active:
            tlright()
        elif frontseqright_active:
            frontsequentialright()            
        if thread_stop:  # Check if the flag is set to stop
            break
        time.sleep(0.1)  # Small delay to prevent high CPU usage
except KeyboardInterrupt:
    print("CAN bus shutdown gracefully")
    thread_stop = True  # Set the flag to stop the thread
finally:
    can_thread.join()   # Wait for the thread to finish
    turn_off_leds()
    bus.shutdown()