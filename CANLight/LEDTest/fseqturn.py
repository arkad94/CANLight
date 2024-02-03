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
white_dim = Color(25, 25, 25)  # Dim white color (brightness reduced)

def set_leds_color(leds, color):
    for i in leds:
        strip.setPixelColor(i, color)
    strip.show()

try:
    while True:
        # Initial state: all LEDs are dim white
        set_leds_color(range(LED_COUNT), white_dim)
        time.sleep(0.5)

        # Turn specified LEDs to amber
        set_leds_color([0, 7, 8, 15, 6, 9, 5, 10, 4, 11], amber)
        time.sleep(3)

        # Sequentially revert LEDs back to dim white with pauses
        revert_groups = [[6, 9], [5, 10], [4, 11]]
        for group in revert_groups:
            set_leds_color(group, white_dim)
            time.sleep(5)

except KeyboardInterrupt:
    # Turn off all the LEDs on Ctrl+C
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
    print("Script stopped by user.")
