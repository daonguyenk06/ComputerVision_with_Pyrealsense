import numpy as np
import cv2
import pyrealsense2 as rs

# Configure RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start the pipeline
pipeline.start(config)

# Start a while loop
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

    """ HSV ranges will need to be adjusted to the environment at competition. 
        Use 'get_HSV_value.py' to get the most accurate values.
    """
    # Define HSV ranges for red, green, blue, yellow, and orange
    black_lower = np.array([0, 0, 0], np.uint8)
    black_upper = np.array([180, 255, 100], np.uint8)
    red_lower1 = np.array([0, 180, 100], np.uint8)
    red_upper1 = np.array([5, 255, 160], np.uint8)
    red_lower2 = np.array([170, 100, 140], np.uint8)
    red_upper2 = np.array([180, 255, 200], np.uint8)
    green_lower = np.array([75, 100, 90], np.uint8)
    green_upper = np.array([95, 255, 180], np.uint8)
    blue_lower = np.array([95, 200, 90], np.uint8)
    blue_upper = np.array([105, 255, 255], np.uint8)
    yellow_lower = np.array([23, 90, 150], np.uint8)
    yellow_upper = np.array([25, 255, 255], np.uint8)
    orange_lower = np.array([10, 80, 150], np.uint8)
    orange_upper = np.array([18, 255, 255], np.uint8)

    # Create masks for each color
    black_mask = cv2.inRange(hsv_image, black_lower, black_upper)
    red_mask1 = cv2.inRange(hsv_image, red_lower1, red_upper1)
    red_mask2 = cv2.inRange(hsv_image, red_lower2, red_upper2)
    red_mask = cv2. bitwise_or(red_mask1, red_mask2)
    green_mask = cv2.inRange(hsv_image, green_lower, green_upper)
    blue_mask = cv2.inRange(hsv_image, blue_lower, blue_upper)
    yellow_mask = cv2.inRange(hsv_image, yellow_lower, yellow_upper)
    orange_mask = cv2.inRange(hsv_image, orange_lower, orange_upper)

    # Apply morphological transformations
    kernel = np.ones((5, 5), "uint8")
    black_mask = cv2.dilate(black_mask, kernel)
    red_mask = cv2.dilate(red_mask, kernel)
    green_mask = cv2.dilate(green_mask, kernel)
    blue_mask = cv2.dilate(blue_mask, kernel)
    yellow_mask = cv2.dilate(yellow_mask, kernel)
    orange_mask = cv2.dilate(orange_mask, kernel)

    # Detect and label colors
    for mask, color_name, color_value in [
        (black_mask, "Black", (0, 0, 0)),  # Add Black
        (red_mask, "Red", (0, 0, 255)),
        (green_mask, "Green", (0, 255, 0)),
        (blue_mask, "Blue", (255, 0, 0)),
        (yellow_mask, "Yellow", (0, 255, 255)),
        (orange_mask, "Orange", (0, 165, 255)),
    ]:
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 300:  # Filter out small detections
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(color_image, (x, y), (x + w, y + h), color_value, 2)
                cv2.putText(color_image, color_name, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_value, 2)

    # Display the result
    cv2.imshow("Color Detection", color_image)

    # Exit on ESC key
    if cv2.waitKey(1) == 27:
        break

# Cleanup
pipeline.stop()
cv2.destroyAllWindows()
