from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time
import traceback

try:
    print("Connecting to CoppeliaSim...")
    client = RemoteAPIClient()
    sim = client.require('sim')
    print("Connected!")
    # Get Joint

    joint = sim.getObject('/YuMi/leftJoint1')
    print("Joint Handle:", joint)
    # Start Simulation

    sim.setStepping(True)

    sim.startSimulation()

    # Read current position
    current_pos = sim.getJointPosition(joint)

    print(f"Current Position: {current_pos:.4f} rad")

    # Target position
    target_pos = current_pos + 0.3

    print(f"Moving to: {target_pos:.4f} rad")

    # Send command
    sim.setJointTargetPosition(joint, target_pos)

    # Allow simulator to execute
    for i in range(200):
        sim.step()

    # Read new position
    new_pos = sim.getJointPosition(joint)

    print(f"New Position: {new_pos:.4f} rad")

    sim.stopSimulation()

    print("\nSUCCESS")

except Exception:
    print("\nERROR\n")
    traceback.print_exc()