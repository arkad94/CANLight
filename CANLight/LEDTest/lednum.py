import time
from rpi_ws281x import PixelStrip, Color

# LED strip configuration
LED_COUNT = 16  # Number of LED pixels.
LED_PIN = 18    # GPIO pin connected to the pixels (must support PWM).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800kHz)
LED_DMA = 10    # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 25  # Set brightness here
LED_INVERT = False   # True to invert the signal (when using NPN transistor level shift)

# Create PixelStrip object with appropriate configuration.
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()  # Initialize the library (must be called once before other functions).

def color_alternator(index):
    # Alternate between turquoise and green
    if index % 2 == 0:
        return Color(51, 204, 255)  # Turquoise color
    else:
        return Color(0, 128, 0)  # Green color

try:
    print('Press Ctrl-C to quit.')
    while True:
        for i in range(LED_COUNT):
            color = color_alternator(i)
            strip.setPixelColor(i, color)  # Turn on LED at position i with alternating colors
            strip.show()
            time.sleep(1)  # Wait for a second
            strip.setPixelColor(i, Color(0, 0, 0))  # Turn off LED at position i

except KeyboardInterrupt:
    # On Ctrl+C, turn off all the LEDs.
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
