"""
Does something ... 
"""
# pylint: disable=C0115  # missing-class-docstring

import re
from pathlib import Path

from syllabus.models import Lesson, LessonSet, Module, Course

assignment_exts = ['.py', '.ipynb', '.md', '.class','.java', '.cpp', '.c', '.h']

name_p = re.compile(r'^(\d+[A-Za-z]*)_([^\.]+)$')
rank_p = re.compile(r'^(\d+[A-Za-z]*)_')


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


class LessonEntry:
    
    def __init__(self, root: Path,  path:Path):
        
        self.root = root
        self.path = path
        
    @property
    def rpath(self):
        return self.path.relative_to(self.root)
        
    @property
    def stem(self):
        return self.path.stem
    
    @property
    def ext(self):
        return self.path.suffix
        
    @property
    def group(self):
        # For the group, take each part of the path and remove the rank, 
        # then on the last part, remove the extension
        
        parts = [ Path(p).stem for p in self.rpath.parts]
        return '/'.join(parts)
    
    @property
    def is_ranked_path(self, sf: Path) -> bool:
        """Check that the path specifies ranked path elements; 
        all path elements start with a number and an underscore.
        """
        
        return all(match_rank_name(Path(p)) for p in self.rpath.parts)
        
    @property
    def rank(self):
        if self.path.stem:
            match = rank_p.match(self.path.stem)
            if match:
                return match.group(1)
        return None


def clean_filename(filename: str) -> str:
    """Remove leading numbers and letters up to the first "_" or " "."""
    return re.sub(r'^[\d\w]*?[_ ]', '', filename).replace('_', ' ').replace('-', ' ')


def sync_syllabus(lesson_dir: Path, syllabus: Course) -> None:
    
    lesson_dir = Path(lesson_dir)
    
    for (dirpath, dirnames, filenames) in lesson_dir.walk():
 
        if not match_rank(Path(dirpath)):
            continue # No rank, so skip this directory
        
        no_ranks = not any(bool(match_rank(Path(f))) for f in filenames)
        
        print(no_ranks, dirpath)
            
        
        # Check if the directory is a module


def renumber_lessons(lesson_dir: Path, increment=1, dryrun: bool = True):
    
    import math
    lesson_dir = Path(lesson_dir)
    

    
    def compile_changes(dirpath, all_names):
        
        changes = []
        
        if len(all_names) == 0:
            return changes
        
        
        all_names.sort()
            
        max_n = max(len(all_names)*increment, 1)
        
        digits = math.ceil(math.log10(max_n))
        digits = max(digits, 2)
            
      
        for i, n in enumerate(all_names,1):
            
            i *= increment
            
            new_name = replace_rank(Path(n), str(i).zfill(digits))
            
            if str(n) == str(new_name):
                continue
            
            old_path = Path(dirpath, n)
            assert old_path.exists(), f"File {old_path} does not exist"
            
            depth = len(old_path.relative_to(lesson_dir).parts)
            
            changes.append((depth, old_path, Path(dirpath, new_name)))
        
        return changes
    
    changes = []
    
    changes.extend(compile_changes(lesson_dir, [d.relative_to(lesson_dir) for d in lesson_dir.iterdir() if match_rank(Path(d))] ))
    
    
    for (dirpath, dirnames, filenames) in lesson_dir.walk():
 
        if not match_rank(Path(dirpath)):
            continue # No rank, so skip this directory
        
        all_names =  [f for f in filenames if match_rank(Path(f))] +  [d for d in dirnames if match_rank(Path(d))] 
        
        changes.extend(compile_changes(dirpath, all_names))
        
            
        
    for  depth, old_name, new_name in reversed(sorted(changes, key=lambda x: x[0])):
        if dryrun:
            print(f"{depth} Rename {old_name.relative_to(lesson_dir)} to {new_name.relative_to(lesson_dir)}")
        else:
            try:
                old_name.rename(new_name)
            except Exception as e:
                print(f"Error renaming {old_name.relative_to(lesson_dir)} to {new_name.relative_to(lesson_dir)}: {e}")
                
    
        
        
        
    
    


def read_module(path: Path, group: bool = False) -> Module:
    """Read the files in a module directory and create a list of
    Lesson objects.

    """

    overview = None


    def mk_lesson(e):

        sfx = Path(e['path']).suffix

        if sfx == '.md':
            return Lesson(name=e['name'], lesson=e['path'])
        if sfx in ('.ipynb', '.py'):
            with open(e['path'], 'r', encoding='utf-8') as file:
                content = file.read()
                display = any(re.search(r'\b' + lib + r'\b', content)
                              for lib in ['turtle', 'zerogui', 'pygame', 'tkinter'])

            return Lesson(name=e['name'], exercise=e['path'], display=display)
        return None

    files = []

    for p in sorted(path.iterdir()):

        if p.stem.lower() == 'readme':
            overview = str(p)
            continue

        if p.name in ('images', 'assets', '.git', '.DS_Store'):
            continue

        e = {
            'path': str(p),
            'name': clean_filename(p.stem),

        }

        files.append(e)

    def match_partner(s, l):
        """Determine if there is an existing lesson that we can pair with the current lesson."""
        for e in s:
            if l.lesson and e.exercise and not e.lesson:
                e.lesson = l.lesson
                e.display = l.display or e.display
                return e
            elif l.exercise and e.lesson and not e.exercise:
                e.exercise = l.exercise
                e.display = l.display or e.display
                return e

        return None

    # Group by key
    if group:
        groups = {}
        for e in files:

            key = e['name']
            if key not in groups:
                groups[key] = []

            m = match_partner(groups[key], mk_lesson(e))
            if not m:
                groups[key].append(mk_lesson(e))

    else:
        groups = {e['path']: [mk_lesson(e)] for e in files}

    lessons = []
    for k, g in groups.items():
        if len(g) > 1:
            l = LessonSet(name=k, lessons=g)
        else:
            l = g[0]

        if l:
            lessons.append(l)

    return Module(name=path.stem, overview=overview, lessons=lessons)
