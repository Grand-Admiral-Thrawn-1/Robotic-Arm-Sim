import time
import math
from coppeliasim_zmqremoteapi_client import RemoteAPIClient


def move_spherical_joint_gradually(client, joint_handle, current_orientation, target_orientation, steps=50, delay=0.0001):
    for i in range(steps):
        interpolated_orientation = [
            current_orientation[0] + (target_orientation[0] - current_orientation[0]) * (i / steps),
            current_orientation[1] + (target_orientation[1] - current_orientation[1]) * (i / steps),
            current_orientation[2] + (target_orientation[2] - current_orientation[2]) * (i / steps)
        ]

        sim = client.getObject('sim')
        sim.setObjectOrientation(joint_handle, -1, interpolated_orientation)

        time.sleep(delay)


def move_to_config_gradually(client, joint_handles, current_positions, target_positions, max_velocities,
                             max_accelerations, max_jerks, steps=50, delay=0.0001):
    for i in range(steps):
        interpolated_position = current_positions + (target_positions - current_positions) * (i / steps)

        sim = client.getObject('sim')
        params = {
            'joints': joint_handles,
            'targetPos': [interpolated_position],
            'maxVel': max_velocities,
            'maxAccel': max_accelerations,
            'maxJerk': max_jerks
        }
        sim.moveToConfig(params)

        time.sleep(delay)


client = RemoteAPIClient()
sim = client.getObject('sim')

joint_handles = [
    sim.getObjectHandle('/Socket_respondable/Arm_1'),
    sim.getObjectHandle('/Socket_respondable/Arm_2'),
    sim.getObjectHandle('/Socket_respondable/Hand')
]

vel = 180 * math.pi / 180
accel = 180 * math.pi / 180
jerk = 180 * math.pi / 180

target_pos1 = [20 * math.pi / 180, 20 * math.pi / 180, 0 * math.pi / 180]
target_pos2 = 90 * math.pi / 180
target_pos3 = [90 * math.pi / 180, 90 * math.pi / 180, 0]

current_pos1 = sim.getObjectOrientation(joint_handles[0], 1)
current_pos2 = sim.getJointPosition(joint_handles[1])
current_pos3 = sim.getObjectOrientation(joint_handles[2], -1)

print("Moving Arm_1 (spherical joint)...")
move_spherical_joint_gradually(client, joint_handles[0], current_pos1, target_pos1)

print("Moving Arm_2 (regular joint)...")
move_to_config_gradually(client, [joint_handles[1]], current_pos2, target_pos2, [vel], [accel], [jerk])

print("Moving Hand (spherical joint)...")
move_spherical_joint_gradually(client, joint_handles[2], current_pos3, target_pos3)
