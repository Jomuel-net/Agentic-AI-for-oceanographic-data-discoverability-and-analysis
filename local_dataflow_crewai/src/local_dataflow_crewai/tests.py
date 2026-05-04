print("Etape 1 — imports")

import os
from dotenv  import load_dotenv
load_dotenv()
from local_dataflow_crewai.crew import LocalFlowCrewai

print("Etape 2 — instanciation")
c = LocalFlowCrewai()

print("Etape 3 — crew")
crew = c.crew()

print("Etape 4 — kickoff")
result = crew.kickoff(inputs={"input_file": os.getenv("INPUT")})

print("RÉSULTAT :", result)

