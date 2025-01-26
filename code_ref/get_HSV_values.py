
""" Click on the Image Frame to get HSV values! """

import cv2
import numpy as np
import pyrealsense2 as rs


# Configure RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start the pipeline
pipeline.start(config)

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Left mouse button click
        hsv_value = hsv_image[y, x]  # Access HSV value at the clicked pixel
        print(f"HSV Value at ({x}, {y}): {hsv_value}")

# Create a window and set the mouse callback
cv2.namedWindow("RealSense Feed")
cv2.setMouseCallback("RealSense Feed", mouse_callback)

try:
    while True:
        # Wait for a new frame
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        # Convert the color frame to a NumPy array
        color_image = np.asanyarray(color_frame.get_data())

        # Convert the BGR image to HSV
        hsv_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

        # Display the original frame
        cv2.imshow("RealSense Feed", color_image)

        # Exit on ESC key
        if cv2.waitKey(1) == 27:
            break

finally:
    # Cleanup
    pipeline.stop()
    cv2.destroyAllWindows()
