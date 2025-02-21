from beanie import Document
from pydantic import BaseModel
from typing import List, Optional


# Sub-models
class Requirement(BaseModel):
    name: str
    value: bool

class Form(BaseModel):
    name: str
    link: str

class Funding(BaseModel):
    evergreen: bool
    current_funding_level: str

#main doc
class Program(Document):
    # id: Optional[PydanticObjectId] = None
    program_id: Optional[int]
    program_name: Optional[str]
    coverage_eligibilities: Optional[List[str]]
    program_type: Optional[str]
    requirements: Optional[List[Requirement]]
    benefits: List[dict]
    forms: Optional[List[Form]]
    funding: Optional[dict]
    details: Optional[List[dict]]
    class Settings:
        name = "programs"
