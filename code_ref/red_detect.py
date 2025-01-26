import pyrealsense2 as rs
import numpy as np
import cv2

# Configure RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start the pipeline
pipeline.start(config)

try:
    while True:
        # Wait for a new frame
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        # Convert the color frame to a NumPy array
        color_image = np.asanyarray(color_frame.get_data())

        # Convert to HSV color space
        hsv_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

        # Define red color range in HSV
        lower_red1 = np.array([0, 120, 70])  # Lower range for red (0-10 degrees)
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 70])  # Upper range for red (170-180 degrees)
        upper_red2 = np.array([180, 255, 255])

        # Create masks for the red range
        mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
        red_mask = cv2.bitwise_or(mask1, mask2)

        # Apply the mask to the original image
        red_objects = cv2.bitwise_and(color_image, color_image, mask=red_mask)

        # Display the results
        cv2.imshow("Original Image", color_image)
        cv2.imshow("Red Mask", red_mask)
        cv2.imshow("Detected Red Objects", red_objects)

        # Exit on ESC key
        if cv2.waitKey(1) == 27:
            break

finally:
    # Clean up
    pipeline.stop()
    cv2.destroyAllWindows()
