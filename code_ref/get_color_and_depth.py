import pyrealsense2 as rs
import numpy as np
import cv2

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape
        
        # Define the pixel range (e.g., a 10x10 area around the center)
        x_start, x_end = 310, 330  # Horizontal range
        y_start, y_end = 230, 250  # Vertical range

        # Extract the region of interest (ROI)
        roi_depth = depth_image[y_start:y_end, x_start:x_end]
        r,b,g = color_image[320, 240]

        # Convert depth values from millimeters to meters
        distances = roi_depth * 0.001

        # Calculate statistics
        valid_distances = distances[distances > 0]  # Ignore zero (invalid) values
        if valid_distances.size > 0:
            avg_distance = np.mean(valid_distances)
            min_distance = np.min(valid_distances)
            max_distance = np.max(valid_distances)
            print(f"\nROI Stats: Avg={avg_distance:.2f}m, Min={min_distance:.2f}m, Max={max_distance:.2f}m")
            print(f"Color: {r}, {b}, {g}")
        else:
            print("No valid distances in the selected range.")

        # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_colormap_dim != color_colormap_dim:
            resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_color_image, depth_colormap))
        else:
            images = np.hstack((color_image, depth_colormap))

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        
        # Exit on ESC key
        if cv2.waitKey(1) == 27:
            break

finally:

    # Stop streaming
    pipeline.stop()