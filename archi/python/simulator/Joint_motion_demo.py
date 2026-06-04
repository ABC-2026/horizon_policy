from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import traceback

try:

    client = RemoteAPIClient()
    sim = client.require('sim')

    sim.setStepping(True)

    joint = sim.getObject('/YuMi/rightJoint1')

    print("Joint Handle:", joint)

    sim.startSimulation()

    start_pos = sim.getJointPosition(joint)

    print("Start Position:", start_pos)

    # Move +0.8 rad
    print("Moving positive...")

    for i in range(200):

        target = start_pos + (0.8 * i / 199)

        sim.setJointTargetPosition(
            joint,
            target
        )

        sim.step()

    # Move back
    print("Moving negative...")

    for i in range(200):

        target = start_pos + 0.8 - (0.8 * i / 199)

        sim.setJointTargetPosition(
            joint,
            target
        )

        sim.step()

    final_pos = sim.getJointPosition(joint)

    print("Final Position:", final_pos)

    sim.stopSimulation()

    print("\nSUCCESS")

except Exception:
    traceback.print_exc()