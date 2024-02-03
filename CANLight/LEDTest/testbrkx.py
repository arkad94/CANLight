import time
from rpi_ws281x import PixelStrip, Color

# LED strip configuration
LED_COUNT = 16        # Number of LED pixels (4x4 grid).
LED_PIN = 18          # GPIO pin connected to the pixels (must support PWM).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800kHz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)

# Custom brightness levels
BRIGHTNESS_RED = 20
BRIGHTNESS_AMBER = 255

# Create PixelStrip object with appropriate configuration
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, BRIGHTNESS_AMBER)  # Max brightness for amber
strip.begin()  # Initialize the library

def set_led_color(index, color):
    strip.setPixelColor(index, color)
    strip.show()

def welcome_animation():
    red = Color(255, 0, 0)  # Red color
    amber = Color(255, 165, 0)  # Amber color

    # LEDs to be set to red
    red_leds = [1, 2, 7, 11, 14, 13, 8, 4]
    for i in red_leds:
        set_led_color(i, red)

    # LEDs to be set to amber
    amber_leds = [1, 7, 11, 13, 4, 6, 10, 16]
    for i in amber_leds:
        set_led_color(i, amber)

    # Transition to Part 2
    transition_to_drl()

def transition_to_drl():
    # Continue with the DRL configuration as before
    # ...

try:
    welcome_animation()
    # Keep DRLs on until script is closed
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    # Turn off all the LEDs on Ctrl+C
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
