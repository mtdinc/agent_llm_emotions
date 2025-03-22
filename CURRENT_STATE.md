# Current State of Agent Board v2: Medical Differential Diagnosis System

## Project Setup (Completed)

- Created a virtual environment using Python 3.12 (compatible with CrewAI requirements)
- Created README.md with setup instructions and project information

## Important: Virtual Environment

**IMPORTANT**: This project uses a Python virtual environment that must be activated before running any scripts or commands.

1. **Activate the virtual environment**:
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```

2. **Verify activation**:
   
   You should see `(venv)` at the beginning of your command prompt when the environment is activated.

## Project Structure (Completed)

The project structure has been successfully created using the CrewAI CLI command `crewai create crew agent_board_v2`. This has generated the foundation for implementing the medical differential diagnosis system with two general medicine internists.

## Implementation Status

- **Environment Setup**: ✅ Completed
- **Project Scaffolding**: ✅ Completed
- **Medical Internist Agent Configuration**: ✅ Completed
- **Medical Case Discussion Task Configuration**: ✅ Completed
- **Hierarchical Collaboration Process**: ✅ Completed
- **Senior Internist Manager Role**: ✅ Completed
- **Natural Clinical Discussion Flow**: ✅ Completed
- **Team Configurations**: ✅ Completed
- **Model Selection System**: ✅ Completed
- **Output Naming System**: ✅ Completed
- **Medical Knowledge Tools**: ⏳ Pending
- **Medical Knowledge Base**: ⏳ Pending
- **Case Input/Output System**: ⏳ Pending

## Team Configurations

We've created four different team configurations to study how team dynamics affect diagnostic accuracy:

1. **Team 1: Collaborative Team** (`agents_team1.yaml`)
   - All team members are collaborative, open to feedback, and team-oriented
   - Emphasizes respectful dialogue and consensus-building

2. **Team 2: Mixed Team** (`agents_team2.yaml`)
   - Chief Internist and Primary Diagnostician are collaborative
   - Diagnostic Reviewer is arrogant and dismissive of others' opinions

3. **Team 3: Difficult Team** (`agents_team3.yaml`)
   - Chief Internist remains collaborative
   - Both Primary Diagnostician and Diagnostic Reviewer are arrogant and non-team players
   - Team members are resistant to feedback and dismissive of others' opinions

4. **Team 4: Baseline Team** (`agents_team4.yaml`)
   - Neutral team with no personality traits or emotional characteristics
   - Focuses purely on medical expertise and clinical reasoning
   - Serves as a control group for comparison

## Running Different Team Configurations

The project now includes a `run_team.py` script that makes it easy to run different team configurations with different medical cases:

1. **Activate the virtual environment** (as described above)
2. **Run the script** with the desired team configuration, case, and model:
   
   ```bash
   # Make sure you're in the agent_board_v2 directory
   cd agent_board_v2
   
   # Run the script
   python run_team.py TEAM_NUMBER [CASE_ID] [STAGE] [OPTIONS]
   ```

Parameters:
- `TEAM_NUMBER`: 1, 2, 3, or 4 (corresponding to the team configurations above)
- `CASE_ID`: The ID of the case to run (e.g., 1572)
- `STAGE`: 1 or 2 (default: 1)
  - Stage 1: Initial patient presentation without lab results
  - Stage 2: Same presentation plus lab results and imaging

Options:
- `-p, --provider`: Model provider (openai or anthropic)
- `-m, --model`: Model name (e.g., gpt-4o for OpenAI or claude-3-5-haiku-20241022 for Anthropic)

Examples:
```bash
# Run Team 1 on Case 1572, Stage 1
python run_team.py 1 1572 1

# Run Team 2 on Case 1573, Stage 2 using OpenAI's GPT-4o model
python run_team.py 2 1573 2 --provider openai --model gpt-4o

# Run Team 3 on Case 1572, Stage 1 using Anthropic's Claude model
python run_team.py 3 1572 1 --provider anthropic --model claude-3-5-haiku-20241022
```

The script will:
1. Check if the virtual environment is activated
2. Update the configuration files to use the specified team and case
3. Update the .env file with the specified model provider and name (if provided)
4. Run the crew and save the output to a file in the `output` directory:
   ```
   output/result_team{team_number}_case{case_id}_stage{stage}_{provider}_{model}.md
   ```
   For example: `output/result_team2_case1573_stage1_openai_gpt4o.md`

## Dependencies

- Python 3.12 has been installed
- Virtual environment has been created
- uv and CrewAI have been installed as per the README.md instructions

## Current Files

- README.md: Project documentation and setup instructions
- crewai_documentation.md: Reference documentation for CrewAI
- CURRENT_STATE.md: This file, documenting the current state of the project
- run_team.py: Script to run different team configurations with different models
- output/: Directory containing analysis results from different runs
- agent_board_v2/: Project directory containing:
  - .env: Environment variables with API keys and model configuration
  - src/agent_board_v2/: Source code directory with:
    - config/agents.yaml: Agent configuration file (customized for senior internist manager and two medical internists)
    - config/tasks.yaml: Task configuration file (simplified for natural clinical discussion flow with delegation guidance)
    - config/agents_team1.yaml: Configuration for collaborative team
    - config/agents_team2.yaml: Configuration for mixed team (one difficult member)
    - config/agents_team3.yaml: Configuration for difficult team (two difficult members)
    - config/agents_team4.yaml: Configuration for baseline team (no personality traits)
    - crew.py: Crew orchestration file (updated with memory and single task for natural discussion)
    - main.py: Entry point for running the crew (updated with sample medical case)
    - tools/: Directory for custom medical tools
  - knowledge/: Directory for medical knowledge base
  - cases/: Directory containing medical cases
    - stage_1/: Initial patient presentations without lab results
    - stage_2/: Same presentations plus lab results and imaging
