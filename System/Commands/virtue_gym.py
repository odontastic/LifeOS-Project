#!/usr/bin/env python3
"""
The Dynamic Virtue Gym - Adaptive Curriculum Generator
Generates custom micro-protocols based on today's struggles.
"""

import os
import argparse
import datetime

LIFEOS_DIR = "/home/austin/Documents/LifeOS"
PROMPT_PATH = os.path.join(LIFEOS_DIR, "System", "Prompts", "virtue_gym_prompt.md")
TOOLKIT_PATH = os.path.join(LIFEOS_DIR, "System", "Personal-Transformation-Toolkit.md")
LOG_PATH = os.path.join(LIFEOS_DIR, "Log.md")
PROTOCOLS_DIR = os.path.join(LIFEOS_DIR, "System", "Protocols")

def read_file(path):
    if not os.path.exists(path):
        return ""
    with open(path, 'r') as f:
        return f.read()

def display_header():
    print("""
╔════════════════════════════════════════════════════════════╗
║         🏋️  DYNAMIC VIRTUE GYM  🏋️                        ║
║         Adaptive Curriculum Generator                      ║
╚════════════════════════════════════════════════════════════╝
""")

def get_struggle():
    print("📝 What was your struggle today?")
    print("   (Be specific: What happened? When? With whom?)\n")
    struggle = input("> ").strip()
    return struggle

def generate_prompt(struggle, toolkit_excerpt=""):
    system_prompt = read_file(PROMPT_PATH)
    
    final_prompt = f"""
{system_prompt}

---

# TODAY'S STRUGGLE
"{struggle}"

# CONTEXT FROM TRANSFORMATION TOOLKIT
{toolkit_excerpt[:2000] if toolkit_excerpt else "[Toolkit not loaded]"}

---

# INSTRUCTION
Generate the custom Virtue Gym protocol for tomorrow.
"""
    return final_prompt

def save_protocol(protocol_content, virtue_name):
    """Save the generated protocol to a file"""
    os.makedirs(PROTOCOLS_DIR, exist_ok=True)
    today = datetime.date.today().strftime("%Y-%m-%d")
    filename = f"{today}-{virtue_name.lower().replace(' ', '-')}-protocol.md"
    filepath = os.path.join(PROTOCOLS_DIR, filename)
    
    with open(filepath, 'w') as f:
        f.write(protocol_content)
    
    return filepath

def main():
    parser = argparse.ArgumentParser(description="Dynamic Virtue Gym: Adaptive Curriculum")
    parser.add_argument("--dry-run", action="store_true", help="Print prompt to console")
    parser.add_argument("--struggle", help="Provide struggle directly instead of interactive input")
    args = parser.parse_args()

    display_header()
    
    # Get the struggle
    if args.struggle:
        struggle = args.struggle
    else:
        struggle = get_struggle()
    
    if not struggle:
        print("❌ No struggle provided. Exiting.")
        return
    
    print(f"\n🎯 Processing: \"{struggle}\"")
    
    # Load toolkit for context
    toolkit = read_file(TOOLKIT_PATH)
    
    # Generate prompt
    prompt = generate_prompt(struggle, toolkit)
    
    if args.dry_run:
        print("\n" + "-"*40)
        print("GENERATED PROMPT FOR LLM:")
        print("-"*40)
        print(prompt)
        print("-"*40)
    else:
        print("\n⚠️  LLM Integration not yet configured.")
        print("Saving prompt to 'virtue_gym_input.txt'.")
        print("\n📋 NEXT STEPS:")
        print("1. Copy the prompt into your AI")
        print("2. The AI will generate your custom micro-protocol")
        print("3. Save the protocol to System/Protocols/")
        with open("virtue_gym_input.txt", "w") as f:
            f.write(prompt)
        
        print("\n💡 TIP: Add the protocol to your morning calibration!")

if __name__ == "__main__":
    main()
