from rpi_ws281x import *
import time

# LED strip configuration:
LED_COUNT = 16      # Number of LED pixels.
LED_PIN = 18        # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10         # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255 # Set to 0 for darkest and 255 for brightest
LED_INVERT = False   # True to invert the signal (when using NPN transistor level shift)

# Define the brightness values for red
R1 = 20   # Lower brightness for static part
R2 = 255  # Full brightness for dynamic part

# Define colors with respective brightness:
RED_LOW = Color(R1, 0, 0)    # Red with lower brightness (R1)
RED_HIGH = Color(R2, 0, 0)   # Red with full brightness (R2)
OFF = Color(0, 0, 0)

# Helper function to set color for a single pixel
def setPixelColor(strip, pixel, color):
    strip.setPixelColor(pixel, color)

# Helper function to set color for multiple pixels
def setMultiplePixels(strip, pixels, color):
    for pixel in pixels:
        setPixelColor(strip, pixel, color)

# Initialize the library (must be called once before other functions).
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()

try:
    while True:
        # Static part with lower brightness:
        setMultiplePixels(strip, [3, 2, 5, 12, 14, 15, 9, 8], RED_LOW)

        # Dynamic part OFF for 3 seconds:
        setMultiplePixels(strip, [0, 5, 10, 15, 3, 6, 9, 12], OFF)
        strip.show()
        time.sleep(3)

        # Dynamic part ON with full brightness for 6 seconds:
        setMultiplePixels(strip, [0, 5, 10, 15, 3, 6, 9, 12], RED_HIGH)
        strip.show()
        time.sleep(6)

except KeyboardInterrupt:
    setMultiplePixels(strip, range(LED_COUNT), OFF)
    strip.show()

