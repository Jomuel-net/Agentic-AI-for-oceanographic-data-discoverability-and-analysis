# Purpose (verify if a certain file is inside a repository by following instructions provided by a json file)
import json
import os
import shutil                                           # forward files
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# input

def load_instructions(json_name):

    """
    Read and load a json file using its name

    """
    with open(json_name, "r", encoding="utf-8") as f:
        return json.load(f)

def file_exists_in_repo(repository, filename):

    f"""
    Returns True if {filename} exists inside {repository}

    """
    full_path = os.path.join(repository, filename)

    return os.path.isfile(full_path)

def forward_from_database(database, repository, filename):
    
    f"""
    Forwards a given {filename} from {database} to the {repository} 
    
    """
    shutil.copy(os.path.join(database, filename),                               # forwading
    os.path.join(repository, filename))

    return " Forwading completed ! "

# read the json instructions
instructions = load_instructions("input.json")

# checking
repository = instructions["repository"]
database = instructions["database"]
filename = instructions["filename"]
exists = file_exists_in_repo(repository, filename)

# # json test
# print(exists)

# orcherstrates the forwading if the file is not in the file system
if exists is False :
    forward_from_database (database=database, repository=repository, filename=filename)

# Agent analysis
load_dotenv()  
# connection to open ai
api_key=os.getenv("OPENAI_API_KEY")                              

# llm
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    api_key=api_key
)

# prompt
template = PromptTemplate(
    input_variables=["filename","database", "repository", "exists"],
    template=
    """
We want to check the filesystem, such that we verify if a certain file is in a certain repository. Otherwise, we forward it from the database

Database: {database}
Repository: {repository}
Filename: {filename}
Exists: {exists}

Please, provide a clear feedback and what happends to the user.

"""
)
# chain

chain = template | llm | StrOutputParser()

result = chain.invoke({
    "database": database,
    "repository": repository,
    "filename": filename,
    "exists": exists
})

# result
print(result)