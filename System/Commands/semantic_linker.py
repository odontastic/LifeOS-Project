import os
import re
import yaml
from pathlib import Path

ROOT_DIR = "/home/austin/Documents/LifeOS"
EXCLUDE_DIRS = {'.git', '.obsidian', 'node_modules', '.gemini', '.agent'}

def get_all_files():
    files = []
    for root, dirs, filenames in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for filename in filenames:
            if filename.endswith('.md'):
                files.append(os.path.join(root, filename))
    return files

def parse_frontmatter(content):
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if match:
        try:
            data = yaml.safe_load(match.group(1))
            if isinstance(data, dict):
                return data, match.end()
            return {}, match.end() # Return empty dict if YAML is valid but not a dict (e.g. list or string)
        except yaml.YAMLError:
            return {}, 0
    return {}, 0

def get_file_type(path):
    rel_path = os.path.relpath(path, ROOT_DIR)
    if rel_path.startswith('Projects'): return 'Project'
    if rel_path.startswith('Areas'): return 'Area'
    if rel_path.startswith('Resources'): return 'Resource'
    if rel_path.startswith('GTD-Tasks'): return 'Task'
    if rel_path.startswith('System'): return 'System'
    return 'Note'

def get_up_link(path):
    rel_path = os.path.relpath(path, ROOT_DIR)
    parts = rel_path.split(os.sep)
    if len(parts) > 1:
        parent_dir = os.path.dirname(rel_path)
        # Check if parent has an index file
        index_path = os.path.join(ROOT_DIR, parent_dir, '00-Index.md')
        if os.path.exists(index_path):
            return f"[[{parent_dir}/00-Index]]"
        return f"[[{parent_dir}]]"
    return ""

def build_index(files):
    title_map = {}
    filename_map = {}
    for f in files:
        with open(f, 'r') as file:
            content = file.read()
            fm, _ = parse_frontmatter(content)
            title = fm.get('title')
            if title:
                title_map[title.lower()] = f
            
            basename = os.path.basename(f)
            filename_map[basename] = f
            filename_map[os.path.splitext(basename)[0]] = f
            
    return title_map, filename_map

def fix_links(content, filename_map, current_file):
    def replace_link(match):
        link_text = match.group(1)
        # Handle piped links [[target|text]]
        target = link_text.split('|')[0]
        alias = link_text.split('|')[1] if '|' in link_text else None
        
        # Clean target
        clean_target = os.path.basename(target)
        if clean_target.endswith('.md'):
            clean_target = clean_target[:-3]
            
        # Try to find target in map
        if clean_target in filename_map:
            abs_path = filename_map[clean_target]
            rel_path = os.path.relpath(abs_path, ROOT_DIR)
            # Remove extension for cleaner links
            rel_path_no_ext = os.path.splitext(rel_path)[0]
            
            if alias:
                return f"[[{rel_path_no_ext}|{alias}]]"
            return f"[[{rel_path_no_ext}]]"
            
        return match.group(0)

    # Regex for [[wiki-links]]
    return re.sub(r'\[\[(.*?)\]\]', replace_link, content)

def semantic_link(content, title_map, current_file):
    # Don't link to self
    current_title = os.path.splitext(os.path.basename(current_file))[0].lower()
    
    for title, path in title_map.items():
        if title == current_title:
            continue
            
        # Simple exact match, word boundary
        # Avoid matching inside existing links
        pattern = re.compile(r'(?<!\[\[)(?<!\[)\b' + re.escape(title) + r'\b(?!\]\])(?!\])', re.IGNORECASE)
        
        def replace_match(match):
            rel_path = os.path.relpath(path, ROOT_DIR)
            rel_path_no_ext = os.path.splitext(rel_path)[0]
            return f"[[{rel_path_no_ext}|{match.group(0)}]]"
            
        content = pattern.sub(replace_match, content)
        
    return content

def process_files():
    files = get_all_files()
    title_map, filename_map = build_index(files)
    
    for f in files:
        with open(f, 'r') as file:
            content = file.read()
            
        fm, content_start = parse_frontmatter(content)
        body = content[content_start:]
        
        # 1. Fix Links
        body = fix_links(body, filename_map, f)
        
        # 2. Semantic Linking (Skip for now to avoid over-linking, or be very selective)
        # body = semantic_link(body, title_map, f) 
        
        # 3. Standardize Metadata
        new_fm = fm.copy()
        if 'title' not in new_fm:
            new_fm['title'] = os.path.splitext(os.path.basename(f))[0].replace('-', ' ').title()
        
        new_fm['type'] = get_file_type(f)
        
        up_link = get_up_link(f)
        if up_link:
            new_fm['up'] = up_link
            
        # Write back
        with open(f, 'w') as file:
            file.write('---\n')
            yaml.dump(new_fm, file, default_flow_style=None, sort_keys=False)
            file.write('---\n')
            file.write(body)

if __name__ == "__main__":
    process_files()
