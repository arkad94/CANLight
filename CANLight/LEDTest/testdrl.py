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

def welcome_animation():
    white = Color(255, 255, 255)

    # Light up 1-4
    for i in range(4):
        strip.setPixelColor(i, white)
        strip.show()
        time.sleep(0.1)

    # Light up 4,5,12,13
    corners = [3, 4, 11, 12]
    for i in corners:
        strip.setPixelColor(i, white)
        strip.show()
        time.sleep(0.1)

    # Light up 14,15,16
    for i in range(13, 16):
        strip.setPixelColor(i, white)
        strip.show()
        time.sleep(0.1)

    # Light up 9,8,1
    sequence = [8, 7, 0]
    for i in sequence:
        strip.setPixelColor(i, white)
        strip.show()
        time.sleep(0.1)

    # Blink 7,6,10,11
    blink_leds = [6, 5, 9, 10]
    for _ in range(3):  # Blink 3 times
        for i in blink_leds:
            strip.setPixelColor(i, white)
        strip.show()
        time.sleep(0.5)
        for i in blink_leds:
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(0.5)

    # Transition to Part 2
    transition_to_drl()

def transition_to_drl():
    # Turn off all LEDs except 1,2,3,4,5,12,13,14,15,16,9,8,1
    drl_leds = [0, 1, 2, 3, 4, 8, 9, 11, 12, 13, 14, 15]
    for i in range(LED_COUNT):
        if i not in drl_leds:
            strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

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
