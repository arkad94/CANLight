import time
from rpi_ws281x import PixelStrip, Color

# LED strip configuration
LED_COUNT = 16        # Number of LED pixels (4x4 grid).
LED_PIN = 18          # GPIO pin connected to the pixels (must support PWM).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800kHz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 25   # Set to a low number for safety.
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)

# Create PixelStrip object with appropriate configuration
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()  # Initialize the library

print('Press Ctrl-C to quit.')
try:
    # Initially set the top and bottom rows to red
    for i in range(4):
        strip.setPixelColor(i, Color(255, 0, 0))  # Top row red
        strip.setPixelColor(15 - i, Color(255, 0, 0))  # Bottom row red
    strip.show()

    while True:
        # Amber animation for the middle rows
        for i in range(4):
            # Middle top row (LEDs 9 to 12 in your setup)
            strip.setPixelColor(8 + i, Color(255, 96, 0))
            # Middle bottom row (LEDs 8 to 5 in your setup, reversed)
            strip.setPixelColor(7 - i, Color(255, 96, 0))

            strip.show()
            time.sleep(0.5)  # Animation speed

        # Turn off only the amber LEDs
        for i in range(4, 12):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(1)

except KeyboardInterrupt:
    # Turn off all the LEDs on Ctrl+C
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
