import json
import sys
import os
import time

JSON_FILE = "questions.json"
FLAG_FILE = "flag.txt"

BANNER = """
░███████                         ░██░██               ░███    ░██                                                ░██████                      
░██   ░██                           ░██               ░████   ░██                                               ░██   ░██                     
░██    ░██  ░███████  ░██    ░██ ░██░██  ░███████     ░██░██  ░██  ░███████  ░██    ░██  ░███████  ░██░████    ░██        ░██░████ ░██    ░██ 
░██    ░██ ░██    ░██ ░██    ░██ ░██░██ ░██           ░██ ░██ ░██ ░██    ░██ ░██    ░██ ░██    ░██ ░███        ░██        ░███     ░██    ░██ 
░██    ░██ ░█████████  ░██  ░██  ░██░██  ░███████     ░██  ░██░██ ░█████████  ░██  ░██  ░█████████ ░██         ░██        ░██      ░██    ░██ 
░██   ░██  ░██          ░██░██   ░██░██        ░██    ░██   ░████ ░██          ░██░██   ░██        ░██          ░██   ░██ ░██      ░██   ░███ 
░███████    ░███████     ░███    ░██░██  ░███████     ░██    ░███  ░███████     ░███     ░███████  ░██           ░██████  ░██       ░█████░██ 
                                                                                                                                          ░██ 
                                                                                                                                    ░███████  
                                                                                                                                              
"""


def load_questions():
    """Load questions from JSON file."""
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("questions", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading questions: {e}")
        return []

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_flag_animated(flag_content, delay=0.001):
    """Print flag line by line with animation effect."""
    lines = flag_content.split('\n')
    for line in lines:
        print(line, flush=True)
        time.sleep(delay)

def get_flag():
    """Read the flag from file with ANSI codes preserved."""
    try:
        with open(FLAG_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Flag not found."


def ask_questions():
    """Run the quiz interactively."""
    questions = load_questions()
    
    if not questions:
        print("No questions available.")
        return
    
    print(BANNER)
    print("The Sons of Sparda have left their mark across gaming history.")
    print("Prove your knowledge of the legendary demon hunters to claim your prize.\n")
    print("=" * 60)

    for i, q in enumerate(questions, 1):
        question_text = q.get("question", "Unknown question")
        answers = {ans.lower() for ans in q.get("answers", [])}

        print(f"\nQuestion {i}: {question_text}")
        print("Your answer: ", end="", flush=True)
        user_input = sys.stdin.readline().strip().lower()

        if user_input not in answers:
            print("This party's over! Looks like you weren't quite ready for this dance.")
            print("The blood of Sparda doesn't flow through your veins... yet.")
            return
    
    clear_screen()
    
    flag_content = get_flag()
    print_flag_animated(flag_content)
    
    print("\n" + "=" * 60)
    print("Now I'm motivated! You've proven yourself worthy.")


if __name__ == "__main__":
    ask_questions()