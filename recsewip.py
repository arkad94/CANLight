import can
import time
import struct
import datetime

def milliseconds_since_midnight():
    now = datetime.datetime.now()
    midnight = datetime.datetime(now.year, now.month, now.day)
    return int((now - midnight).total_seconds() * 1000)  # Convert to milliseconds

def send_response(bus, arbitration_id, received_time):
    response_time = milliseconds_since_midnight()
    one_way_latency = response_time - received_time  # Calculate one-way latency (a1)
    data = struct.pack('II', one_way_latency, response_time)  # Pack a1 and response_time
    message = can.Message(arbitration_id=arbitration_id, data=data, is_extended_id=False)
    try:
        bus.send(message)
        print(f"Sent response with latency {one_way_latency} ms on {bus.channel_info}")
        print(f"Response data: {data}")
    except can.CanError:
        print("Response NOT sent")

def listen_and_respond(bus, arbitration_id):
    while True:
        message = bus.recv(60.0)  # Timeout in seconds
        if message is None:
            print("Timeout occurred, no message.")
            continue
        if message.arbitration_id == arbitration_id:
            received_time = milliseconds_since_midnight()
            print(f"Message received: {message}")
            print(f"Received data: {message.data}")
            send_response(bus, arbitration_id, received_time)

def main():
    global bus
    bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=500000)
    print("Listening for messages...")
    listen_and_respond(bus, 749)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        print("Closing CAN bus.")
        bus.shutdown()
