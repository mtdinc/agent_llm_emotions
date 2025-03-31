# run_full_experiment.py
import subprocess
import sys
import os

# --- Configuration ---
TEAMS_TO_RUN = [1, 2, 3, 4]
RUN_TEAM_SCRIPT = "run_team.py"
AGGREGATE_SCRIPT = os.path.join("src", "agent_board_v2", "output_to_csv.py")
ANALYZE_SCRIPT = "analyze_outputs_llm.py"

# --- Helper Function to Run Subprocess ---
def run_script(script_path, args=[]):
    """Runs a python script using subprocess, checking for errors."""
    command = [sys.executable, script_path] + args
    print(f"\n--- Running command: {' '.join(command)} ---")
    try:
        # Use check=True to raise CalledProcessError if the script fails (non-zero exit code)
        result = subprocess.run(command, check=True, text=True, capture_output=False) # Stream output directly
        print(f"--- Successfully completed: {' '.join(command)} ---")
        return True
    except FileNotFoundError:
        print(f"Error: Script not found at {script_path}")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error running script: {' '.join(command)}")
        print(f"Exit code: {e.returncode}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while running {' '.join(command)}: {e}")
        return False

# --- Main Execution ---
def main():
    """Runs the full experiment: all teams for Stage 2 (default), aggregation, and analysis."""

    # --- Step 1: Run all teams for Stage 2 (default) ---
    print(f">>> Starting Step 1: Running all teams for all cases in Stage 2 (default) <<<")
    print(f"Using model configuration from .env file.")
    all_teams_successful = True
    for team_num in TEAMS_TO_RUN:
        print(f"\n== Running Team {team_num} ==")
        # Pass only team number. run_team.py defaults to stage 2 and all cases.
        run_team_args = [str(team_num)]

        if not run_script(RUN_TEAM_SCRIPT, run_team_args):
            all_teams_successful = False
            print(f"!!! Team {team_num} run failed. Stopping experiment. !!!")
            break # Stop if one team fails

    if not all_teams_successful:
        print("Experiment aborted due to failure in team runs.")
        sys.exit(1)

    print("\n>>> Completed Step 1: All team runs finished successfully. <<<")

    # --- Step 2: Aggregate Results ---
    print("\n>>> Starting Step 2: Aggregating raw outputs <<<")
    # No arguments needed for the aggregation script
    if not run_script(AGGREGATE_SCRIPT):
        print("!!! Aggregation script failed. Stopping experiment. !!!")
        sys.exit(1)
    print(">>> Completed Step 2: Aggregation finished successfully. <<<")

    # --- Step 3: Analyze Results ---
    print("\n>>> Starting Step 3: Analyzing aggregated outputs <<<")
    # No arguments needed for the analysis script
    if not run_script(ANALYZE_SCRIPT):
        print("!!! Analysis script failed. !!!")
        # Decide if failure here should stop the overall process or just be noted
        # sys.exit(1)
    else:
        print(">>> Completed Step 3: Analysis finished successfully. <<<")

    print("\n=== Full Experiment Run Completed ===")

if __name__ == "__main__":
    main()