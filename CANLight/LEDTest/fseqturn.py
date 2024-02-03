import time
from rpi_ws281x import PixelStrip, Color

# LED strip configuration
LED_COUNT = 16        # Number of LED pixels (4x4 grid).
LED_PIN = 18          # GPIO pin connected to the pixels (must support PWM).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800kHz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to maximum for visibility.
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)

# Create PixelStrip object with appropriate configuration
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()  # Initialize the library

# Define colors
amber = Color(255, 96, 0)  # Amber color
white = Color(255, 255, 255)  # White color

def set_leds_color(leds, color):
    for i in leds:
        strip.setPixelColor(i, color)
    strip.show()

try:
    while True:
        # Set LEDs 0 and 12 to white
        set_leds_color([0, 12], white)

        # Step 1: Set other specified LEDs to amber
        set_leds_color([4, 8, 5, 9, 6, 10, 7, 11], amber)
        time.sleep(0.5)

        # Step 2: Sequentially turn LEDs white with pauses
        for leds in [[0, 5, 8, 12], [5, 9], [6, 10], [7, 11]]:
            set_leds_color(leds, white)
            time.sleep(0.5)

except KeyboardInterrupt:
    # Turn off all the LEDs on Ctrl+C
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
    print("Script stopped by user.")
