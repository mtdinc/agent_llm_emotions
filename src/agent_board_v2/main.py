#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from agent_board_v2.crew import AgentBoardV2

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Sample medical case for testing the differential diagnosis system
SAMPLE_MEDICAL_CASE = """CC: 53-year-old male was transferred due to cough, dyspnea, and fevers for 2 weeks.

HPI: Has minimal health care exposure. Presented to urgent care and was found to be hypoxic, leading to transfer to the hospital. Productive cough with brown sputum, intermittent fevers.

ROS: Poor oral intake, unintentional weight loss over the last 2 months.

PMH: Tobacco use disorder, otherwise none.

Meds: None. Fam Hx: Brother passed away from lung cancer, mother has COPD and colon cancer.

Soc Hx: Wood stove in house, worked in landscaping, no travel. Lives in North Carolina.

Health-Related Behaviors: Smoking (20 pack-year), sexually active with one partner.

Allergies: Codeine.

Vitals: T: 99.3°F (37.2°C) BP: 116/71 HR: 121 Sat: 99% on 4L of O2 by nasal cannula. Exam: Gen: 14.8 BMI, ill-appearing and cachectic. HEENT: Unremarkable. CV: Tachycardia, otherwise unremarkable. Pulm: Limited air movement, diffuse rhonchi. Abd: Soft, non-tender, bowel sounds normal. Neuro: No focal deficits, AO x 3. MSK: No edema, strong peripheral pulses.

Notable Labs & Imaging:
Hematology:
WBC: 22.8 Hgb: 12.5 Plt: 494 MCV: 94.6

Chemistry:
Na: 135 K: 3.8 Cr: 0.47 BUN: 13 Ca: 8.4 Ph: 2.2 Mg: 1.5 Glu: 67 Cl: 102 HCO3: 25 Anion gap normal. Lactic acid 1.4 AST: 56 ALT: 33 ALP: 158 (slightly high) Bili: 0.4 Total protein: 5.6 Albumin: 2.5 HIV & COVID negative.

Imaging:
EKG: Sinus tachycardia with HR of 132 bpm. CXR: Hyperinflation, bilateral dense areas of consolidations and cavitary lesions. CT: No PE, dense LUL consolidation + cavity, large RUL cavity with gas/fluid level, bilateral areas of nodular consolidation, bilateral hilar LAD.

S. pneumo, Histo, Cocci, Crypto, Legionella, Aspergillus negative. Quantiferon negative.

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
