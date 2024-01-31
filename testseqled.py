import time
from rpi_ws281x import PixelStrip, Color

# LED strip configuration:
LED_COUNT = 16        # Number of LED pixels (4x4 grid).
LED_PIN = 18          # GPIO pin connected to the pixels (must support PWM).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800kHz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 128   # Set to a low number for safety.
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)

# Create PixelStrip object with appropriate configuration.
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# Initialize the library (must be called once before other functions).
strip.begin()

print('Press Ctrl-C to quit.')
try:
    while True:
        # Color the top and bottom rows in red.
        for i in range(0, 4):
            strip.setPixelColor(i, Color(255, 0, 0))  # Red color
            strip.setPixelColor(i + 12, Color(255, 0, 0))  # Red color
        
        # Amber animation for the middle rows.
        for i in range(4, 12):
            strip.setPixelColor(i, Color(255, 96, 0))  # Amber color
            strip.setPixelColor(i + 4, Color(255, 96, 0))  # Amber color
            strip.show()
            time.sleep(0.5)  # Adjust the sleep duration for the desired speed
        
        strip.show()
        time.sleep(1)
        
        # Turn all LEDs off.
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(1)

except KeyboardInterrupt:
    # On Ctrl+C, turn off all the LEDs.
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
