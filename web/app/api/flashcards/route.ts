import { NextResponse } from "next/server";
import { runPythonBridge } from "../pythonBridge";

export async function GET() {
  try {
    const data = await runPythonBridge("/api/flashcards", "GET");
    return NextResponse.json(data);
  } catch {
    return NextResponse.json([
      {
        id: "deck_python",
        title: "Python Memory & LEGB Scope",
        cards: [
          {
            card_id: "py_01",
            prompt: "What is the intuitive difference between a Stack and a Heap?",
            answer: "Stack: Fast, fixed-size automatic memory allocated per function call frame.\nHeap: Dynamic, manually allocated memory requiring explicit deallocation (`delete`).",
            analogy: "Stack = Desk surface for active work; Heap = Storage warehouse down the hall.",
            repetition_number: 1,
            interval_days: 1,
          },
          {
            card_id: "py_02",
            prompt: "What does LEGB Scope resolution rule stand for in Python?",
            answer: "L: Local ➔ E: Enclosing ➔ G: Global ➔ B: Built-in scope lookup chain.",
            analogy: "Looking for an item first in your pocket, then room, house, and city.",
            repetition_number: 1,
            interval_days: 1,
          },
          {
            card_id: "py_03",
            prompt: "Why are Python lists dynamic arrays under the hood?",
            answer: "Over-allocates contiguous memory blocks; appending is O(1) amortized time.",
            analogy: "Reserving extra seats at a table in advance for future guests.",
            repetition_number: 1,
            interval_days: 1,
          },
        ],
      },
    ]);
  }
}

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const data = await runPythonBridge("/api/flashcards", "POST", body);
    return NextResponse.json(data);
  } catch {
    return NextResponse.json({ card_id: "card", interval_days: 1, easiness_factor: 2.5 });
  }
}
