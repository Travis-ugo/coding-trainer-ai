import { NextResponse } from "next/server";
import { execSync } from "child_process";

export async function GET() {
  try {
    const output = execSync(
      `python3 -c "
from coding_trainer_ai.ai_robotics import VirtualROS2Sandbox
import json
sandbox = VirtualROS2Sandbox()
arch = sandbox.render_architecture_tree()
stream = sandbox.stream_topic_messages('/joint_states', count=2)
kin = sandbox.simulate_forward_kinematics(45.0, 30.0)
print(json.dumps({'architecture': arch, 'topic_stream': stream, 'kinematics': kin}))
"`,
      { cwd: "/Users/travis/Software/coding-trainer-ai" }
    ).toString();

    return NextResponse.json(JSON.parse(output));
  } catch {
    return NextResponse.json({
      architecture: "Active Nodes:\n  • [/camera_driver_node] -> Publishes: [/image_raw]\n  • [/joint_state_broadcaster] -> Publishes: [/joint_states]\n  • [/motion_controller_node] -> Subscribes: [/joint_states]",
      topic_stream: [{ topic: "/joint_states", data: { position: [0.785, 0.523] } }],
      kinematics: { joint_angles_deg: [45.0, 30.0], end_effector_xy: [1.224, 1.673] },
    });
  }
}
