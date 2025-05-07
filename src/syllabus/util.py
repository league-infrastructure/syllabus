import re
from pathlib import Path
import frontmatter
import json
import string
import random

name_p = re.compile(r'^(\d+[A-Za-z]*)_([^\.]+)$')
assignment_exts = ['.py', '.ipynb', '.md', '.class','.java', '.cpp', '.c', '.h']
rank_p = re.compile(r'^(\d+[A-Za-z]*)_')


# rexeexes that indicate that the file will require a display
display_p = [ re.compile(r'\bturtle\b'), re.compile(r'\bzerogui\b'), re.compile(r'\bpygame\b'), 
              re.compile(r'\btkinter') ]


def rand62(n: int) -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=n))

def clean_filename(filename: str) -> str:
    """Remove leading numbers and letters up to the first "_" or " "."""

    return re.sub(rank_p, '', filename).replace('_', ' ').replace('-', ' ')


def extract_metadata_python(p: Path) -> dict:
    """Extract metadata from a Python file."""
    metadata = {}
    with open(p, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('#') and ':' in line:
                match = re.match(r'^#\s+(\w+):\s*(.*)', line)
                if match:
                    key, value = match.groups()
                    metadata[key.strip()] = value.strip()
    return metadata

def extract_metadata_markdown(p: Path) -> dict:
    """ Return the frontmatter"""
    
    with open(p, 'r', encoding='utf-8') as file:
        return frontmatter.load(file).metadata
        
def extract_metadata_notebook(p: Path) -> dict:
    """Extract metadata from a jupyter notebook file."""
    with open(p, 'r', encoding='utf-8') as file:
        notebook = json.load(file)
        metadata = notebook.get('metadata', {}).get('syllabus', {})
        return metadata
    
    
def insert_metadata_notebook(p: Path, metadata: dict) -> None:
    """Insert metadata into a jupyter notebook file."""
    with open(p, 'r', encoding='utf-8') as file:
        notebook = json.load(file)
        
        if 'syllabus' not in notebook['metadata']:
            notebook['metadata']['syllabus'] = {}
        
        notebook['metadata']['syllabus'] = metadata
    
    with open(p, 'w', encoding='utf-8') as file:
        json.dump(notebook, file, indent=2)
        
        
    
def extract_metadata(p: Path) -> dict:
    """Extract metadata from a file."""
    if p.suffix == '.ipynb':
        return extract_metadata_notebook(p)
    elif p.suffix == '.md':
        return extract_metadata_markdown(p)
    elif p.suffix == '.py':
        return extract_metadata_python(p)
    else:
        return {}


def match_rank_name(f: Path) -> str:

    match = name_p.match(f.stem)
    if match:
        rank, base = match.groups()
        return rank, base
    else:
        return None, None


def match_rank(f: Path) -> str:
    match = rank_p.match(f.stem)
    if match:
        rank = match.group(1)
        return rank
    else:
        return None


def replace_rank(f: Path, rank: str) -> Path:
    """Replace the rank in the filename with the new rank."""
    old_rank = match_rank(f)

    if not old_rank:
        return f

    return f.with_stem(f.stem.replace(old_rank, rank, 1))

def extract_rank_string(p: Path) -> str:
    """ Extract the rank from each components of the path and
    return a path composed of just the ranks"""
    
    return str(Path(*[match_rank(Path(f)) for f in p.parts if match_rank(Path(f))]))
