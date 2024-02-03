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
R1 = 127  # Half brightness for static part
R2 = 255  # Full brightness for dynamic part

# Define colors with respective brightness:
RED_HALF_BRIGHT = Color(R1, 0, 0)  # Red with half brightness
RED_FULL_BRIGHT = Color(R2, 0, 0)  # Red with full brightness
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
        # Static part with half brightness:
        setMultiplePixels(strip, [0, 1, 2, 3, 12, 13, 14, 15], RED_HALF_BRIGHT)

        # Dynamic part with full brightness:
        setMultiplePixels(strip, [5, 9, 6, 10], RED_FULL_BRIGHT)  # LEDs on
        strip.show()
        time.sleep(6)  # LEDs on for 6 seconds

        setMultiplePixels(strip, [5, 9, 6, 10], OFF)  # LEDs off
        strip.show()
        time.sleep(3)  # LEDs off for 3 seconds

except KeyboardInterrupt:
    setMultiplePixels(strip, range(LED_COUNT), OFF)
    strip.show()

