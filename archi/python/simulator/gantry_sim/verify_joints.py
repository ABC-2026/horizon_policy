from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require('sim')

for joint in sim.getObjectsInTree(
        sim.handle_scene,
        sim.object_joint_type):

    try:
        name = sim.getObjectAlias(joint)
        joint_type = sim.getJointType(joint)

        print(
            f"name={name}, type={joint_type}"
        )

    except Exception as e:
        print(e)