from gpiozero import LED
from time import sleep
import os

# Output folder path (change to your desired path)
output_folder = "/home/pi/gpio_test_results"

# Create the folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Output file path
output_file_path = os.path.join(output_folder, "gpio_test_results.txt")

# Open the file in write mode
with open(output_file_path, "w") as file:

    # Test GPIO pins 2 through 27
    for pin in range(2, 28):
        try:
            test_pin = LED(pin)
            test_pin.on()
            sleep(1)
            test_pin.off()
            result = f"GPIO pin {pin} is working.\n"
            print(result)
            file.write(result)
        except Exception as e:
            error_message = f"GPIO pin {pin} may have an issue: {e}\n"
            print(error_message)
            file.write(error_message)
        finally:
            test_pin.close()

print(f"Test results saved to {output_file_path}")
