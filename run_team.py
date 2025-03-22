#!/usr/bin/env python
r"""
Script to run different team configurations with different medical cases.

IMPORTANT: Before running this script, make sure to activate the virtual environment:
    source venv/bin/activate (macOS/Linux)
    venv\Scripts\activate (Windows)
"""

import sys
import os
import argparse
from pathlib import Path
import subprocess
import shutil
import re

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

def update_env_model(provider, model_name):
    """
    Update the .env file with the specified model provider and name.
    
    Args:
        provider (str): The model provider (openai or anthropic)
        model_name (str): The model name
    """
    # Validate provider
    if provider.lower() not in ['openai', 'anthropic']:
        print(f"Error: Invalid provider '{provider}'. Must be 'openai' or 'anthropic'.")
        sys.exit(1)
    
    # Path to the .env file
    env_file = Path(".env")
    
    # Check if .env file exists
    if not env_file.exists():
        print("Error: .env file not found.")
        sys.exit(1)
    
    # Read the current content
    with open(env_file, 'r') as file:
        lines = file.readlines()
    
    # Update the MODEL line
    updated_lines = []
    model_updated = False
    
    for line in lines:
        if line.startswith('MODEL='):
            updated_lines.append(f"MODEL={provider.lower()}/{model_name}\n")
            model_updated = True
        else:
            updated_lines.append(line)
    
    # If MODEL line wasn't found, add it
    if not model_updated:
        updated_lines.append(f"MODEL={provider.lower()}/{model_name}\n")
    
    # Write the updated content
    with open(env_file, 'w') as file:
        file.writelines(updated_lines)
    
    print(f"✅ Updated .env to use {provider}/{model_name}")

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

def ensure_output_dir():
    """
    Ensure the output directory exists.
    
    Returns:
        Path: The path to the output directory
    """
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    return output_dir

def run_team(team_number, case_id, stage=1, provider=None, model_name=None):
    """
    Run a specific team configuration with a specific case.
    
    Args:
        team_number (int): The team configuration to use (1, 2, 3, or 4)
        case_id (str): The ID of the case to run
        stage (int): The stage of the case (1 or 2)
        provider (str, optional): The model provider (openai or anthropic)
        model_name (str, optional): The model name
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
    
    # Ensure output directory exists
    output_dir = ensure_output_dir()
    
    # Set the output file name
    if provider and model_name:
        output_file = output_dir / f"result_team{team_number}_case{case_id}_stage{stage}_{provider}_{model_name}.md"
    else:
        output_file = output_dir / f"result_team{team_number}_case{case_id}_stage{stage}.md"
    
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
    parser = argparse.ArgumentParser(description='Run different team configurations with different medical cases.')
    
    # Required arguments
    parser.add_argument('team_number', type=int, choices=[1, 2, 3, 4],
                        help='Team configuration to use (1: Collaborative, 2: Mixed, 3: Difficult, 4: Baseline)')
    
    # Optional arguments
    parser.add_argument('case_id', nargs='?', default=None,
                        help='Case ID to run (e.g., 1572). If omitted, all cases in the stage will be run.')
    parser.add_argument('stage', nargs='?', type=int, choices=[1, 2], default=1,
                        help='Stage of the case (1 or 2). Default: 1')
    
    # Model configuration arguments
    parser.add_argument('-p', '--provider', choices=['openai', 'anthropic'], metavar='PROVIDER',
                        help='Model provider (openai or anthropic)')
    parser.add_argument('-m', '--model', dest='model_name',
                        help='Model name (e.g., gpt-4o or claude-3-7-sonnet-20250219 claude-3-5-haiku-20241022 )')
    
    args = parser.parse_args()
    
    # Update model configuration if provided
    if args.provider and args.model_name:
        update_env_model(args.provider, args.model_name)
    elif args.provider or args.model_name:
        print("Error: Both --provider and --model must be specified together.")
        sys.exit(1)
    
    # If case_id is provided, run just that case
    if args.case_id:
        run_team(args.team_number, args.case_id, args.stage, args.provider, args.model_name)
    else:
        # Run all cases in the specified stage
        case_ids = get_all_case_ids(args.stage)
        if not case_ids:
            print(f"No cases found for stage {args.stage}")
            return
        
        print(f"Running Team {args.team_number} on all cases in Stage {args.stage}")
        print(f"Found {len(case_ids)} cases: {', '.join(case_ids)}")
        
        for i, case_id in enumerate(case_ids):
            print(f"\n[{i+1}/{len(case_ids)}] Processing case {case_id}...")
            run_team(args.team_number, case_id, args.stage, args.provider, args.model_name)
            print(f"Completed case {case_id}")

# Call the main function when the script is run directly
if __name__ == "__main__":
    main()
