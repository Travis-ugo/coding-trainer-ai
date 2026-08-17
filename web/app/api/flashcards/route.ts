import { NextResponse } from "next/server";
import { execSync } from "child_process";

export async function GET() {
  try {
    const output = execSync(
      `python3 -c "
from coding_trainer_ai.srs import DeckRepository
import json
repo = DeckRepository()
decks_data = []
for deck_id, deck in repo.decks.items():
    cards_data = [{'card_id': c.card_id, 'prompt': c.prompt, 'answer': c.answer, 'analogy': c.analogy, 'repetition_number': c.repetition_number, 'interval_days': c.interval_days} for c in deck.cards]
    decks_data.append({'id': deck.deck_id, 'title': deck.title, 'cards': cards_data})
print(json.dumps(decks_data))
"`,
      { cwd: "/Users/travis/Software/coding-trainer-ai" }
    ).toString();

    return NextResponse.json(JSON.parse(output));
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
    const cardId = body.card_id;
    const rating = body.rating || 4;

    const output = execSync(
      `python3 -c "
from coding_trainer_ai.srs import DeckRepository, SM2Engine
import json
repo = DeckRepository()
sm2 = SM2Engine()
updated = None
for deck in repo.decks.values():
    for card in deck.cards:
        if card.card_id == '${cardId}':
            updated = sm2.calculate_next_interval(card, ${rating})
            break
print(json.dumps({'card_id': '${cardId}', 'interval_days': updated.interval_days if updated else 1, 'easiness_factor': updated.easiness_factor if updated else 2.5}))
"`,
      { cwd: "/Users/travis/Software/coding-trainer-ai" }
    ).toString();

    return NextResponse.json(JSON.parse(output));
  } catch {
    return NextResponse.json({ card_id: "card", interval_days: 1, easiness_factor: 2.5 });
  }
}
