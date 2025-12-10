import os
import re
import argparse
import json
import datetime
import yaml

# Configuration
LIFEOS_DIR = "/home/austin/Documents/LifeOS"
INBOX_PATH = os.path.join(LIFEOS_DIR, "Inbox.md")
PROMPT_PATH = os.path.join(LIFEOS_DIR, "System", "Prompts", "omni_triage_prompt.md")
TO_READ_PATH = os.path.join(LIFEOS_DIR, "Resources", "Lists", "to_read_list.md")
TO_WATCH_PATH = os.path.join(LIFEOS_DIR, "Resources", "Lists", "to_watch_list.md")

def print_cheat_sheet():
    print("\n" + "="*50)
    print("🚀 OMNI-TRIAGE CHEAT SHEET (PARA + GTD)")
    print("="*50)
    print("1. PROJECT  : Has a deadline? Has an outcome? (e.g., 'Finish Report')")
    print("2. AREA     : Ongoing standard? No end date? (e.g., 'Health', 'Finances')")
    print("3. RESOURCE : Useful info? No action needed? (e.g., 'Book Notes')")
    print("4. TASK     : Single step? Actionable? (e.g., 'Call Mom')")
    print("="*50 + "\n")

def read_file(path):
    if not os.path.exists(path):
        return ""
    with open(path, 'r') as f:
        return f.read()

def generate_prompt(inbox_content):
    system_prompt = read_file(PROMPT_PATH)
    
    final_prompt = f"""
{system_prompt}

---

# RAW INPUT (INBOX)
{inbox_content}

---

# INSTRUCTION
Process the above input and return the JSON object.
"""
    return final_prompt

def create_file_with_frontmatter(filepath, frontmatter, content):
    """Create a markdown file with YAML frontmatter"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w') as f:
        f.write('---\n')
        yaml.dump(frontmatter, f, default_flow_style=False, sort_keys=False)
        f.write('---\n\n')
        f.write(content)
    
    return filepath

def append_to_reading_list(item, list_type="to_read"):
    """Append a reference to the To Read or To Watch list"""
    list_path = TO_READ_PATH if list_type == "to_read" else TO_WATCH_PATH
    
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    entry = f"""
### [{item['title']}]
**Source:** {item.get('author', 'Unknown')}
**Category:** {', '.join(item.get('category', ['Uncategorized']))}
**Added:** {today}
**Priority:** {item.get('priority', 'Medium')}
**Status:** Not Started

**Why:** {item.get('why', 'Added via Omni-Triage')}

{"**⚠️ RESEARCH RECOMMENDED**: Knowledge gap detected - consider deep AI-driven research on this topic" if item.get('research_recommended') else ''}

---
"""
    
    with open(list_path, 'a') as f:
        f.write(entry)
    
    return list_path

def process_items(items_json):
    """Process the JSON items and create the actual files"""
    results = []
    
    for item in items_json['items']:
        item_type = item['type']
        
        if item_type == 'Reference':
            # Append to reading/watching list
            list_type = item.get('target_list', 'to_read_list')
            list_type = "to_read" if "read" in list_type else "to_watch"
            path = append_to_reading_list(item, list_type)
            results.append(f"✓ Added '{item['title']}' to {list_type} list")
            
        elif item_type in ['Task', 'Project']:
            # Create file with frontmatter
            filename = item['filename']
            target_dir = os.path.join(LIFEOS_DIR, item['target_dir'])
            filepath = os.path.join(target_dir, filename)
            
            frontmatter = item['frontmatter']
            content = item.get('content', '')
            
            create_file_with_frontmatter(filepath, frontmatter, content)
            results.append(f"✓ Created {item_type}: {filepath}")
    
    return results

def main():
    parser = argparse.ArgumentParser(description="Omni-Triage: AI-Powered PARA-GTD Intake")
    parser.add_argument("--dry-run", action="store_true", help="Print prompt to console")
    parser.add_argument("--execute", action="store_true", help="Execute file creation from JSON (requires --json-file)")
    parser.add_argument("--json-file", help="Path to JSON file with triage results")
    args = parser.parse_args()

    # 1. Show Cheat Sheet
    print_cheat_sheet()

    if args.execute and args.json_file:
        # Execute mode: create files from JSON
        print(f"📂 Processing JSON file: {args.json_file}")
        with open(args.json_file, 'r') as f:
            items_json = json.load(f)
        
        results = process_items(items_json)
        print("\n✅ PROCESSING COMPLETE:")
        for result in results:
            print(f"  {result}")
        return

    # 2. Read Inbox
    inbox_content = read_file(INBOX_PATH)
    if not inbox_content.strip():
        print("📭 Inbox is empty. Nothing to triage.")
        return

    print(f"📥 Found {len(inbox_content.splitlines())} lines in Inbox.")
    print("🧠 Processing with AI...")

    # 3. Generate Prompt
    prompt = generate_prompt(inbox_content)

    if args.dry_run:
        print("\n" + "-"*40)
        print("GENERATED PROMPT FOR LLM:")
        print("-"*40)
        print(prompt)
        print("-"*40)
    else:
        # TODO: Connect to LLM
        print("⚠️  LLM Integration not yet configured.")
        print("Saving prompt to 'omni_triage_input.txt'.")
        print("\n📋 NEXT STEPS:")
        print("1. Copy prompt into your AI")
        print("2. Save the JSON response to a file (e.g., 'triage_result.json')")
        print("3. Run: python3 omni_triage.py --execute --json-file triage_result.json")
        with open("omni_triage_input.txt", "w") as f:
            f.write(prompt)

if __name__ == "__main__":
    main()
