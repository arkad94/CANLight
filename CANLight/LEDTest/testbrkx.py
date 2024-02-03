import time
from rpi_ws281x import PixelStrip, Color

# LED strip configuration
LED_COUNT = 16        # Number of LED pixels (4x4 grid).
LED_PIN = 18          # GPIO pin connected to the pixels (must support PWM).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800kHz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 15   # Set to a low number for safety.
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)

# Create PixelStrip object with appropriate configuration
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()  # Initialize the library

def welcome_animation():
    deep_red = Color(139, 0, 0)  # Deep red color for tail light
    amber = Color(255, 191, 0)   # Amber color

    # Tail light sequence
    tail_sequence = [1, 2, 7, 11, 14, 13, 8, 4]

    # Light up LEDs in the specified tail light sequence
    for i in tail_sequence:
        strip.setPixelColor(i, deep_red)
        strip.show()
        time.sleep(0.1)

    # Light up remaining LEDs in amber
    for i in range(LED_COUNT):
        if i not in tail_sequence:
            strip.setPixelColor(i, amber)
            strip.show()
            time.sleep(0.1)

    # Blink "X" pattern
    for _ in range(4):  # Blink 4 times
        for i in range(LED_COUNT):
            strip.setPixelColor(i, deep_red if i in tail_sequence else amber)
        strip.show()
        time.sleep(0.25)  # Blink every 0.25 seconds
        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(0.25)  # Off for 0.25 seconds

    # Transition to tail light
    transition_to_tail()

def transition_to_tail():
    deep_red = Color(139, 0, 0)  # Deep red color for tail light
    amber = Color(255, 191, 0)   # Amber color

    # Turn on specific LEDs in deep red and amber
    for i in range(LED_COUNT):
        strip.setPixelColor(i, deep_red if i in [1, 2, 7, 11, 14, 13, 8, 4] else amber)
    strip.show()

try:
    welcome_animation()
    # Keep tail lights on until script is closed
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    # Turn off all the LEDs on Ctrl+C
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

