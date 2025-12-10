import os
import datetime
import argparse

# Configuration
LIFEOS_DIR = "/home/austin/Documents/LifeOS"
PROMPT_PATH = os.path.join(LIFEOS_DIR, "System", "Prompts", "virtual_mirror_prompt.md")
CALENDAR_PATH = os.path.join(LIFEOS_DIR, "calendar_dump.txt")
LOG_PATH = os.path.join(LIFEOS_DIR, "Log.md")
OUTPUT_PATH = os.path.join(LIFEOS_DIR, "Daily_Risk_Report.md")

def read_file(path):
    if not os.path.exists(path):
        return f"[Missing File: {path}]"
    with open(path, 'r') as f:
        return f.read()

def get_date_str():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def generate_prompt():
    # 1. Read System Prompt
    system_prompt = read_file(PROMPT_PATH)

    # 2. Read Context
    calendar_data = read_file(CALENDAR_PATH)
    # For Log, we might want just the last 50 lines if it's huge
    log_data = read_file(LOG_PATH)
    if len(log_data) > 2000:
        log_data = "..." + log_data[-2000:]

    # 3. Construct the Final Prompt
    final_prompt = f"""
{system_prompt}

---

# CURRENT CONTEXT FOR {get_date_str()}

## 1. CALENDAR (The Hard Landscape)
{calendar_data}

## 2. RECENT LOGS (The Residue)
{log_data}

---

# INSTRUCTION
Generate the **Daily Risk Report** now.
"""
    return final_prompt

def main():
    parser = argparse.ArgumentParser(description="Virtual Mirror: Daily Risk Report Generator")
    parser.add_argument("--dry-run", action="store_true", help="Print prompt to console instead of calling LLM")
    args = parser.parse_args()

    print(f"🔮 Virtual Mirror activating for {get_date_str()}...")
    
    prompt = generate_prompt()

    if args.dry_run:
        print("\n" + "="*40)
        print("GENERATED PROMPT:")
        print("="*40)
        print(prompt)
        print("="*40)
    else:
        # TODO: Connect to actual LLM API here.
        # For now, we will simulate a response or save the prompt to a file for manual processing.
        print("⚠️  LLM Integration not yet configured.")
        print("Saving prompt to 'virtual_mirror_input.txt' for manual processing.")
        with open("virtual_mirror_input.txt", "w") as f:
            f.write(prompt)

if __name__ == "__main__":
    main()
