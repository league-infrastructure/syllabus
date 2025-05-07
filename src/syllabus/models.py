
import json
import re
from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel

from syllabus.util import clean_filename, display_p, extract_rank_string

def to_yaml(m, simplify=False):
    """
    Convert a Pydantic model to YAML representation.

    Args:
        m: The Pydantic model to convert
        simplify: If True, includes all fields; if False, excludes unset, default, and None values

    Returns:
        str: YAML string representation of the model
    """
    d = {
        #"exclude_unset": not simplify,
        "exclude_defaults": not simplify,
        "exclude_none": not simplify,
        'by_alias': True,
    }


    return yaml.dump(m.model_dump(**d), sort_keys=False)


class Lesson(BaseModel):
    """
    Represents an individual lesson within a module or lesson set.

    A Lesson contains educational content and configuration for a single
    learning activity.
    """
    name: str
    description: Optional[str] = None
    uid: Optional[str] = False
    path: Optional[str] = None
    lesson: Optional[str] = None
    exercise: Optional[str] = None
    exer_test: Optional[str] = None
    assessment: Optional[str] = None
    display: Optional[bool] = False
    terminal: Optional[bool] = False
    
    
    def update_metadata(self, root: Path):
        """
        Extract metadata from the lesson file.

        Returns:
            dict: A dictionary containing the extracted metadata
        """
        from syllabus.util import extract_metadata


        
        d = {}
        
        if self.lesson:
            d.update(extract_metadata(root/self.lesson))

        if self.exercise:
            d.update(extract_metadata(root/self.exercise))
           
          
        for k, v in d.items():
            if k in self.model_fields:
                setattr(self, k, v)
                
        return self

    
    @classmethod
    def new_lesson(cls, root: Path,  p: Path):
        

        if (root/p).is_dir():
            lesson = Lesson(name=clean_filename(p.name))
            for f in (root/p).iterdir():
                tless = Lesson.new_lesson(root, f.relative_to(root))
                
                lesson.display = lesson.display or tless.display
                lesson.lesson = lesson.lesson or tless.lesson
                lesson.exercise = lesson.exercise or tless.exercise
                lesson.lesson = lesson.lesson or tless.lesson
                lesson.description = lesson.description or tless.description
                
            lesson.update_metadata(root)
                
            
        else:            
            # Just a single file
            if (root/p).suffix == '.md':  
                d = {"name": clean_filename(p.stem), "lesson": str(p)}
            
            elif (root/p).suffix in ('.ipynb', '.py'):

                display = any(re.search(rx, (root/p).read_text())  for rx in display_p)

                d = {"name": clean_filename(p.stem), "exercise": str(p), "display": display}
           
            else:
                return None
           
            lesson = Lesson(**d).update_metadata(root)
            
        
        lesson.path = extract_rank_string(p)
            
        return lesson
            
    
    def __str__(self):
        return f"Lesson<{self.name}, lesson={Path(self.lesson)if self.lesson else '' }, exercise={Path(self.exercise) if self.exercise else ''}>"
    
    def sort(self):
        pass
    
class LessonSet(BaseModel):
    """
    Represents a group of related lessons.

    A LessonSet is a collection of lessons that belong together as a 
    cohesive unit within a module.
    """
    name: str
    path: str
    description: Optional[str] = None
    uid: Optional[str] = False
    lessons: List[Lesson] = []
    
    
    def sort(self):
        """Sort the lessons and lesson sets within the module."""
        self.lessons.sort(key=lambda x: str(x.path))
        for l in self.lessons:
            l.sort()
    
    


class Module(BaseModel):
    """
    Represents a module within a course.

    A Module is a major educational unit containing multiple lessons or lesson sets,
    forming a key component of the overall course structure.
    """
    name: str
    path: str
    description: Optional[str] = None
    
    overview: Optional[str] = None
    uid: Optional[str] = False
    lessons: List[Lesson | LessonSet] = []


            
    def to_yaml(self, simplify=False):
        """
        Convert the Module to YAML format.

        Args:
            simplify: If True, includes all fields; if False, excludes unset, default, and None values

        Returns:
            str: YAML string representation of the Module
        """
        return to_yaml(self, simplify)
    
    
    def sort(self):
        """Sort the lessons and lesson sets within the module."""
        self.lessons.sort(key=lambda x: str(x.path))
        for l in self.lessons:
            l.sort()
    

class Course(BaseModel):
    """
    Represents a complete course with modules, objectives, and configuration.

    A Course is the top-level container for educational content, containing
    a series of modules and course-level metadata.
    """
    name: str
    description:  Optional[str] = None
    objectives: Optional[List["Objective"]] = None
    module_dir: Optional[str] = None # Path from the syllabus dir to the prefix dir for the lesson paths
    uid: Optional[str] = False
   
    modules: List[Module] = []



    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
        json_encoders = {
            BaseModel: lambda v: v.dict(by_alias=True)
        }


    @classmethod
    def from_yaml(cls, path):
        """
        Create a Course instance from a YAML file.

        Args:
            path: Path to the YAML file

        Returns:
            Course: A new Course instance
        """
        with open(path, encoding='utf-8') as f:
            data = yaml.safe_load(f)

        return cls(**data)

    def to_yaml(self, path=None, simplify=False):
        """
        Convert the Course to YAML format.

        Args:
            path: If provided, writes YAML to this file path
            simplify: If True, includes all fields; if False, excludes unset, default, and None values

        Returns:
            str or None: YAML string if path is None, otherwise None (writes to file)
        """

        if path:
            with open(path, 'w', encoding="utf-8") as f:
                f.write(to_yaml(self, simplify))
        else:
            return to_yaml(self, simplify)

    def to_json(self):
        """
        Convert the Course to JSON format.

        Returns:
            str: JSON string representation of the Course
        """
        
        return json.dumps(self.model_dump(), indent=4)

    def __str__(self):
        return f"Course<{self.name}>"

    def sort(self):
        """Recursively sort by the path strings """

        self.modules.sort(key=lambda x: str(x.path))

        for m in self.modules:
            m.sort()
            

    def path_map():
        ...



class Objective(BaseModel):
    """
    Represents a learning objective for a course.

    Objectives define the educational goals and expected outcomes
    that students should achieve through the course.
    """
    name: str
    description: str
