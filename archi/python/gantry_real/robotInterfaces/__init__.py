import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

class Robot:
    def __init__(self, type, port):
        # pass
        self.type = type
        if type == 'dobot':
            import dobot.dobot as rb
            self.robot = rb.Dobot(port)
        if type == 'gantry':
            print(type)
            import gantry.gantry as rb
            self.robot = rb.Gantry(port)
            
        
    
    def move_to(self, x=None, y=None, z=None, rHead=None, gripper_state=None):
        # pass
        # x, y, z = self.robot.transformation(x, y, z)
        print("Gripper :",gripper_state)
        print("Head ",rHead)
        self.robot.move_to(x, y, z, rHead, gripper_state)
    
    def rotate_gripper(self, rHead):
        # pass
        self.robot.rotate_gripper(rHead)
    
    def gripper(self, gripper_state):
        # pass
        self.robot.gripper(gripper_state)

    def get_pose(self):
        # pass
        pose = self.robot.get_pose()
        return pose
    
    def clear_alarm(self):
        # pass
        self.robot.clear_alarm()
    
    def home(self):
        # pass
        print("hii")
        self.robot.home()

    def transformation(self,coords,mode='src'):
        x, y, z, rHead = coords
        return self.robot.transformation(x, y, z, rHead,mode)
        
        
    def set_pwm(self,pwr_pin,pwm_pin,freq):
        if self.type == 'dobot':
            self.robot.set_pwm(pwr_pin,pwm_pin,freq)
        else:
            return ValueError('Invalid Function')