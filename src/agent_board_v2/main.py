#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from agent_board_v2.crew import AgentBoardV2

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Sample medical case for testing the differential diagnosis system
SAMPLE_MEDICAL_CASE = """CC: 32 y/o M with 5 days of bilateral lower extremity weakness & pain  

HPI: While getting up from his sofa, he developed acute pain in his right calf followed by acute weakness, to the point that he couldn't move it at all. An hour later, a similar event occurred on the left side. Over the next 5 days, he had to crawl to move. This has never happened before.  
History of anorexia & 10-pound weight loss last month  

ROS: (-) numbness, paresthesia, back pain  

PMH: No relevant history  

Meds: None  

Fam Hx: No relevant history  

Soc Hx: Moved from India to the Bay Area in 2015. Visited India in 2016. Uber driver  

Health-Related Behaviors: 3-4 beers/day, 1-1.5 packs of cigarettes for the last 10 years, no recreational drugs.  

Allergies: NKDA  
Vitals: T: Afebrile BP: Normal RR: Normal HR: Normal Sat: Normal  
Exam: Gen: Thin appearing  
HEENT: Normal  
Neck: Normal  
CV: Normal  
Pulm: Normal  
Abd: Normal  
Neuro: AAOx3, Cranial Nerves normal, Strength: 5/5 upper limbs, 5/5 hip flexion bilaterally, 1/5 dorsiflexion bilaterally, eversion bilaterally, big toe dorsiflexion affected. Gait - foot drop, negative Romberg, Reflexes normal.  
MSK: Normal  

"""

def run():
    """
    Run the crew.
    """
    inputs = {
        'medical_case': SAMPLE_MEDICAL_CASE,
    }
    
    try:
        AgentBoardV2().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'medical_case': SAMPLE_MEDICAL_CASE,
    }
    try:
        AgentBoardV2().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AgentBoardV2().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'medical_case': SAMPLE_MEDICAL_CASE,
    }
    try:
        AgentBoardV2().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
