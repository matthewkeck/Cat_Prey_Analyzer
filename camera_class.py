from picamera2 import Picamera2, Preview
from collections import deque
import pytz
from datetime import datetime
import time
import sys
import cv2
import numpy as np
import io, gc

class Camera:
    def __init__(self):
        # Initialize Picamera2
        self.picam2 = Picamera2()
        self.picam2.preview_configuration.main.size = (2592, 1944)
        self.picam2.preview_configuration.main.format = 'RGB888'
        self.picam2.preview_configuration.align()
        self.picam2.configure("preview")
        self.picam2.start()

    def fill_queue(self, deque):
        while True:
            gc.collect()
            frame = self.picam2.capture_array()
            image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            deque.append((datetime.now(pytz.timezone('Europe/Zurich')).strftime("%Y_%m_%d_%H-%M-%S.%f"), image))
            
            # Optionally remove the oldest item if the deque exceeds a certain size
            if len(deque) > 60:
                deque.popleft()
                
            print("Queue length: " + str(len(deque)) + "\tFrame size: " + str(sys.getsizeof(frame)))
            
            # Sleep to control frame rate
            time.sleep(1 / 3)  # 3 frames per second

# Example usage
if __name__ == "__main__":
    # Initialize the deque with a max length if needed
    image_deque = deque(maxlen=100)
    cam = Camera()
    cam.fill_queue(image_deque)


