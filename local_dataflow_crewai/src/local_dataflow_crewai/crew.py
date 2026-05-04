# imports
import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai import LLM
from local_dataflow_crewai.tools.custom_tool import ReadjsonTool, DeploymentFirstAreaTool, DeploymentSecondAreaTool
from typing import List

# load env
load_dotenv()

# The Crew
@CrewBase

class LocalFlowCrewai():
    """LocalCheckingCrewai crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    #========llm==========
    
    def build_llm(self) :   

        return LLM(                                      #crewai
                model="ollama/llama3.1",
                base_url="http://localhost:11434",
                api_key="ollama",
                timeout= 300,
                temperature=0
            )
   
    #=======agents=========
    @agent
    def Readjson_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['Readjson_agent'], # type: ignore[index]
            verbose=True,
            llm = self.build_llm(),
            tools = [ReadjsonTool()],
            max_iter = 2
        )

    @agent
    def DeploymentFirstArea_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['DeploymentFirstArea_agent'], # type: ignore[index]
            verbose=True,
            llm = self.build_llm(),
            tools = [DeploymentFirstAreaTool()],
            max_iter = 2
        )
    
    @agent
    def DeploymentSecondArea_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['DeploymentSecondArea_agent'], # type: ignore[index]
            verbose=True,
            llm = self.build_llm(),
            tools = [DeploymentSecondAreaTool()],
            max_iter = 2
        )

    #=======tasks=========
  
    @task
    def Readjson_task(self) -> Task:
        return Task(
            config=self.tasks_config['Readjson_task'], # type: ignore[index]
        )

    @task
    def DeploymentFirstArea_task(self) -> Task:
        return Task(
            config=self.tasks_config['DeploymentFirstArea_task'], # type: ignore[index]     
        )
    
    @task
    def  DeploymentSecondArea_task(self) -> Task:
        return Task(
            config=self.tasks_config['DeploymentSecondArea_task'], # type: ignore[index]
        )

    #==========crew=========
    @crew
    def crew(self) -> Crew:
        """Creates the LocalCheckingCrewai crew"""
        
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True
            )
