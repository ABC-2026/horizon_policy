from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time

client = RemoteAPIClient()
sim = client.require('sim')

x = sim.getObject('/Gantry_Base/Prismatic_joint')
y = sim.getObject('/Gantry_Base/Gantry_X/Prismatic_joint1')
z = sim.getObject('/Gantry_Base/Gantry_X/Prismatic_joint1/Gantry_Y/Disc/Prismatic_joint2')
print("\nStarting simulation...")
sim.startSimulation()
print("Found handles")

print("Move X")
sim.setJointTargetPosition(x, 0.5)
time.sleep(3)

print("Move Y")
sim.setJointTargetPosition(y, -0.5)
time.sleep(3)

print("Move Z")
sim.setJointTargetPosition(z, -0.06)
time.sleep(3)
print("\nStopping simulation...")

sim.stopSimulation()