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
    red = Color(255, 0, 0)

    # Light up 2-3
    for i in range(1, 3):
        strip.setPixelColor(i, white)
        strip.show()
        time.sleep(0.1)

    # Light up 5,12
    corners = [4, 11]
    for i in corners:
        strip.setPixelColor(i, white)
        strip.show()
        time.sleep(0.1)

    # Light up 14,15
    for i in range(13, 15):
        strip.setPixelColor(i, white)
        strip.show()
        time.sleep(0.1)

    # Light up 9,8
    sequence = [8, 7]
    for i in sequence:
        strip.setPixelColor(i, white)
        strip.show()
        time.sleep(0.1)

    # Blink "X" pattern (additional_sequence)
    for _ in range(4):  # Blink 4 times
        for i in [0, 6, 10, 12, 3, 5, 9, 15]:
            strip.setPixelColor(i, white)
        strip.show()
        time.sleep(0.25)  # Blink every 0.25 seconds
        for i in [0, 6, 10, 12, 3, 5, 9, 15]:
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(0.25)  # Off for 0.25 seconds

    # Transition to Part 2
    transition_to_drl()

    

def transition_to_drl():
    white = Color(255, 235, 200)
    # Turn off all LEDs except 1,2,3,4,5,12,13,14,15,16,9,8
    drl_leds = [0, 1, 2, 3, 4, 7, 8, 11, 12, 13, 14, 15]  # Corrected list of LEDs for DRL
    for i in range(LED_COUNT):
        if i in drl_leds:
            strip.setPixelColor(i, white)  # Ensure these LEDs are on
        else:
            strip.setPixelColor(i, Color(0, 0, 0))  # Turn off other LEDs
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
