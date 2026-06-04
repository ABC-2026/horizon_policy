import sys
from pathlib import Path

# Add 'archi' directory to sys.path to resolve 'python' package import
archi_dir = Path(__file__).resolve().parents[2]
if str(archi_dir) not in sys.path:
    sys.path.insert(0, str(archi_dir))

import serial.tools.list_ports
import robotInterfaces as rb
import time
import python.simulator.read_shared_memory as read_shared 

def find_arduino_port():
    """
    Find the Arduino Mega connected via CH340.
    """

    ports = serial.tools.list_ports.comports()

    print("\nSearching for Arduino...\n")

    for port in ports:
        print(f"Port: {port.device}")
        print(f"Description: {port.description}")
        print("-" * 40)

        desc = port.description.lower()

        if "ch340" in desc:
            print(f"Arduino found on {port.device}")
            return port.device

    raise RuntimeError("Arduino CH340 device not found.")


def main():
    points = read_shared.read_shared_memory()
    (x, y, z, gripper_state) = points[0]  # use first point
    rHead = 49
    print(f"x = {x}")
    print(f"y = {y}")
    print(f"z = {z}")
    print(f"rHead = {rHead}")
    print(f"gripper = {gripper_state}")

    

    try:
        # Find Arduino
        arduino_port = find_arduino_port()

        # Create robot
        robot = rb.Robot("gantry", arduino_port)

        print("\nRobot connected successfully.")

        # Home robot
        print("\nHoming robot...")
        robot.home()

        print("Homing complete.")
        time.sleep(2)

        # --------------------------------------------------
        # CHANGE THESE VALUES
        # --------------------------------------------------
        

      

        # --------------------------------------------------

        print("\nMoving robot...")
        print(f"x = {x}")
        print(f"y = {y}")
        print(f"z = {z}")
        print(f"rHead = {rHead}")
        print(f"gripper = {gripper_state}")

        robot.move_to(
            x,
            y,
            z,
            rHead=rHead,
            gripper_state=gripper_state
        )

        print("\nMove complete.")

        pose = robot.get_pose()

        print("\nCurrent Pose:")
        print(pose)

        # Example: Close gripper after move
        # robot.move_to(
        #     x,
        #     y,
        #     z,
        #     rHead=rHead,
        #     gripper_state=1
        # )

    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()