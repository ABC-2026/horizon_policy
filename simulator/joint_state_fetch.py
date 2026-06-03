from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import traceback

try:
    print("Connecting to CoppeliaSim...")

    client = RemoteAPIClient()
    sim = client.require('sim')

    print("Connected!")

    # ----------------------------
    # Start simulation
    # ----------------------------

    sim.startSimulation()
    sim.step()

    print("\nFinding joints...\n")

    joint_names = []

    # Left arm
    for i in range(1, 8):
        joint_names.append(f"/YuMi/leftJoint{i}")

    # Right arm
    for i in range(1, 8):
        joint_names.append(f"/YuMi/rightJoint{i}")

    joint_handles = {}

    # ----------------------------
    # Get handles
    # ----------------------------

    for joint_path in joint_names:
        handle = sim.getObject(joint_path)
        joint_handles[joint_path] = handle

        print(f"{joint_path} -> {handle}")

    print("\n")
    print("=" * 50)
    print("JOINT POSITIONS")
    print("=" * 50)

    # ----------------------------
    # Read positions
    # ----------------------------

    for joint_path, handle in joint_handles.items():

        position = sim.getJointPosition(handle)

        print(
            f"{joint_path:<25} = {position:.6f} rad"
        )

    print("\nStopping simulation...")

    sim.stopSimulation()

except Exception:
    print("\nERROR:\n")
    traceback.print_exc()