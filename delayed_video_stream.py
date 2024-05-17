# type in command line
# pip install opencv-python
# pip install screeninfo
# CHANGE delay=20 IN LINE 15 TO +/- DELAY (IN SECONDS)

import cv2
import time
import threading
from collections import deque
from screeninfo import get_monitors


# Buffer to store video frames along with timestamps
class FrameBuffer:
    def __init__(self, delay=30):
        self.buffer = deque()
        self.delay = delay  # Delay in seconds

    def add_frame(self, frame):
        timestamp = time.time()
        # Append the frame and timestamp to the buffer
        self.buffer.append((frame, timestamp))

    def get_delayed_frame(self):
        current_time = time.time()
        while self.buffer:
            frame, timestamp = self.buffer[0]
            # Check if the frame is older than the specified delay
            if current_time - timestamp > self.delay:
                self.buffer.popleft()  # Remove the frame from the buffer as it's displayed
                return frame
            else:
                break
        return None  # If no frame is old enough, return None

# Capture frames from the webcam
def capture_frames(buffer):
    cap = cv2.VideoCapture(0)  # Open the default camera
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            buffer.add_frame(frame)
        else:
            break
    cap.release()

def display_frames(buffer):
    monitor = get_monitors()[0]
    while True:
        frame = buffer.get_delayed_frame()
        if frame is not None:
            # Resize the frame to match the screen resolution
            frame = cv2.resize(frame, (monitor.width, monitor.height))
            cv2.imshow('Vizzy Delay Loop Dreams', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(0.01)  # Sleep to prevent excessive CPU usage


if __name__ == '__main__':
    buffer = FrameBuffer()
    print('Press q to exit')
    # Start the thread for capturing frames
    threading.Thread(target=capture_frames, args=(buffer,)).start()
    # Start the display function in the main thread
    display_frames(buffer)
    cv2.destroyAllWindows()

# buffer = FrameBuffer()
# # Start the thread for capturing frames
# threading.Thread(target=capture_frames, args=(buffer,)).start()
# # Start the display function in the main thread
# display_frames(buffer)
# cv2.destroyAllWindows()