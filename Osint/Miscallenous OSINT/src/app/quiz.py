import json
import sys

JSON_FILE = "questions.json"
FLAG_FILE = "/flag.txt"


def load_questions():
    """Load questions from JSON file."""
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("questions", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[!] Error loading questions: {e}")
        return []


def get_flag():
    """Read the flag from file."""
    try:
        with open(FLAG_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Flag not found."


def ask_questions():
    """Run the OSINT challenge interactively."""
    questions = load_questions()

    if not questions:
        print("No questions available. The archive sits silent.")
        return

    print("=" * 60)
    print("Welcome to the Miscellaneous OSINT Challenge.")
    print("=" * 60)

    for i, q in enumerate(questions, 1):
        question_text = q.get("question", "Unknown question")
        answers = {ans.lower() for ans in q.get("answers", [])}

        print(f"\n[Q{i}] {question_text}")
        user_input = input(">>> ").strip().lower()

        if user_input not in answers:
            print("\n[!] Incorrect answer.")
            print("The archive rejects you. Access terminated.")
            return

        print("[✓] Accepted. Proceed...")

    print("\nAll checkpoints cleared.")
    print("The archive recognizes your effort.")
    print("You’ve reached the end of the trail.\n")
    print(f"Flag: {get_flag()}")
    print("\n— End of Transmission —")


if __name__ == "__main__":
    ask_questions()
