DEBUG = True
import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import serial
import time 
class Gantry:
    def __init__(self,port):
        # pass
        self.last_rotation_pos = 3
        self.gantry = serial.Serial(port=port, baudrate=115200, timeout = 0.1)
        self.current_pos = [0,0,0,0,0]#x,y,z,rhead,gs
        # self.home()
        time.sleep(1)
        print("Gantry connected on port %s" % port)
        
        
    def move_to(self, x=None, y=None, z=None, rHead=None, gripper_state=None):
        #print('before doing something',gripper_state)
        if gripper_state is not None:
            #print("hiiiiii")
            gripper_state = 1 if gripper_state == 0 else 0
            # gripper_state = not gripper_state
        else:
            #print("oooppsss")
            gripper_state = self.current_pos[4]
        x = x if x is not None else self.current_pos[0]
        y = y if y is not None else self.current_pos[1]
        z = z if z is not None else self.current_pos[2]
        rHead = rHead if rHead is not None else self.current_pos[3]
        
        # print(x,y,z,rHead,gripper_state)
        #print("inside move to ",gripper_state)
        cmd = self.conv_to_ard_cmd(x, y, z, gripper_state, rHead)
        self.gantry.write(cmd.encode('utf-8'))
        # if(((pp := device.readline().decode()) == "d\r\n")):
        # while((pp := self.gantry.read() != b"d")):
        #     if DEBUG:
        #         print(repr(pp))
        #         ...
        # print(pp)
        tmpp = [float(x) for x in cmd[:-2].split(" ")]
        # tmpp = [int(x) for x in ' '.join(cmd.split(" ")[:-1]).split()]
        # tmpp = map(int,cmd.split(" "))
        while(((pp := self.gantry.read()) != b'j')):
            if DEBUG:
                # print(repr(pp))
                pass        
        #print("done")
        self.update_current_pos(tmpp[0],tmpp[1],tmpp[2],tmpp[4],tmpp[3])
    
    def rotate_gripper(self, rHead):
        # pass
        cmd = "-1 -1 -1 9 %s ;" % str(rHead) 
        self.gantry.write(cmd.encode('utf-8'))
        while((pp := self.gantry.read() != b'r')):
            if DEBUG:
                # print(repr(pp))
                ...
        self.update_current_pos(self.current_pos[0],self.current_pos[1],self.current_pos[2],rHead,self.current_pos[3])
    
    def gripper(self, gripper_state):
        # pass
        cmd = self.conv_to_ard_cmd(-1, -1, -1, gripper_state, self.last_rotation_pos)
        self.gantry.write(cmd.encode('utf-8'))
        while((tempp:=self.gantry.read()) != b'e'):
            if DEBUG:
                # print(tempp)
                ...
        self.update_current_pos(self.current_pos[0],self.current_pos[1],self.current_pos[2],self.current_pos[4],gripper_state)
        
    def get_pose(self):
        # pass
        pose = self.current_pos
        return pose
    
    def clear_alarm():
        pass
    
    def home(self):
        # pass
        print("inside gantry sub module\nhoming")
        # cmd = "-1 -1 -1 2 %s ;" % str(self.last_rotation_pos) 
        cmd = "-1 -1 -1 2 0 ;" 
        # print(cmd)
        bytes_written = self.gantry.write(cmd.encode('utf-8'))
        # print(bytes_written)
        self.gantry.write(cmd.encode('utf-8'))
        # print("sent")
        # while(((pp:=device.readline().decode()) != "h\r\n")):
        while(((pp := self.gantry.read()) != b'h')):
            if DEBUG:
                # print(repr(pp))
                pass
        self.current_pos = [0,0,0,0,0]


    def conv_to_ard_cmd(self,x,y,z,end,servo):
        temp = "%s %s %s %s %s ;" % (str(x), str(y), str(z), str(end), str(servo))
        # print(temp)
        return temp     

    def update_current_pos(self, x, y, z, rhead, gripper_state):
        self.current_pos = [x, y, z, rhead, gripper_state]
        
        
    def transformation(self, x, y, z, rHead,mode):
        # pass
        if x==0 or y==0 or z==0:
            # return ValueError("InvalidCoordinates")
            return None
        if mode=='src':
            g_x = 140 + y
            g_y = 220 + x
        if mode=='dest':
            g_x = 415 + y
            g_y = 306 + x
        # g_x = 117 + y + 10
        # g_y = 134 + x - 30
        g_z = z - 165 + 15
        g_z = 134
            
        g_rHead = rHead + 3 
        
        if g_rHead < 0 :
            g_rHead = g_rHead + 180
        elif g_rHead > 180:
            g_rHead = g_rHead - 180
            
        
        return [g_x, g_y, g_z, g_rHead]
    
# robot_1 = Gantry('COM9')