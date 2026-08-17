import { NextResponse } from "next/server";
import { runPythonBridge } from "../pythonBridge";

export async function GET() {
  try {
    const data = await runPythonBridge("/api/modules", "GET");
    return NextResponse.json(data);
  } catch {
    return NextResponse.json([
      {
        id: "py_mod_01",
        title: "Module 1: Variables, Dynamic Typing & Name Tag Analogy",
        summary: "Understanding how Python stores variables as dynamic name tags pointing to objects in memory.",
        non_cs_analogy: "In Python, a variable is simply a sticky 'Name Tag' stuck onto an object in memory!",
        syntax_guide: "def calculate_memory_address(obj):\n    # Return integer memory address id of object\n    return id(obj)",
        order: 1,
      },
    ]);
  }
}
