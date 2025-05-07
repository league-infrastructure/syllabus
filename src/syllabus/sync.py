"""
Does something ... 
"""
# pylint: disable=C0115  # missing-class-docstring

import re
from pathlib import Path
from collections import defaultdict
import math

from syllabus.models import Lesson, LessonSet, Module, Course
from syllabus.util import clean_filename, match_rank, match_rank_name, replace_rank, extract_rank_string, extract_metadata_markdown

def is_lesson(f: Path) -> bool:
    """Check if the file is a lesson. It is a lesson if it has a rank and
    an extension of (.ipynb, .md, or .py), or if it is a directory with a rank
    and no file in the directory has a rank. """
    
    if f.is_dir():
        return match_rank(f) and not any(match_rank(Path(d)) for d in f.iterdir())
    
    if f.suffix in ('.ipynb', '.md', '.py'):
        return match_rank(f)
    
    return False


def get_readme_metadata(lesson_dir: Path) -> dict:
    """Get the metadata from the README.md file in the lesson directory."""
    
    readme_path = Path(lesson_dir, 'README.md')
    if readme_path.exists():
        
        # Get the first level 1 heading for the name
        heading1 = None
        with open(readme_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith('# '):  # Level 1 heading
                    heading1  = line[2:].strip()                
                    break
        
        metadata = extract_metadata_markdown(readme_path)
        metadata['name'] = metadata.get('name', heading1)
        return metadata
    
    return {}

def compile_syllabus(lesson_dir: Path) -> None:
    
    lesson_dir = Path(lesson_dir)
    
    course = Course(name='')
    m = get_readme_metadata(lesson_dir)

    course.description = m.get('description', course.description)
    course.name = m.get('name', course.name)
    
    omap = {}
    last_container = None
     
    for (dirpath, dirnames, filenames) in lesson_dir.walk():
 
        if not match_rank(Path(dirpath)):
            continue # No rank, so skip this directory


        dprtld = Path(dirpath).relative_to(lesson_dir)
        
        ranks = extract_rank_string(Path(dirpath))
        pparts =ranks.split('/')
        

        if is_lesson(Path(dirpath)):
            l =  Lesson.new_lesson(lesson_dir, dprtld) 
            last_container.lessons.append(l)
        else:
            if len(pparts) == 1:
                module = Module(name=clean_filename(dirpath.stem), path=ranks)  
                module.description = get_readme_metadata(dirpath).get('description')
                course.modules.append(module)
                omap[ranks] = module
                last_container = module
                
                
            else:
                lesson_set = LessonSet(name=clean_filename(dirpath.stem), path=ranks)
                
                lesson_set.description = get_readme_metadata(dirpath).get('description')
                        
                module = omap['/'.join(pparts[:-1])]
                module.lessons.append(lesson_set)
                omap[ranks] = lesson_set
                last_container = lesson_set
        
        
        for f in sorted(filenames):
            if is_lesson(Path(f)):
                l = Lesson.new_lesson(lesson_dir, Path(dirpath, f).relative_to(lesson_dir))
                last_container.lessons.append(l)
        

    # Because we added the lessons that are single files independently from lessons
    # that are directories, they won't have been added in srted order. So we need to sort them now.
    
    course.sort()
    
    def remove_path(obj):
        """Remove the path from the object."""
        if hasattr(obj, 'path'):
            del obj.path
        if hasattr(obj, 'lessons'):
            for lesson in obj.lessons:
                remove_path(lesson)
        elif hasattr(obj, 'modules'):
            for module in obj.modules:
                remove_path(module)
    
    remove_path(course)
    
    
    return course
    

def regroup_lessons(lesson_dir: Path, dryrun: bool = True):

    from syllabus.cli.main import logger
    
    check_structure(lesson_dir)
    
    lesson_dir = Path(lesson_dir)
    
    
    for (dirpath, dirnames, filenames) in lesson_dir.walk():
 
        if not match_rank(Path(dirpath)):
            continue # No rank, so skip this directory
        
        grouped = defaultdict(list)
        
        for f in filenames:
            rank, base = match_rank_name(Path(f))
            if rank:
                grouped[ f"{rank}_{base}" ].append(f)
            
        grouped = {k: v for k, v in grouped.items() if len(v) > 1}
            
        for k, v in grouped.items():
            logger.info("Group %s -> %s", k, v)
            
            # Create a new directory for the group
            new_dir = Path(dirpath, k)
          
            if not dryrun:
                new_dir.mkdir(parents=True, exist_ok=True)
            
            for f in v:
                old_path = Path(dirpath, f)
                new_path = Path(new_dir, str(replace_rank(Path(f), '')).strip('_'))
                
                # If the new path is a .md file, move it to README.md
                if new_path.suffix == '.md':
                    new_path = new_path.with_name('README.md')
                
                
                logger.info("Move %s to %s", old_path.relative_to(lesson_dir), new_path.relative_to(lesson_dir))
                
                
                
                if not dryrun:
                    old_path.rename(new_path)


def renumber_lessons(lesson_dir: Path, increment=1, dryrun: bool = True):
    
    
    from syllabus.cli.main import logger
    lesson_dir = Path(lesson_dir)
    
    check_structure(lesson_dir)
    
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
        
        all_names =  [f for f in filenames if match_rank(Path(f))] +  [d for d in dirnames if match_rank(Path(d)) ] 
        
        changes.extend(compile_changes(dirpath, all_names))
        
    
    # Delete all empty directories
    for dirpath, dirnames, filenames in lesson_dir.walk():
        for dirname in dirnames:
            dir_to_check = Path(dirpath, dirname)
            if not any(dir_to_check.iterdir()):  # Check if directory is empty
                logger.info("Deleting empty directory: %s", dir_to_check.relative_to(lesson_dir))
                if not dryrun:
                    dir_to_check.rmdir()
    
        
    for  depth, old_name, new_name in reversed(sorted(changes, key=lambda x: x[0])):
        logger.info("%d Rename %s to %s", depth, old_name.relative_to(lesson_dir), new_name.relative_to(lesson_dir))
        if not dryrun:
            try:
                old_name.rename(new_name)
            except OSError as e:
                logger.info("Error renaming %s to %s: %s", old_name.relative_to(lesson_dir), new_name.relative_to(lesson_dir), e)
                
def check_structure(lesson_dir: Path):
    """Check the structure of the lesson directory and return a list of
    LessonEntry objects.

    """
    lesson_dir = Path(lesson_dir)

    if not lesson_dir.is_dir():
        raise ValueError(f"{lesson_dir} is not a directory")


    # The top level of the lessons directory must contain only modules, 
    # which means (1) There are no files except a README.md, (2) all of the
    # directories have a rank. 

    for p in lesson_dir.iterdir():
        
        if p.name in ('.DS_Store', '.git', 'README.md'):
            continue
        
        if p.stem.startswith('.') or p.name.startswith('_'):
            continue
        
        
        if p.stem.lower() == 'readme':
            continue
        if not p.is_dir() and p.name != 'README.md':
            raise ValueError(f"{lesson_dir} contains files other than directories: {p}")
        if not match_rank(p):
            raise ValueError(f"{lesson_dir} contains directories without ranks: {p}")

    return True       
        
        
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
