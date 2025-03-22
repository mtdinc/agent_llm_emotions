#!/usr/bin/env python
r"""
Script to run different team configurations with different medical cases.

IMPORTANT: Before running this script, make sure to activate the virtual environment:
    source venv/bin/activate (macOS/Linux)
    venv\Scripts\activate (Windows)
"""

import sys
import os
from pathlib import Path
import subprocess
import shutil

def check_venv():
    """Check if the virtual environment is activated."""
    # Check if the virtual environment is activated by looking for the VIRTUAL_ENV environment variable
    if 'VIRTUAL_ENV' not in os.environ:
        print("WARNING: Virtual environment may not be activated!")
        print("It's recommended to activate the virtual environment before running this script:")
        print("  On macOS/Linux: source venv/bin/activate")
        print("  On Windows: venv\\Scripts\\activate")
        # Ask for confirmation to continue
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    else:
        print("✅ Virtual environment is activated.")

def update_config(team_number):
    """
    Update the crew.py file to use the specified team configuration.
    
    Args:
        team_number (int): The team configuration to use (1, 2, 3, or 4)
    """
    # Path to the crew.py file
    crew_file = Path("src/agent_board_v2/crew.py")
    
    # Read the current content
    with open(crew_file, 'r') as file:
        content = file.read()
    
    # Replace the agents_config line
    import re
    pattern = r"agents_config\s*=\s*'config/agents.*?\.yaml'"
    replacement = f"agents_config = 'config/agents_team{team_number}.yaml'"
    
    new_content = re.sub(pattern, replacement, content)
    
    # Write the updated content
    with open(crew_file, 'w') as file:
        file.write(new_content)
    
    print(f"✅ Updated crew.py to use Team {team_number} configuration.")

def load_case(case_id, stage=1):
    """
    Load a medical case from the file system.
    
    Args:
        case_id (str): The ID of the case to load
        stage (int): The stage of the case (1 or 2)
        
    Returns:
        str: The medical case text
    """
    file_path = Path(f"cases/stage_{stage}/{case_id}_s{stage}.md")
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: Case {case_id} stage {stage} not found at {file_path}")
        sys.exit(1)

def get_true_diagnosis(case_id):
    """
    Get the true diagnosis for a case from case_list.csv.
    
    Args:
        case_id (str): The ID of the case
        
    Returns:
        str: The true diagnosis
    """
    file_path = Path("cases/case_list.csv")
    with open(file_path, 'r') as file:
        for line in file:
            id, diagnosis = line.strip().split(',', 1)
            if id == case_id:
                return diagnosis
    return "Unknown"

def update_main_py(case_id, stage):
    """
    Update main.py to use the specified case.
    
    Args:
        case_id (str): The ID of the case to run
        stage (int): The stage of the case (1 or 2)
    """
    # Load the case
    case_text = load_case(case_id, stage)
    
    # Path to the main.py file
    main_file = Path("src/agent_board_v2/main.py")
    
    # Read the current content
    with open(main_file, 'r') as file:
        content = file.read()
    
    # Find the SAMPLE_MEDICAL_CASE variable
    import re
    pattern = r"SAMPLE_MEDICAL_CASE\s*=\s*\"\"\".*?\"\"\""
    replacement = f'SAMPLE_MEDICAL_CASE = """{case_text}"""'
    
    # Replace the content using re.DOTALL to match across multiple lines
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Write the updated content
    with open(main_file, 'w') as file:
        file.write(new_content)
    
    print(f"✅ Updated main.py to use Case {case_id} Stage {stage}.")

def run_team(team_number, case_id, stage=1):
    """
    Run a specific team configuration with a specific case.
    
    Args:
        team_number (int): The team configuration to use (1, 2, 3, or 4)
        case_id (str): The ID of the case to run
        stage (int): The stage of the case (1 or 2)
    """
    # Validate inputs
    if team_number not in [1, 2, 3, 4]:
        print(f"Error: Invalid team number {team_number}. Must be 1, 2, 3, or 4.")
        return
    
    # Check if virtual environment is activated
    check_venv()
    
    # Get the true diagnosis
    true_diagnosis = get_true_diagnosis(case_id)
    print(f"Running Team {team_number} on Case {case_id} (Stage {stage})")
    print(f"True diagnosis: {true_diagnosis}")
    
    # Update the configuration files
    update_config(team_number)
    update_main_py(case_id, stage)
    
    # Set the output file name
    output_file = f"medical_case_analysis_team{team_number}_case{case_id}_stage{stage}.md"
    
    # Make a backup of the original medical_case_analysis.md if it exists
    if os.path.exists("medical_case_analysis.md"):
        shutil.copy("medical_case_analysis.md", "medical_case_analysis_backup.md")
        print("✅ Backed up existing medical_case_analysis.md")
    
    # Run the crew
    try:
        print("Running CrewAI... (this may take a while)")
        subprocess.run(["crewai", "run"], check=True)
        
        # Rename the output file
        if os.path.exists("medical_case_analysis.md"):
            shutil.copy("medical_case_analysis.md", output_file)
            print(f"✅ Analysis completed. Output saved to {output_file}")
        else:
            print("⚠️ Warning: medical_case_analysis.md was not created.")
    except subprocess.CalledProcessError as e:
        print(f"Error running the crew: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def get_all_case_ids(stage):
    """
    Get all case IDs available in the specified stage directory.
    
    Args:
        stage (int): The stage (1 or 2)
        
    Returns:
        list: A sorted list of case IDs
    """
    stage_dir = Path(f"cases/stage_{stage}")
    case_files = list(stage_dir.glob(f"*_s{stage}.md"))
    # Extract case IDs from filenames (e.g., "1572_s1.md" -> "1572")
    case_ids = [file.stem.split('_')[0] for file in case_files]
    return sorted(case_ids)  # Sort to process in order

def main():
    """Main function to parse command line arguments and run the team."""
    if len(sys.argv) < 2:
        print("Usage: python run_team.py TEAM_NUMBER [CASE_ID] [STAGE]")
        print("  TEAM_NUMBER: 1, 2, 3, or 4")
        print("    1: Collaborative team")
        print("    2: Mixed team (one difficult member)")
        print("    3: Difficult team (two difficult members)")
        print("    4: Baseline team (no personality traits)")
        print("  CASE_ID: e.g., 1572 (if omitted, all cases in the stage will be run)")
        print("  STAGE: 1 or 2 (default: 1)")
        return
    
    team_number = int(sys.argv[1])
    
    # Default stage is 1
    stage = 1
    case_id = None
    
    # Parse remaining arguments
    if len(sys.argv) > 2:
        # Check if the second argument is a stage number (1 or 2)
        if sys.argv[2].isdigit() and int(sys.argv[2]) in [1, 2]:
            # It's a stage number
            stage = int(sys.argv[2])
        else:
            # It's a case ID
            case_id = sys.argv[2]
            # Check if there's a stage specified
            if len(sys.argv) > 3:
                stage = int(sys.argv[3])
    
    # If case_id is provided, run just that case
    if case_id:
        run_team(team_number, case_id, stage)
    else:
        # Run all cases in the specified stage
        case_ids = get_all_case_ids(stage)
        if not case_ids:
            print(f"No cases found for stage {stage}")
            return
        
        print(f"Running Team {team_number} on all cases in Stage {stage}")
        print(f"Found {len(case_ids)} cases: {', '.join(case_ids)}")
        
        for i, case_id in enumerate(case_ids):
            print(f"\n[{i+1}/{len(case_ids)}] Processing case {case_id}...")
            run_team(team_number, case_id, stage)
            print(f"Completed case {case_id}")

