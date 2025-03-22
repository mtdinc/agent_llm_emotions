#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from agent_board_v2.crew import AgentBoardV2

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Sample medical case for testing the differential diagnosis system
SAMPLE_MEDICAL_CASE = """
Chief Concern: 
73 yo Male presents with 4 weeks of bilateral lower leg swelling & fatigue

HPI:
Feeling generally unwell, worse in last 4 weeks. No orthopnea, PND, chest pain. Intermittent nausea and vomiting not triggered byfood - no abdominal pain, no melena or hematochezia.

РМН:
Aortic Stenosis (TAVR in 2023)
DM2
HPT
HFpEF

Meds:
Metformin
Amlodipine
Atorvastatin
SGLT2-inhibitor Soc Hx:
Lives in Central Valley
California. No travel
overseas in 30 years.
Electrician
Adopted alternative
lifestyle, travelling in
truck. Bathing at rest
stops. No dietary
changes. Eating less
healthy food.
Health-Related
Behaviors: No
substances

Allergies: 
None

Vitals: T: 97 F BP: 167/100 mmHg RR: 16 HR: 80 bpm Sat:
Exam: Comfortable. N pupils and dentition. Bipedal pitting edema.
CV: Reg, No murmurs, No JVD
Pulm: Clear
Abd:
Neuro: Normal
Derm: Petechiae on shins

Notable Labs & Imaging:

Hematology:
WBC: 2.8, neutrophil count: 2.4 (normal); lymphopenia, Hb: 7.5 (12 baseline)
Plt: 16K; MCV: 91

Chemistry:
BUN 62, Creatinine 4.17 (baseline 1), AST 33, ALP 160, ALT 20, Albumin 3, Total Bilirubin 1.1, NT ProBNP 16000

UA: 3+ protein, 3+ RBC, UPCR 1.52. PT, PTT, smear, hemolysis labs all normal. Normal B12, Iron, copper.

Imaging:
TTE: EF 55%, LV hypertrophy, diastolic dysfunction. Normal aortic valve. Normal right atrium and ventricle.

Immune Studies:
C-ANCA, P-ANCA both positive (MPO and PR3 positive). Anti-GBM negative. C3 50, C4 9 (both low). ANA 1:80; dsDNA negative, Anti-Histone positive. Anti-SSA, SSB negative. Cryoglobulins negative.

Microbiology:
Blood cultures x 3 negative. Hep B immune, Hep C negative, HIV negative. TPPA and RPR positive: 1:64. Coxiella negative.

Renal Biopsy:
Pauci-Immune Crescentic GN (Moderate immune complex deposition in mesangium and subendothelium).

BMAT:
Erythroid hyperplasia. No dysplasia, no vacuoles, no infiltrative process.

Patient started on Rituximab - 1 week later, worsening creatinine needing dialysis. 


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
