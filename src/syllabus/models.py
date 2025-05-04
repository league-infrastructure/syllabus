
from typing import List, Optional

import yaml
from pydantic import BaseModel
import json

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
        "exclude_unset": not simplify,
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
    workdir: Optional[str] = None
    sourcedir: Optional[str] = None
    lesson: Optional[str] = None
    exercise: Optional[str] = None
    exer_test: Optional[str] = None
    assessment: Optional[str] = None
    display: Optional[bool] = False
    
class LessonSet(BaseModel):
    """
    Represents a group of related lessons.

    A LessonSet is a collection of lessons that belong together as a 
    cohesive unit within a module.
    """
    name: str
    description: Optional[str] = None
    lessons: List[Lesson]
    
    


class Module(BaseModel):
    """
    Represents a module within a course.

    A Module is a major educational unit containing multiple lessons or lesson sets,
    forming a key component of the overall course structure.
    """
    name: str
    description: Optional[str] = None
    overview: Optional[str] = None
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
    



class Course(BaseModel):
    """
    Represents a complete course with modules, objectives, and configuration.

    A Course is the top-level container for educational content, containing
    a series of modules and course-level metadata.
    """
    name: str
    description: str
    objectives: Optional[List["Objective"]] = None
    workdir: Optional[str] = None
    sourcedir: Optional[str] = None
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





class Objective(BaseModel):
    """
    Represents a learning objective for a course.

    Objectives define the educational goals and expected outcomes
    that students should achieve through the course.
    """
    name: str
    description: str
