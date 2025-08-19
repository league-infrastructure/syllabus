import re
from pathlib import Path
import frontmatter
import json
import string
import random
import ast

name_p = re.compile(r'^(\d+[A-Za-z]*)_([^\.]+)$')
assignment_exts = ['.py', '.ipynb', '.md', '.class','.java', '.cpp', '.c', '.h']
rank_p = re.compile(r'^(\d+[A-Za-z]*)_')

# List of module names that indicate the file will require a display
display_modules = ['turtle', 'guizero', 'pygame', 'tkinter']

def get_imports(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        node = ast.parse(file.read(), filename=filepath)
    imports = set()

    for n in ast.walk(node):
        if isinstance(n, ast.Import):
            for alias in n.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(n, ast.ImportFrom):
            if n.module is not None:
                imports.add(n.module.split('.')[0])
    
    return sorted(imports)
                
def needs_display(filepath):
    
    return len(set(get_imports(filepath)).intersection(display_modules)) > 0
                  
def rand62(n: int) -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=n))

def clean_filename(filename: str) -> str:
    """Remove leading numbers and letters up to the first "_" or " "."""

    return re.sub(rank_p, '', filename).replace('_', ' ').replace('-', ' ')


def extract_metadata_python(p: Path, with_doc: bool = False):
    """Extract metadata from a Python file.

    Scans (1) the module docstring for lines of the form ``key: value`` and
    (2) top-level comment lines beginning with ``# key: value``. Comment lines
    override docstring values on key collisions.

    Args:
        p: Path to the Python file.
        with_doc: If True, also return the module docstring content with any
            metadata ``key: value`` lines removed (preserving order of the
            remaining lines and trimming leading/trailing blank lines).

    Returns:
        If ``with_doc`` is False (default): ``dict`` of metadata.
        If ``with_doc`` is True: ``(metadata_dict, cleaned_docstring_text)``.
    """
    metadata: dict[str, str] = {}
    cleaned_doc = ''

    text = p.read_text(encoding='utf-8')

    # Parse module docstring for key: value lines.
    try:
        module = ast.parse(text, filename=str(p))
        if module.body and isinstance(module.body[0], ast.Expr) and isinstance(module.body[0].value, ast.Constant) and isinstance(module.body[0].value.value, str):
            docstring = module.body[0].value.value
            preserved_lines = []
            for line in docstring.splitlines():
                m = re.match(r'^(\w+):\s*(.*)$', line.strip())
                if m:
                    k, v = m.groups()
                    metadata[k] = v
                else:
                    preserved_lines.append(line)
            cleaned_doc = '\n'.join(l for l in preserved_lines).strip('\n')
    except SyntaxError:
        pass  # fall through; metadata may still come from comments

    # Also parse YAML-ish comment lines beginning with '# key: value'
    for line in text.splitlines():
        if line.startswith('#') and ':' in line:
            match = re.match(r'^#\s+(\w+):\s*(.*)', line)
            if match:
                key, value = match.groups()
                metadata[key.strip()] = value.strip()

    if with_doc:
        return metadata, cleaned_doc
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
        
        
def insert_metadata_python(p: Path, metadata: dict) -> None:
    """Insert or update metadata inside the module docstring of a Python file.

    Metadata is appended (or updated) as simple `key: value` lines at the END
    of the module docstring (no --- delimiters). If the file has no module
    docstring, one is created at the top.
    """
    original_text = p.read_text(encoding='utf-8')

    # 1) Get existing metadata + cleaned docstring text (without metadata lines)
    try:
        existing_md, cleaned_doc = extract_metadata_python(p, with_doc=True)  # type: ignore[arg-type]
    except Exception:
        existing_md, cleaned_doc = {}, ''

    # 2) Merge metadata (new overrides old)
    merged = {**existing_md, **metadata}

    def build_metadata_block(md: dict[str, str]) -> str:
        return '\n'.join(f"{k}: {v}" for k, v in md.items())

    # Construct new docstring body: preserved text then blank line then metadata
    body_lines = []
    if cleaned_doc.strip():
        body_lines.append(cleaned_doc.strip())
        body_lines.append('')  # blank line separator
    body_lines.append(build_metadata_block(merged))
    new_docstring_text = '\n'.join(body_lines).rstrip() + '\n'

    new_docstring_block = f'"""\n{new_docstring_text}"""\n\n'

    # 3) Remove the existing module docstring block from file text (if present)
    try:
        module = ast.parse(original_text, filename=str(p))
        if module.body and isinstance(module.body[0], ast.Expr) and isinstance(module.body[0].value, ast.Constant) and isinstance(module.body[0].value.value, str):
            docnode = module.body[0]
            lines = original_text.splitlines()
            start = docnode.lineno - 1
            end = getattr(docnode, 'end_lineno', docnode.lineno) - 1
            # Remove those lines
            del lines[start:end+1]
            remainder = '\n'.join(lines).lstrip('\n')  # trim leading blank lines after removal
        else:
            remainder = original_text.lstrip('\n')
    except SyntaxError:
        remainder = original_text

    # 4) Write new file content with reconstructed docstring at top
    p.write_text(new_docstring_block + remainder, encoding='utf-8')
        
        
    
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
