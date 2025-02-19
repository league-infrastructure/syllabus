"""

"""

import re
from pathlib import Path

from syllabus.models import *


def read_module(path: Path):
    """Read the files in a module directory and create a list of
    Lesson objects.
    
    """
    
    
    m = Module( name=path.stem)
    
    def clean_filename(filename: str) -> str:
        """Remove leading numbers and letters up to the first "_" or " "."""
        return re.sub(r'^[\d\w]*?[_ ]', '', filename)

    
    files = []
    
    for p in path.iterdir():
        
        if p.stem.lower() == 'readme':
            m.overview = str(p)
            continue
        
        if p.name in ('images', 'assets', '.git', '.DS_Store'):
            continue
        
        e = {
            'path': str(p),
            'name': p.stem,
            'key': clean_filename(p.stem),
        }
        
        files.append(e)
            
    # Group by key
    groups = {}
    for l in files:
        key = l['key']
        if key not in groups:
            groups[key] = []
        groups[key].append(l)
         
    
    def mk_lesson(e):
        
        sfx = Path(e['path']).suffix
        
        if sfx == '.md':
            return Lesson(name = e['key'], lesson=e['path'])
        elif sfx in ('.ipynb', '.py'):
            return Lesson(name = e['key'], exercise=e['path'])
        else:
            None
            
    lessons = []
    for k, g in groups.items():
        if len(g) > 1:
            l = LessonSet(name=k, lessons=[ mk_lesson(e) for e in g if mk_lesson(e) ])
        else:
            l = Lesson(**g[0])
            
        lessons.append(l)
        
    m.lessons = lessons
    
    return m
    
    
    
    