# imports
import sys
import os
import warnings
import json
from dotenv  import load_dotenv
from local_dataflow_crewai.crew import LocalFlowCrewai

#warning
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# load env
load_dotenv()

# functions related to the crew
def run():
    """
    Run the crew.
    """
    inputs = {
        "input_file" :   os.getenv("DEPLOY")                              # inputs 
    }

    try:
        LocalFlowCrewai().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

#  python -m local_dataflow_crewai.main
                      
# def replay():
#     """
#     Replay the crew execution from a specific task.
#     """
#     try:
#         LocalFlowCrewai().crew().replay(task_id=sys.argv[1])

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")



# def run_with_trigger():
#     """
#     Run the crew with trigger payload.
#     """

#     if len(sys.argv) < 2:
#         raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

#     try:
#         trigger_payload = json.loads(sys.argv[1])                                # trigger to define
#     except json.JSONDecodeError:
#         raise Exception("Invalid JSON payload provided as argument")
    

#     inputs = {
#         "crewai_trigger_payload": trigger_payload
#     }

#     try:
#         result = LocalFlowCrewai().crew().kickoff(inputs=inputs)
#         return result
#     except Exception as e:
#         raise Exception(f"An error occurred while running the crew with trigger: {e}")

# running
run()   