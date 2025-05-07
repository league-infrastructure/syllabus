"""
Does something ... 
"""
# pylint: disable=C0115  # missing-class-docstring

import re
from pathlib import Path
from collections import defaultdict
import math
from textwrap import dedent
import frontmatter


from syllabus.models import Lesson, LessonSet, Module, Course
from syllabus.util import( clean_filename, match_rank, match_rank_name, rand62,
                          replace_rank, extract_rank_string, extract_metadata_markdown, 
                          extract_metadata_notebook, insert_metadata_notebook )

def is_lesson(f: Path) -> bool:
    """Check if the file is a lesson. It is a lesson if it has a rank and
    an extension of (.ipynb, .md, or .py), or if it is a directory with a rank
    and no file in the directory has a rank. """
    
    if f.is_dir():
        return match_rank(f) and not any(match_rank(Path(d)) for d in f.iterdir())
    
    if f.suffix in ('.ipynb', '.md', '.py'):
        return match_rank(f)
    
    return False

def is_module(d: Path) -> bool:
    
    if d.is_dir():

        ranks = extract_rank_string(Path(d))
        pparts =ranks.split('/')
        if len(pparts) == 1:
            return True
        
    return False

def is_lesson_set(d: Path) -> bool:
    
    return d.is_dir() and not is_module(d) and not is_lesson(d)


def what_is(p: Path) -> str:
    """Determine if the path is a lesson, module, or lesson set."""
    
    if is_lesson(p):
        if p.is_dir():
            return 'LD'
        else:
            return 'LF'
    elif is_lesson_set(p):
        return 'SL'
    elif is_module(p):
        return 'MO'
    elif p.name == 'README.md':
        return 'RM'
    else:
        return 'UK'
  
    
def get_lesson_name(p: Path) -> str:
    """Get the name of the lesson from the path."""
    
    if p.is_dir():
        return clean_filename(p.stem)
    else:
        return clean_filename(p.name)


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
    course.uid = m.get('uid', rand62(8))
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

            last_container.lessons.append(Lesson.new_lesson(lesson_dir, dprtld) )
        else:
            if len(pparts) == 1:
                assert is_module(Path(dirpath)), f"Path {dirpath} is not a module"
                
                module = Module(name=clean_filename(dirpath.stem), path=ranks)  
                m = get_readme_metadata(dirpath)
                module.description =m.get('description')
                module.uid = m.get('uid')
                course.modules.append(module)
                omap[ranks] = module
                last_container = module
                
                
            else:
                assert is_lesson_set(Path(dirpath)), f"Path {dirpath} is not a lesson set"
                
                lesson_set = LessonSet(name=clean_filename(dirpath.stem), path=ranks)
                m = get_readme_metadata(dirpath)
                lesson_set.description = m.get('description')
                lesson_set.uid = m.get('uid')
                        
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
        """Remove the rank path from the object."""
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
    

def iterlessons(lesson_dir: Path):
    
    """Iterate over the lessons in the lesson directory."""
    
    lesson_dir = Path(lesson_dir)
    
    for (dirpath, dirnames, filenames) in lesson_dir.walk():
 
        if not match_rank(Path(dirpath)):
            continue # No rank, so skip this directory
       
        tp = what_is(Path(dirpath))
        
        yield tp, dirpath
       
        if tp == 'LD':
            continue
       
        for f in filenames:
            yield what_is(Path(f)), Path(dirpath, f)
       

def ensure_readme(p: Path, uid = None):
    """Ensure that a directory has a README.md"""
    
    from syllabus.cli.main import logger
    from syllabus.util import rand62

    if not p.is_dir():
        return
    
    readme_path = Path(p, 'README.md')

    uid = uid or rand62(8)
    
    if not readme_path.exists():
        
           
        text = dedent(f"""
        ---
        
        uid: {uid}
        
        ---
        
        # {clean_filename(p.stem)}
    
        """)
        
        with open(readme_path, 'w', encoding='utf-8') as file:
            file.write(text)

        logger.info("Create %s", readme_path.relative_to(p))
        
    else:
        # Load the README.md file
        with open(readme_path, 'r', encoding='utf-8') as file:
            post = frontmatter.load(file)

        # Ensure the frontmatter has a uid
        if 'uid' not in post.metadata:
            post.metadata['uid'] = uid

            # Save the updated README.md file
            frontmatter.dump(post, readme_path)

                
def metafy_lessons(lesson_dir: Path, dryrun: bool = True):
    """ Add metadata to lessons, modules and sets.
    
    Creates README.md files, or ads uids to existing READMEs, and
    ads metadata to ipynb and py files"""
    
    from syllabus.cli.main import logger
    from uuid import uuid4
    
    logger.debug("Metafy lessons in %s", lesson_dir)
    
    # The course gets a uuid4, for more randomness
    ensure_readme(lesson_dir, uid=str(uuid4()))
    
    for typ, p in iterlessons(lesson_dir):
        
        if typ == 'UK' and p.name == '.DS_Store': # I hate these files. 
            p.unlink()
        
        if p.is_dir():
            ensure_readme(p)
            
        if typ == 'LF':
            if p.suffix == '.ipynb':
                metadata = extract_metadata_notebook(p)
               
                if 'uid' not in metadata:
                    metadata['uid'] = metadata.get('uid', rand62(8))                
                    insert_metadata_notebook(p, metadata)
                    logger.info("Add uid to notebook %s", p.relative_to(lesson_dir))
                

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
    
    from syllabus.cli.main import logger

    
    
    logger.debug("Checking structure of %s", lesson_dir)
    
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
        