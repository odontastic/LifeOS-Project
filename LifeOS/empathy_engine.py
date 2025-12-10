#!/usr/bin/env python3
"""
The Empathy Engine - Wife Conversation Simulator
Practice difficult conversations before they happen.
"""

import os
import argparse

LIFEOS_DIR = "/home/austin/Documents/LifeOS"
PROMPT_PATH = os.path.join(LIFEOS_DIR, "System", "Prompts", "empathy_engine_prompt.md")

def read_file(path):
    if not os.path.exists(path):
        return ""
    with open(path, 'r') as f:
        return f.read()

def display_header():
    print("""
═══════════════════════════════════════════════════════════════
💬 EMPATHY ENGINE - CONVERSATION SIMULATOR
═══════════════════════════════════════════════════════════════
Practice difficult conversations. Get real-time feedback.
Type 'quit' to exit.
═══════════════════════════════════════════════════════════════
""")

def get_scenario():
    print("📋 SCENARIO OPTIONS:")
    print("  1. She's upset because I forgot something important.")
    print("  2. She's anxious about finances.")
    print("  3. She's hurt because I was dismissive.")
    print("  4. [Custom] Enter your own scenario.")
    print("")
    
    choice = input("Choose scenario (1-4): ").strip()
    
    scenarios = {
        "1": "Your wife is upset because you forgot to pick up Matthew from practice. She had to leave work early.",
        "2": "Your wife is anxious because she saw an unexpected charge on the credit card.",
        "3": "Your wife is hurt because when she tried to share something with you, you were on your phone.",
        "4": None
    }
    
    if choice == "4":
        return input("Describe the scenario: ").strip()
    return scenarios.get(choice, scenarios["1"])

def generate_prompt(scenario, user_response):
    system_prompt = read_file(PROMPT_PATH)
    
    final_prompt = f"""
{system_prompt}

---

# THE SCENARIO
{scenario}

# USER'S RESPONSE TO HIS WIFE
"{user_response}"

---

# INSTRUCTION
1. First, respond AS THE WIFE to his statement.
2. Then, provide [COACH FEEDBACK] on his response.
"""
    return final_prompt

def main():
    parser = argparse.ArgumentParser(description="Empathy Engine: Conversation Simulator")
    parser.add_argument("--dry-run", action="store_true", help="Print prompt instead of simulating")
    args = parser.parse_args()

    display_header()
    
    scenario = get_scenario()
    print(f"\n📍 SCENARIO: {scenario}\n")
    print("═══════════════════════════════════════════════════════════════")
    
    while True:
        print("\n👤 YOUR RESPONSE (what would you say to her?):")
        user_response = input("> ").strip()
        
        if user_response.lower() == 'quit':
            print("\n✨ Practice makes progress. Go be present.")
            break
        
        prompt = generate_prompt(scenario, user_response)
        
        if args.dry_run:
            print("\n" + "-"*40)
            print("GENERATED PROMPT FOR LLM:")
            print("-"*40)
            print(prompt)
            print("-"*40)
        else:
            print("\n⚠️  LLM Integration not yet configured.")
            print("Saving prompt to 'empathy_engine_input.txt'.")
            print("Copy this into your AI and paste the response here.\n")
            with open("empathy_engine_input.txt", "w") as f:
                f.write(prompt)
            
            print("📋 Prompt saved. Paste the AI's response below (or type 'skip'):")
            ai_response = input("> ").strip()
            if ai_response.lower() != 'skip':
                print("\n" + "─"*50)
                print("👩 WIFE'S RESPONSE + COACH FEEDBACK:")
                print("─"*50)
                print(ai_response)
                print("─"*50)
        
        print("\nTry again with the same scenario? (Press ENTER to continue, or type 'quit')")

if __name__ == "__main__":
    main()
