from typing import List, Union, Annotated
from pydantic import BaseModel, Field
from typing import List, Optional
import yaml

def to_yaml(m, simplify=False):
    d = {
            "exclude_unset": not simplify,
            "exclude_defaults":  not simplify,
            "exclude_none": not simplify,
            'by_alias': True,
    }

    return yaml.dump(m.model_dump(**d), sort_keys=False) 

class Course(BaseModel):
    name: str
    description: str
    objectives: Optional[List["Objective"]] = None
    workdir: Optional[str] = None
    sourcedir: Optional[str] = None
    modules: List["Module"]
    
    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
        json_encoders = {
            BaseModel: lambda v: v.dict(by_alias=True)
        }

    @classmethod
    def from_yaml(cls, path):
        with open(path) as f:
            data = yaml.safe_load(f)
        
        return cls(**data)
    
    def to_yaml(self, path = None, simplify=False):
        
        if path:
            with open(path, 'w') as f:
                f.write(to_yaml(self, simplify))
        else:
            return to_yaml(self, simplify)
        
        

    def to_json(self):
        import json 
        return json.dumps(self.model_dump(), indent=4)


    def __str__(self):
        return f"Course<{self.name}>"
   
   

class Lesson(BaseModel):
    name: str
    description: Optional[str] = None
    workdir: Optional[str] = None
    sourcedir: Optional[str] = None
    lesson: Optional[str] = None
    exercise: Optional[str] = None
    exer_test: Optional[str] = None
    assessment: Optional[str] = None
    

class LessonSet(BaseModel):
    name: str
    description: Optional[str] = None
    lessons: List["Lesson"]

        
class Module(BaseModel):
    name: str
    description: Optional[str] = None
    overview: Optional[str] = None
    lessons: List[Lesson|LessonSet] = []


    def to_yaml(self, simplify=False):
        return to_yaml(self, simplify)
    
class Objective(BaseModel):
    name: str
    description: str

