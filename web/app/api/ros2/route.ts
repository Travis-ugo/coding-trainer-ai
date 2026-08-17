import { NextResponse } from "next/server";
import { runPythonBridge } from "../pythonBridge";

export async function GET() {
  try {
    const data = await runPythonBridge("/api/ros2", "GET");
    return NextResponse.json(data);
  } catch {
    return NextResponse.json({
      architecture: "Active Nodes:\n  • [/camera_driver_node] -> Publishes: [/image_raw]\n  • [/joint_state_broadcaster] -> Publishes: [/joint_states]\n  • [/motion_controller_node] -> Subscribes: [/joint_states]",
      topic_stream: [{ topic: "/joint_states", data: { position: [0.785, 0.523] } }],
      kinematics: { joint_angles_deg: [45.0, 30.0], end_effector_xy: [1.224, 1.673] },
    });
  }
}
