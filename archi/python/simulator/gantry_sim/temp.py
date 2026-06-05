from gantry_controller import GantryController
import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require('sim')
robot = GantryController()

print("\nStarting simulation...")
sim.startSimulation()
robot.open_gripper()
time.sleep(3)

robot.close_gripper()
time.sleep(3)

print("Stopping sim")
sim.stopSimulation()