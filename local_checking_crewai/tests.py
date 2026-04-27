print("étape 1 — imports")
from local_checking_crewai.crew import LocalCheckingCrewai

print("étape 2 — instanciation")
c = LocalCheckingCrewai()

print("étape 3 — crew")
crew = c.crew()

print("étape 4 — kickoff")
result = crew.kickoff(inputs={"input_file": "input.json"})

print("RÉSULTAT :", result)