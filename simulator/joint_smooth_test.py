from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import traceback

try:

    client = RemoteAPIClient()
    sim = client.require('sim')

    sim.setStepping(True)

    joint = sim.getObject('/YuMi/leftJoint1')

    sim.startSimulation()

    start = sim.getJointPosition(joint)

    print("Start:", start)

    for i in range(50):

        target = start + (0.3 * i / 49.0)

        sim.setJointTargetPosition(
            joint,
            target
        )

        sim.step()

    final = sim.getJointPosition(joint)

    print("Final:", final)

    sim.stopSimulation()

except Exception:
    traceback.print_exc()