import os
import re
import argparse

# Configuration
LIFEOS_DIR = "/home/austin/Documents/LifeOS"
LOG_PATH = os.path.join(LIFEOS_DIR, "Log.md")
PROMPT_PATH = os.path.join(LIFEOS_DIR, "System", "Prompts", "pattern_hunter_prompt.md")

NEGATIVE_KEYWORDS = ["missed", "failed", "argued", "yelled", "tired", "forgot", "anxious", "angry", "struggle"]

def read_file(path):
    if not os.path.exists(path):
        return ""
    with open(path, 'r') as f:
        return f.read()

def extract_negative_entries(log_content):
    entries = []
    lines = log_content.splitlines()
    current_date = "Unknown Date"
    
    for line in lines:
        if line.startswith("# "):
            current_date = line.strip()
        
        # Check for keywords
        if any(keyword in line.lower() for keyword in NEGATIVE_KEYWORDS):
            entries.append(f"[{current_date}] {line.strip()}")
            
    return "\n".join(entries)

def generate_prompt(negative_entries):
    system_prompt = read_file(PROMPT_PATH)
    
    final_prompt = f"""
{system_prompt}

---

# NEGATIVE LOG ENTRIES (LAST 30 DAYS)
{negative_entries}

---

# INSTRUCTION
Analyze the above logs and generate the **Pattern Report**.
"""
    return final_prompt

def main():
    parser = argparse.ArgumentParser(description="Pattern Hunter: Root Cause Analysis")
    parser.add_argument("--dry-run", action="store_true", help="Print prompt to console")
    args = parser.parse_args()

    print("🕵️‍♂️ Pattern Hunter activating...")
    
    # 1. Read Log
    log_content = read_file(LOG_PATH)
    if not log_content:
        print("📭 Log is empty.")
        return

    # 2. Filter
    negative_entries = extract_negative_entries(log_content)
    if not negative_entries:
        print("✅ No negative entries found! You are doing great.")
        return
        
    print(f"📉 Found {len(negative_entries.splitlines())} negative entries.")

    # 3. Generate Prompt
    prompt = generate_prompt(negative_entries)

    if args.dry_run:
        print("\n" + "-"*40)
        print("GENERATED PROMPT FOR LLM:")
        print("-"*40)
        print(prompt)
        print("-"*40)
    else:
        # TODO: Connect to LLM
        print("⚠️  LLM Integration not yet configured.")
        print("Saving prompt to 'pattern_hunter_input.txt'.")
        with open("pattern_hunter_input.txt", "w") as f:
            f.write(prompt)

if __name__ == "__main__":
    main()
