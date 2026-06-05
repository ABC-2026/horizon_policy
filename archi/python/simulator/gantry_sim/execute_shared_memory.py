from pathlib import Path
import sys
import time

from coppeliasim_zmqremoteapi_client import RemoteAPIClient

CURRENT_DIR = Path(__file__).resolve().parent
SIMULATOR_DIR = CURRENT_DIR.parent

sys.path.append(str(SIMULATOR_DIR))

from read_shared_memory import read_shared_memory
from gantry_controller import GantryController


client = RemoteAPIClient()
sim = client.require('sim')

robot = GantryController()

print("Starting simulation...")
sim.startSimulation()

time.sleep(1)

points = read_shared_memory()

print(f"Loaded {len(points)} points")

for i, (x, y, z, g) in enumerate(points):

    print(
        f"Step {i+1}: "
        f"x={x}, y={y}, z={z}, g={g}"
    )

    robot.move_xyz(x,y,z, wait_time=2
    )

    if g > 0:
        print("Opening gripper")
        robot.open_gripper()
    else:
        print("Closing gripper")
        robot.close_gripper()

    time.sleep(1)

print("Trajectory complete")

time.sleep(2)

print("Stopping simulation...")
sim.stopSimulation()