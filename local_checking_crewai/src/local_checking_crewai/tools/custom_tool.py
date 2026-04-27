from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import json
import os
import shutil

#=========Base model==========
class ReadjsonToolInput(BaseModel):
   
    input_file: str = Field(..., description="path to the json file to read")

class CheckingInput(BaseModel):
    repository: str = Field(..., description="path to the repository")
    filename: str = Field(..., description="path to the file")

class ForwardToolInput(BaseModel):
    exists: str = Field(..., description="Does the file already exist?")
    database: str = Field(..., description="Path to the database folder")
    repository: str = Field(..., description="Path to the repository folder")
    filename: str = Field(..., description="Name of the file to forward")

#==========Base Tool============
class ReadjsonTool(BaseTool):
    name : str = "read_json"
    description : str = "This tool will help agents to receive instructions from a json file"
    args_schema : Type[BaseModel] = ReadjsonToolInput 
    
    class Config:
        arbitrary_types_allowed = True


    def _run(self, input_file: str):
        with open(input_file, "r", encoding="utf-8") as f:
            return json.load(f)

class CheckingRepoTool(BaseTool):
    name: str = "checking"
    description: str = "Check if a file exists in a repository"
    args_schema: Type[BaseModel] = CheckingInput

    def _run(self, repository: str, filename: str):
        full_path = os.path.join(repository, filename)
        exists = os.path.isfile(full_path)

        if exists:
            return "exists=true"
        else:
            return "exists=false"

        
class ForwadingRepoTool(BaseTool):

    name: str = "forward"
    description : str  = """
    This tool will help agents to forward a filename from a database to a given repository
    if the filenma doesn't exist inside the repository.

    """ 
    args_schema : Type[BaseModel] = ForwardToolInput

    class Config:
        arbitrary_types_allowed = True


    def _run(self, exists: str, database:str, repository:str, filename:str):

        if exists == "exists=false" :
            shutil.copy(os.path.join(database, filename),                               # forwading
            os.path.join(repository, filename))
            return " Forwading completed ! "
        
        if exists == "exists=true" :
            return "The repository contains the filename"