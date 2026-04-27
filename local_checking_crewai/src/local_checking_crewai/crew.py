# imports
import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.custom_tool import ReadjsonTool, CheckingRepoTool, ForwadingRepoTool 
from typing import List

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


# load env
load_dotenv()

@CrewBase
class LocalCheckingCrewai():
    """LocalCheckingCrewai crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools


    #========llm==========
    def build_llm(self):

        return ChatGoogleGenerativeAI(
            model="gemini-3.1-pro-preview",
            api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.2
        )

    #=======agents=========
    @agent
    def load_instructions_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['load_instructions_agent'], # type: ignore[index]
            verbose=True,
            llm = self.build_llm(),
            tools = [ReadjsonTool()]
        )

    @agent
    def file_exists_in_repo_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['file_exists_in_repo_agent'], # type: ignore[index]
            verbose=True,
            llm = self.build_llm(),
            tools = [CheckingRepoTool()]
        )
    
    @agent
    def forward_from_database_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['forward_from_database_agent'], # type: ignore[index]
            verbose=True,
            llm = self.build_llm(),
            tools = [ForwadingRepoTool()]
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task

    #=======tasks=========
    @task
    def load_instructions_task(self) -> Task:
        return Task(
            config=self.tasks_config['load_instructions_task'], # type: ignore[index]
        )

    @task
    def file_exists_in_repo_task(self) -> Task:
        return Task(
            config=self.tasks_config['file_exists_in_repo_task'], # type: ignore[index]
        )
    
    @task
    def forward_from_database_task(self) -> Task:
        return Task(
            config=self.tasks_config['forward_from_database_task'], # type: ignore[index]
            output_file='report.md'
        )

    #======crew=====
    @crew
    def crew(self) -> Crew:
        """Creates the LocalCheckingCrewai crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
