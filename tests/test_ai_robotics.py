import unittest
import math
from coding_trainer_ai.ai_robotics import (
    MathAIEngine,
    PyTorchSandbox,
    SimulatedTensor,
    VirtualROS2Sandbox,
)


class TestAIRobotics(unittest.TestCase):

    def setUp(self):
        self.math_engine = MathAIEngine()
        self.pytorch_sandbox = PyTorchSandbox()
        self.ros2_sandbox = VirtualROS2Sandbox()

    # -------------------------------------------------------------------------
    # Math for AI Tests
    # -------------------------------------------------------------------------
    def test_matrix_multiplication(self):
        a = [[1, 2], [3, 4]]
        b = [[5, 6], [7, 8]]
        res = self.math_engine.matrix_multiply(a, b)
        self.assertEqual(res, [[19, 22], [43, 50]])

    def test_se2_transformation_matrix(self):
        t_matrix = self.math_engine.create_2d_transform_matrix(0.0, 5.0, -2.0)
        self.assertEqual(t_matrix.matrix_data[0][2], 5.0)
        self.assertEqual(t_matrix.matrix_data[1][2], -2.0)

    def test_kalman_filter_step(self):
        res = self.math_engine.kalman_filter_1d_step(10.0, 1.0, 15.0)
        self.assertGreater(res["x_estimate"], 10.0)
        self.assertLess(res["x_estimate"], 15.0)

    # -------------------------------------------------------------------------
    # PyTorch Autograd Sandbox Tests
    # -------------------------------------------------------------------------
    def test_pytorch_tensor_and_autograd(self):
        x = SimulatedTensor([2.0, 3.0], requires_grad=False)
        w = SimulatedTensor([1.0, -1.0], requires_grad=True)
        b = 0.5
        target = 1.0

        res = self.pytorch_sandbox.autograd_backward(x, w, b, target)
        self.assertEqual(res["prediction"], -0.5)  # 2(1) + 3(-1) + 0.5 = -0.5
        self.assertEqual(len(res["grad_w"]), 2)
        self.assertIn("loss", res)

    # -------------------------------------------------------------------------
    # Virtual ROS 2 Sandbox Tests
    # -------------------------------------------------------------------------
    def test_ros2_pub_sub_and_echo(self):
        self.ros2_sandbox.create_publisher("camera_node", "/image_raw")
        self.ros2_sandbox.create_subscriber("object_detector", "/image_raw")

        msg = self.ros2_sandbox.publish_message("/image_raw", "sensor_msgs/Image", {"width": 640})
        self.assertEqual(msg.topic_name, "/image_raw")

        echoed = self.ros2_sandbox.echo_topic("/image_raw")
        self.assertEqual(len(echoed), 1)

    def test_forward_kinematics_2dof(self):
        fk = self.ros2_sandbox.forward_kinematics_2dof(1.0, 1.0, 0.0, 0.0)
        self.assertEqual(fk["end_effector_x"], 2.0)
        self.assertEqual(fk["end_effector_y"], 0.0)


if __name__ == "__main__":
    unittest.main()
