# camera_debug.py

from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import numpy as np
from PIL import Image
import traceback
import os


def save_camera_image(sim, camera_path, output_file):
    """
    Reads a vision sensor image from CoppeliaSim and saves it.
    """

    print("\n" + "=" * 60)
    print(f"Processing camera: {camera_path}")
    print("=" * 60)

    # Get handle
    cam = sim.getObject(camera_path)

    print("Handle:", cam)

    # Get image
    img_data, resolution = sim.getVisionSensorImg(cam)

    width = resolution[0]
    height = resolution[1]

    print(f"Resolution: {width} x {height}")

    # Convert bytes -> numpy
    img_array = np.frombuffer(img_data, dtype=np.uint8)

    print("Raw pixel count:", img_array.size)

    expected_pixels = width * height * 3

    print("Expected pixels:", expected_pixels)

    if img_array.size != expected_pixels:
        raise ValueError(
            f"Pixel mismatch! Expected {expected_pixels}, got {img_array.size}"
        )

    # Reshape
    img_array = img_array.reshape(height, width, 3)

    print("Image shape:", img_array.shape)

    # Some CoppeliaSim builds return vertically flipped images
    img_array = np.flipud(img_array)

    # Save
    Image.fromarray(img_array).save(output_file)

    print(f"Saved: {os.path.abspath(output_file)}")


try:
    print("Connecting to CoppeliaSim...")

    client = RemoteAPIClient()
    sim = client.require('sim')

    print("Connected!")

    # --------------------------------------------------
    # Camera paths
    # --------------------------------------------------

    LEFT_CAMERA = "/YuMi/Left_wrist_cam"
    RIGHT_CAMERA = "/YuMi/Right_wrist_cam"
    OVERHEAD_CAMERA = "/YuMi/overhead_cam"

    # --------------------------------------------------
    # Start simulation
    # --------------------------------------------------

    print("\nStarting simulation...")

    sim.startSimulation()

    # Let simulation advance one step
    sim.step()

    # --------------------------------------------------
    # Save all cameras
    # --------------------------------------------------

    save_camera_image(
        sim,
        LEFT_CAMERA,
        "left.png"
    )

    save_camera_image(
        sim,
        RIGHT_CAMERA,
        "right.png"
    )

    save_camera_image(
        sim,
        OVERHEAD_CAMERA,
        "overhead.png"
    )

    # --------------------------------------------------
    # Stop simulation
    # --------------------------------------------------

    print("\nStopping simulation...")

    sim.stopSimulation()

    print("\nSUCCESS!")
    print("Generated:")
    print("  left.png")
    print("  right.png")
    print("  overhead.png")

except Exception:
    print("\nERROR OCCURRED:\n")
    traceback.print_exc()