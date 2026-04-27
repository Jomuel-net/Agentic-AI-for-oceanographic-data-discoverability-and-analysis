from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import json
import os
import shutil

#=========Base model==========
class ReadjsonToolInput(BaseModel):

    # tool inputs 
    input_file: str = Field(..., description="path to the json file to read")

class CheckingInput(BaseModel):

    # tool inputs
    database: str = Field(..., description="Path to the database folder") 
    repository: str = Field(..., description="path to the repository folder")
    jojofile: str = Field(..., description="name of the file to consider")

class ForwardToolInput(BaseModel):

    # tool inputs 
    exists: str = Field(..., description="Does the file already exist inside the repository?")
    database: str = Field(..., description="Path to the database folder")
    repository: str = Field(..., description="Path to the repository folder")
    jojofile: str = Field(..., description="Name of the file to forward")

#==========Base Tool============
class ReadjsonTool(BaseTool):
    name : str = "read_json"
    description : str = """ This tool will help agents to receive instructions from a json file by 
                        taking the path of repository and database, and the name of the file
                  
                        """
    args_schema : Type[BaseModel] = ReadjsonToolInput 
    
    def _run(self, input_file: str):
        with open(input_file, "r", encoding="utf-8") as f:
            json_file = json.load(f)
            database : str = json_file ["database"]
            repository : str  =  json_file ["repository"]
            jojofile: str  =  json_file ["jojofile"]
            
        return  { "database" : database,
                      "repository": repository,
                        "jojofile" : jojofile
                            }

class CheckingRepoTool(BaseTool):
    name: str = "checking"
    description: str = "This tool will help the agent to verify if a file exists in a repository by using the information provided previously"
    args_schema: Type[BaseModel] = CheckingInput

    def _run(self, database : str,  repository: str, jojofile: str):
        full_path = os.path.join(repository, jojofile)
        exists = os.path.isfile(full_path)

        if exists:
            return { 
                "exists" : "exists=true",
                    "database" : database,
                      "repository": repository,
                        "jojofile" : jojofile
                            }
        else:
            return { 
                "exists" : "exists=false",
                    "database" : database,
                      "repository": repository,
                        "jojofile" : jojofile
                            }

        
class ForwadingRepoTool(BaseTool):

    name: str = "forward"
    description : str  = """
    This tool will help the agent to forward a jojofile from a database to a given repository path
    if the jojofile doesn't exist inside the repository.

    """ 
    args_schema : Type[BaseModel] = ForwardToolInput

    def _run(self, exists: str, database:str, repository:str, jojofile:str):

        if exists == "exists=false" :
            shutil.copy(os.path.join(database, jojofile),                               # forwading
            os.path.join(repository, jojofile))
            return " Forwading completed ! "
        
        if exists == "exists=true" :
            return "The repository already contains the jojofile !"