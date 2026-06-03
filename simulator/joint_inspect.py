from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import traceback

try:
    client = RemoteAPIClient()
    sim = client.require('sim')

    joint = sim.getObject('/YuMi/leftJoint1')

    print("Joint Handle:", joint)

    print("Joint Position:", sim.getJointPosition(joint))

    try:
        print("Joint Mode:", sim.getJointMode(joint))
    except Exception as e:
        print("Could not read joint mode:", e)

    try:
        print("Target Position:", sim.getJointTargetPosition(joint))
    except Exception as e:
        print("Could not read target position:", e)

    try:
        print("Target Velocity:", sim.getJointTargetVelocity(joint))
    except Exception as e:
        print("Could not read target velocity:", e)

except Exception:
    traceback.print_exc()