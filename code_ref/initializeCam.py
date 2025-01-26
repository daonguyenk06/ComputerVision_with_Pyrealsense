# import sys
# sys.path.append('/Users/101173468/Desktop/Python311.0/IntelRealSense Code/pyrealsense.py')
# # print(sys.path)

import pyrealsense2 as rs

# Logging to make sure the camera works
try:
    # Initialize the pipeline
    print("Initializing pipeline...")
    pipe = rs.pipeline()
    print(f"Pipeline initialized: {pipe}")

    # Start the pipeline and retrieve the profile
    print("Starting pipeline...")
    profile = pipe.start()
    print(f"Pipeline started with profile: {profile}")

    # Print profile details
    print("Profile streams:")
    for stream in profile.get_streams():
        print(f"- Stream: {stream.stream_type()}, Format: {stream.format()}, FPS: {stream.fps()}")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Stop the pipeline to ensure proper cleanup
    if 'pipe' in locals():
        print("Stopping pipeline...")
        pipe.stop()
        print("Pipeline stopped.")