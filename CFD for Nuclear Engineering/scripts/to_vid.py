import cv2
import glob
import os

# Configuration
output_video = "output_video.mp4"  # Desired output video file name
frame_rate = 30  # Frames per second for the video

# Get list of PNG files in the current working directory and sort them
images = sorted(glob.glob("animation-1_*.png"))

# Check if images are found
if not images:
    print("No images found in the current working directory.")
    exit()

# Read the first image to determine the video frame size
first_image = cv2.imread(images[0])
height, width, _ = first_image.shape

# Initialize the video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4
video_writer = cv2.VideoWriter(output_video, fourcc, frame_rate, (width, height))

# Add images to the video
for image_path in images:
    img = cv2.imread(image_path)
    video_writer.write(img)

# Release the video writer
video_writer.release()

print(f"Video saved as {output_video}")
