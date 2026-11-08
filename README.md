# kuka-pendulum-balancer
A comparative robotics study evaluating MuJoCo vs. Gazebo for real-time optimal control (LQR). Implements a 1kHz balancing loop for a free-spinning inverted pendulum on a 7-DOF KUKA LBR iiwa using ROS 2 (ros2_control).

## System Architecture

```
                  ROS 2
                    |
          Joint State Feedback
                    |
                    v
          +-------------------+
          |  LQR Controller   |
          |                   |
          | Pendulum Angle    |
          | Pendulum Velocity |
          | Robot Joint State |
          +-------------------+
                    |
              Torque Commands
                    |
                    v
          +-------------------+
          |  ros2_control     |
          |  Controller       |
          +-------------------+
                    |
                    v
          +-------------------+
          | MuJoCo Simulator  |
          |                   |
          | KUKA iiwa (7 DOF) |
          | Inverted Pendulum |
          +-------------------+
                    |
                    v
             Physics Feedback

```
