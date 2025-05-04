"""Report on where the syllabus is running: CodeSpaces, League Codeserver, or local. """

import os
from pathlib import Path
import yaml

def where():
    """Return the environment where the syllabus is running."""
    if os.getenv('LEAGUE_CODESERVER'):
        return 'league-codeserver'
    elif os.getenv('CODESPACES'):
        return 'codespaces'
    else:
        return 'local'
    

def prune(where_cond: str, in_file: Path | str, out_file: Path | str):
    """Prune the syllabus, based on if the where condition in each lesson ie
    the same as the where condition of the current environment."""
    
    with open(in_file, 'r', encoding='utf-8') as file:
        syllabus = yaml.safe_load(file)

    def prune_dict(d):
        if isinstance(d, dict):
            if 'where' in d:
                if where_cond not in d['where'].split(','):
                    return None
            return {k: prune_dict(v) for k, v in d.items() if prune_dict(v) is not None}
        elif isinstance(d, list):
            return [prune_dict(item) for item in d if prune_dict(item) is not None]
        else:
            return d

    pruned_syllabus = prune_dict(syllabus)

    with open(out_file, 'w', encoding='utf-8') as file:
        yaml.safe_dump(pruned_syllabus, file)

