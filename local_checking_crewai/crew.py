# imports
import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai import LLM
from local_checking_crewai.tools.custom_tool import ReadjsonTool, CheckingRepoTool, ForwadingRepoTool
from pydantic import BaseModel                                  # pydantic
from typing import List

# load env
load_dotenv()
#=========link with the output pydantic stylish======

class InstructionsOutput(BaseModel):
    database: str
    repository: str
    jojofile: str

class CheckingOutput(BaseModel):
    exists: str
    database: str
    repository: str
    jojofile: str

class ForwardOutput(BaseModel):
    status: str
    file_forwarded: bool
    jojofile: str

@CrewBase

class LocalCheckingCrewai():
    """LocalCheckingCrewai crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    #========llm==========
    def build_llm(self):

        return LLM(
            model=os.getenv("MODEL"),   # format LiteLLM : provider/model
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.2
             )

    #=======agents=========
    @agent
    def load_instructions_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['load_instructions_agent'], # type: ignore[index]
            verbose=True,
            llm = self.build_llm(),
            tools = [ReadjsonTool()],
            force_tool_usage=True 
        )

    @agent
    def file_exists_in_repo_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['file_exists_in_repo_agent'], # type: ignore[index]
            verbose=True,
            llm = self.build_llm(),
            tools = [CheckingRepoTool()],
            force_tool_usage=True 
        )
    
    @agent
    def forward_from_database_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['forward_from_database_agent'], # type: ignore[index]
            verbose=True,
            llm = self.build_llm(),
            tools = [ForwadingRepoTool()],
            force_tool_usage=True 
        )

    #=======tasks=========
  
    @task
    def load_instructions_task(self) -> Task:
        return Task(
            config=self.tasks_config['load_instructions_task'], # type: ignore[index]
            output_pydantic=InstructionsOutput,  # link the output to the tasks
        )

    @task
    def file_exists_in_repo_task(self) -> Task:
        return Task(
            config=self.tasks_config['file_exists_in_repo_task'], # type: ignore[index]
            output_pydantic=CheckingOutput
        )
    
    @task
    def forward_from_database_task(self) -> Task:
        return Task(
            config=self.tasks_config['forward_from_database_task'], # type: ignore[index]
            output_pydantic=ForwardOutput,         # ← ici
        )

    #======crew=====
    @crew
    def crew(self) -> Crew:
        """Creates the LocalCheckingCrewai crew"""
        
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
