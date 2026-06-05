from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time


class GantryController:

    def __init__(self):

        client = RemoteAPIClient()
        self.sim = client.require('sim')

        self.x_joint = self.sim.getObject('/Prismatic_joint')
        self.y_joint = self.sim.getObject('/Prismatic_joint1')
        self.z_joint = self.sim.getObject('/Prismatic_joint2')

    def move_xyz(self, x, y, z, wait_time=1.0):

        self.sim.setJointTargetPosition(
            self.x_joint, x
        )

        self.sim.setJointTargetPosition(
            self.y_joint, y
        )

        self.sim.setJointTargetPosition(
            self.z_joint, z
        )

        time.sleep(wait_time)

    def open_gripper(self):

        self.sim.setIntProperty(
            self.sim.handle_scene,
            "signal.RG2_open",
            1
        )

    def close_gripper(self):

        self.sim.setIntProperty(
            self.sim.handle_scene,
            "signal.RG2_open",
            0
        )