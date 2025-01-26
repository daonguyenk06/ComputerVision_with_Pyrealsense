# import the necessary packages
import numpy as np
import cv2
import pyrealsense2 as rs

# Configure RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start the pipeline
pipeline.start(config)

# define the list of boundaries
boundaries = [
	([17, 15, 100], [50, 56, 200]),
	([86, 31, 4], [220, 88, 50]),
	([25, 146, 190], [62, 174, 250]),
	([103, 86, 65], [145, 133, 128])
]

try:
    while True:
        # Wait for a new frame
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        # Convert the color frame to a NumPy array
        color_image = np.asanyarray(color_frame.get_data())
        
        # loop over the boundaries
        for (lower, upper) in boundaries:
            # create NumPy arrays from the boundaries
            lower = np.array(lower, dtype = "uint8")
            upper = np.array(upper, dtype = "uint8")
            
            # the mask
            mask = cv2.inRange(color_image, lower, upper)
            output = cv2.bitwise_and(color_image, color_image, mask = mask)
        
            # show the images
            cv2.imshow("images", np.hstack([color_image, output]))
            
        # Exit on ESC key
        if cv2.waitKey(1) == 27:
            break

finally:
    # Clean up
    pipeline.stop()
    cv2.destroyAllWindows()