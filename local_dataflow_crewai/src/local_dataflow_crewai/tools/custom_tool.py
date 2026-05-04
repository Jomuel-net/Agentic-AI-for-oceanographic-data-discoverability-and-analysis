from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import json
import os                                   # system file
import shutil
import pandas as pd

#=========BaseModel==========
class ReadjsonToolInput(BaseModel):

    # tool inputs 
    input_file: str = Field(..., description="name of the json file to read for the deployment")
    
class DeploymentFirstAreaToolInput(BaseModel):

    # tool inputs 
    id : str = Field(..., description="Deployment identifier") 
    title : str = Field(..., description="Deployment title")   
    area1: str = Field(..., description="The stage 1 of the deployment")
    dataflow_step1: str = Field(..., description="The step of a flow inside area 1")
    type_input1: str = Field(..., description="The type of the input data")
    path_input1: str = Field(..., description="The path of the data to deploy")
    type_output1: str = Field(..., description="The type of the output data")
    path_output1: str = Field(..., description="The path of the data after deployment")
    tools_and_technologies1: str = Field(..., description="Technologies used to processing the deployment")

class DeploymentSecondAreaToolInput(BaseModel):

    # tool inputs  
    area2: str = Field(..., description="The stage 2 of the deployment")
    dataflow_step2: str = Field(..., description="The step of a flow inside area 2")
    type_input2: str = Field(..., description="The type of the input data")
    path_input2: str = Field(..., description="The path of the data to deploy")
    type_output2: str = Field(..., description="The type of the output data")
    path_output2: str = Field(..., description="The path of the data after deployment")
    tools_and_technologies2: str = Field(..., description="Technologies used to processing the deployment")


#==========BaseTool============

# Deployment (Expected) and checking  vs (actual)

class ReadjsonTool(BaseTool):
    name : str = "read_json"
    description : str = """ This tool will help agents to receive instructions of a given deployment from a json file by 
                        taking the deployment datas like, the deployment id, the title and the dataflow details.
                  
                        """
    args_schema : Type[BaseModel] = ReadjsonToolInput 
    
    def _run(self, input_file: str):

        try :
                
            with open(input_file, "r", encoding="utf-8") as f:

                # json file
                json_file = json.load(f)
                id : str = json_file ["id"]
                title : str  =  json_file ["title"]
                dataflow: list  =  json_file ["data_flow"]
                firstarea: dict  =  dataflow [0]
                secondarea:dict  =  dataflow [1]

                # area1
                area1 : str = firstarea ["area"]
                dataflow_step1: str = firstarea ["dataflow_step"]
                type_input1: str = firstarea ["type_input"]
                path_input1: str = firstarea ["path_input"]
                type_output1: str = firstarea ["type_output"]
                path_output1: str = firstarea ["path_output"]
                tools_and_technologies1: str =  firstarea ["tools_and_technologies"]

                # area2
                area2 : str = secondarea ["area"]
                dataflow_step2: str = secondarea ["dataflow_step"]
                type_input2: str = secondarea ["type_input"]
                path_input2: str = secondarea ["path_input"]
                type_output2: str = secondarea ["type_output"]
                path_output2: str = secondarea ["path_output"]
                tools_and_technologies2: str =  secondarea ["tools_and_technologies"]
                
            return  {       "id" : id,
                            "title": title,

                            # area1
                            "area1": area1,
                            "dataflow_step1": dataflow_step1,
                            "type_input1": type_input1,
                            "path_input1": path_input1,
                            "type_output1": type_output1,
                            "path_output1": path_output1,
                            "tools_and_technologies1": tools_and_technologies1,

                            # area1
                            "area2": area2,
                            "dataflow_step2": dataflow_step2,
                            "type_input2": type_input2,
                            "path_input2": path_input2,
                            "type_output2": type_output2,
                            "path_output2": path_output2,
                            "tools_and_technologies2": tools_and_technologies2

                                }
        
        except Exception as e :

            return (f"An error occured during the process : {e}")
        
        
class DeploymentFirstAreaTool(BaseTool):

    name: str = "deploymentfirstarea"
    description: str = """  This tool will help the agent to have all 
                            the necessar informations to proceed to the first step of the deployment
                            by using the information provided previously
                      """
    args_schema: Type[BaseModel] = DeploymentFirstAreaToolInput

                      
    def _run(self, id : str,   title : str, area1 : str,
               dataflow_step1: str,   type_input1: str,
                path_input1: str, path_output1: str,  type_output1: str,
                tools_and_technologies1: str):
        
        try :
            print(f"=========Start of the deployment id :{id}, title : {title}=========")
            print(f"=========Start of the area : {area1}, the dataflow step is : {dataflow_step1}=========")
            print(f"=========The goal is to make to obtain this type for the input data :  {type_output1}========")
            print(f"=========We will use :{tools_and_technologies1} as technology=========")

            if type_input1 == ".xlsx":
                
                exceltocsv = pd.read_excel(path_input1)                             # excel to csv
                exceltocsv.to_csv(os.path.join(path_output1,"exceltocsv.csv"))      # load in the new repo

                return {
                    "path_output1" : path_output1,
                    "type_output1" : type_output1,

                }  
            else :
                return ("Sorry ! The type of the input data is not .xls. Check your input data.")

        except Exception as e:
            return (f"An Error occured in the data deployment : {e}")


class DeploymentSecondAreaTool(BaseTool):

    name: str = "deploymentsecondarea"
    description: str = """  This tool will help the agent to have all 
                            the necessar informations to proceed to the first step of the deployment
                            by using the information provided previously
                      """
    args_schema: Type[BaseModel] = DeploymentSecondAreaToolInput

                      
    def _run(self,  area2 : str,
               dataflow_step2: str,   type_input2: str,
                path_input2: str, path_output2: str,  type_output2: str,
                tools_and_technologies2: str):
        
        try :

            print(f"=========Start of the area : {area2}, the dataflow step is : {dataflow_step2}=========")
            print(f"=========The goal is to make to obtain this type for the input data :  {type_output2}========")
            print(f"=========We will use :{tools_and_technologies2} as technology=========")

            if type_input2 == ".csv":
                
                full_path = os.path.join(path_input2, "exceltocsv.csv")
                csvtoexcel = pd.read_csv(full_path)                                                  # csv to excel
                csvtoexcel.to_excel(os.path.join(path_output2, "csvtoexcel.xlsx"), index=False)      # load in the new repo
                
                return "Second Deployment finished !"
            else :
                return ("Sorry ! May be the type of the input data is not .CSV. Check your input data. Else, it's an other error.")

        except Exception as e:

            return (f"An Error occured in the data deployment : {e}")