import time
from rpi_ws281x import PixelStrip, Color

# LED strip configuration common to all scripts
LED_COUNT = 16        # Number of LED pixels (4x4 grid).
LED_PIN = 18          # GPIO pin connected to the pixels (must support PWM).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800kHz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to a reasonable number for safety.
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)

# Create PixelStrip object with appropriate configuration
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()  # Initialize the library

# Helper functions
def setPixelColor(strip, pixel, color):
    strip.setPixelColor(pixel, color)

def setMultiplePixels(strip, pixels, color):
    for pixel in pixels:
        setPixelColor(strip, pixel, color)

# Script 1: Welcome Animation
def welcome_animation():
    white = Color(255, 235, 200)
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
    time.sleep(2)

# Script 2: Amber Animation
def script2():
    # Initially set the top and bottom rows to red
    for i in range(4):
        strip.setPixelColor(i, Color(255, 0, 0))  # Top row red
        strip.setPixelColor(15 - i, Color(255, 0, 0))  # Bottom row red
    strip.show()

    # Amber animation for the middle rows
    for i in range(4):
        # Middle top row (LEDs 9 to 12 in your setup)
        strip.setPixelColor(8 + i, Color(255, 96, 0))
        # Middle bottom row (LEDs 8 to 5 in your setup, reversed)
        strip.setPixelColor(7 - i, Color(255, 96, 0))
        strip.show()
        time.sleep(0.2)  # Animation speed

    # Turn off only the amber LEDs
    for i in range(4, 12):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
    time.sleep(1)
    time.sleep(2)

# Script 3: Mirrored Amber Animation
def script3():
    # Set top and bottom rows to red
    for i in range(4):
        strip.setPixelColor(i, Color(255, 0, 0))  # Top row red
        strip.setPixelColor(15 - i, Color(255, 0, 0))  # Bottom row red
    strip.show()

    # Mirrored Amber animation for the middle rows
    for i in reversed(range(4)):
        # Middle top row (LEDs 5 to 8 in your setup, reversed)
        strip.setPixelColor(4 + i, Color(255, 96, 0))
        # Middle bottom row (LEDs 13 to 10 in your setup)
        strip.setPixelColor(12 - i, Color(255, 96, 0))
        strip.show()
        time.sleep(0.2)  # Animation speed

    # Turn off only the amber LEDs
    for i in range(4, 12):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
    time.sleep(1)
    time.sleep(2)

# Script 4: Stop Light Animation
def script4():
    # Define the brightness values for red
    R1 = 20   # Lower brightness for static part
    R2 = 255  # Full brightness for dynamic part

    # Define colors with respective brightness:
    RED_LOW = Color(R1, 0, 0)    # Red with lower brightness (R1)
    RED_HIGH = Color(R2, 0, 0)   # Red with full brightness (R2)
    OFF = Color(0, 0, 0)

    # Static part with lower brightness:
    setMultiplePixels(strip, [1, 2, 7, 11, 14, 13, 4, 8], RED_LOW)

    # Dynamic part OFF for 3 seconds:
    setMultiplePixels(strip, [0, 5, 10, 15, 3, 6, 9, 12], OFF)
    strip.show()
    time.sleep(3)

    # Dynamic part ON with full brightness for 6 seconds:
    setMultiplePixels(strip, [0, 5, 10, 15, 3, 6, 9, 12], RED_HIGH)
    strip.show()
    time.sleep(6)

# Main logic to run each script sequentially
def main():
    try:
        welcome_animation()
        script2()
        script3()
        script4()
    except KeyboardInterrupt:
        # Turn off all LEDs before exiting
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()

if __name__ == '__main__':
    main()

