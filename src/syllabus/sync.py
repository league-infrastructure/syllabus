"""
Does something ... 
"""

import re
from pathlib import Path

from syllabus.models import Lesson, LessonSet, Module


def read_module(path: Path, group: bool = False) -> Module:
    """Read the files in a module directory and create a list of
    Lesson objects.

    """

    overview = None

    def clean_filename(filename: str) -> str:
        """Remove leading numbers and letters up to the first "_" or " "."""
        return re.sub(r'^[\d\w]*?[_ ]', '', filename).replace('_', ' ').replace('-', ' ')

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
