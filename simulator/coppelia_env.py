from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import numpy as np
class CoppeliaYuMiEnv:

    def __init__(self):

        print("Connecting to CoppeliaSim...")

        client = RemoteAPIClient()
        self.sim = client.require("sim")

        print("Connected!")

        # Cameras
        self.left_cam = self.sim.getObject("/YuMi/Left_wrist_cam")
        self.right_cam = self.sim.getObject("/YuMi/Right_wrist_cam")
        self.overhead_cam = self.sim.getObject("/YuMi/overhead_cam")

        print("Camera handles loaded")

        # Joint paths
        self.joint_names = []

        for i in range(1, 8):
            self.joint_names.append(f"/YuMi/leftJoint{i}")

        for i in range(1, 8):
            self.joint_names.append(f"/YuMi/rightJoint{i}")

        self.joints = [
            self.sim.getObject(name)
            for name in self.joint_names
        ]

        print("Joint handles loaded")

    def start(self):
        self.sim.startSimulation()
        self.sim.step()

    def stop(self):
        self.sim.stopSimulation()

    def get_joint_state(self):

        state = []

        for joint in self.joints:
            state.append(
                self.sim.getJointPosition(joint)
            )

        return np.array(
            state,
            dtype=np.float32
        )

    def get_camera_image(self, cam_handle):

        img_data, resolution = self.sim.getVisionSensorImg(
            cam_handle
        )

        width = resolution[0]
        height = resolution[1]

        img = np.frombuffer(
            img_data,
            dtype=np.uint8
        )
        img = img.reshape(
            height,
            width,
            3
        )
        img = np.flipud(img)
        return img

    def get_observation(self):
        return {
            "state": self.get_joint_state(),
            "images": {
                "overhead":
                    self.get_camera_image(
                        self.overhead_cam
                    ),
                "left_wrist":
                    self.get_camera_image(
                        self.left_cam
                    ),
                "right_wrist":
                    self.get_camera_image(
                        self.right_cam
                    ),
            },
            "prompt":
                "pick and place object"
        }