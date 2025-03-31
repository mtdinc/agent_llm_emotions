# Agent Board v2: Medical Differential Diagnosis System

This project uses CrewAI to create a system where a Department Chief of Internal Medicine leads two general medicine internists in a natural clinical discussion to develop a differential diagnosis with detailed reasoning.

## Requirements

- Python >=3.10 and <3.13 (Project is set up with Python 3.12)
- uv (dependency management tool)
- OpenAI API Key (for output analysis)

## Setup

### 1. Virtual Environment

**IMPORTANT**: This project uses a Python virtual environment (venv) that must be activated before running any scripts or commands.

A virtual environment has already been created in the `venv` directory using Python 3.12. To activate it:

On macOS/Linux:
```bash
source venv/bin/activate
```

On Windows:
```bash
venv\Scripts\activate
```

You should see `(venv)` at the beginning of your command prompt when the environment is activated.

### 2. Install uv

If you haven't installed uv yet, follow these steps:

On macOS/Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On Windows:
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. Install CrewAI & Dependencies

With the virtual environment activated, install CrewAI and other project dependencies:

```bash
# Install CrewAI CLI tool
uv tool install crewai

# Install project dependencies (including CrewAI library, pandas, openai)
crewai install
uv pip install pandas openai python-dotenv
```

If you encounter a PATH warning after installing the `crewai` tool, run:
```bash
uv tool update-shell
```

Verify the tool installation:
```bash
uv tool list
```

### 4. Environment Variables

Create a `.env` file in the project root directory and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
# Optional: Specify default model for run_team.py if not using command-line args
# MODEL=openai/gpt-4o
```
The `analyze_outputs_llm.py` script specifically requires the `OPENAI_API_KEY`.

### 5. Project Structure Generation (If needed)

If you haven't generated the project scaffolding yet:
```bash
crewai create crew agent_board_v2
```
This will create the necessary project structure with configuration files for agents and tasks.

## Running the Crew

The project includes a `run_team.py` script that makes it easy to run different team configurations with different medical cases:

```bash
# Make sure the virtual environment is activated
# source venv/bin/activate (macOS/Linux) or venv\Scripts\activate (Windows)

# Run the script
python run_team.py TEAM_NUMBER [CASE_ID] [STAGE] [OPTIONS]
```

Parameters:
- `TEAM_NUMBER`: 1, 2, 3, or 4 (corresponding to the team configurations below)
- `CASE_ID`: The ID of the case to run (e.g., 1572). If omitted, runs all cases for the stage.
- `STAGE`: 1 or 2 (default: 2)
  - Stage 1: Initial patient presentation without lab results
  - Stage 2: Same presentation plus lab results and imaging

Options:
- `-p, --provider`: Model provider (openai or anthropic). Default: anthropic
- `-m, --model`: Model name (e.g., gpt-4o for OpenAI or claude-3-5-haiku-20241022 for Anthropic). Default: claude-3-5-haiku-20241022

Examples:
```bash
# Run Team 1 on Case 1572, Stage 2 (uses default Anthropic Claude 3 Haiku model)
python run_team.py 1 1572 2

# Run Team 2 on Case 1573, Stage 2 using OpenAI's GPT-4o model
python run_team.py 2 1573 2 --provider openai --model gpt-4o

# Run Team 3 on all cases in Stage 1 using Anthropic's Claude model
python run_team.py 3 --stage 1 --provider anthropic --model claude-3-5-haiku-20241022
```

The script will:
1. Check if the virtual environment is activated
2. Update the configuration files (`crew.py`, `main.py`) to use the specified team and case
3. Update the `.env` file with the specified model provider and name (if provided via options)
4. Run the crew using `crewai run` and save the output to a file in the `output` directory:
   ```
   output/result_team{team_number}_case{case_id}_stage{stage}_{provider}_{model}.md
   ```
   For example: `output/result_team2_case1573_stage1_openai_gpt4o.md`

## Output Analysis

After running one or more crew configurations, you can analyze the diagnostic accuracy using an LLM-based script.

First, aggregate the raw markdown outputs and true diagnoses into a summary CSV:
```bash
# Make sure the virtual environment is activated
python src/agent_board_v2/output_to_csv.py
```
This creates `output/output_summary.csv`.

Then, run the LLM-based analysis script:
```bash
# Make sure the virtual environment is activated and OPENAI_API_KEY is set in .env
python analyze_outputs_llm.py
```
This script reads `output/output_summary.csv`, uses the configured OpenAI model (default: GPT-4o) to perform two checks for each run:
1.  **Final Diagnosis Match:** Compares the final diagnosis in the report to the true diagnosis.
2.  **Differential Inclusion:** Checks if the true diagnosis was mentioned anywhere in the differential list.

The results are saved to `output/analysis_summary_llm.csv`, including boolean columns (`LLM_Accuracy_Match`, `LLM_Differential_Inclusion`) and a summary is printed to the console.

**Note:** This analysis script makes OpenAI API calls (two per result analyzed) and will incur costs.

## Team Configurations

The project includes four different team configurations to study how team dynamics affect diagnostic accuracy:

1.  **Team 1: Collaborative Team** (`agents_team1.yaml`)
    - All team members are collaborative, open to feedback, and team-oriented
    - Emphasizes respectful dialogue and consensus-building

2.  **Team 2: Mixed Team** (`agents_team2.yaml`)
    - Chief Internist and Primary Diagnostician are collaborative
    - Diagnostic Reviewer is arrogant and dismissive of others' opinions

3.  **Team 3: Difficult Team** (`agents_team3.yaml`)
    - Chief Internist remains collaborative
    - Both Primary Diagnostician and Diagnostic Reviewer are arrogant and non-team players
    - Team members are resistant to feedback and dismissive of others' opinions

4.  **Team 4: Baseline Team** (`agents_team4.yaml`)
    - Neutral team with no personality traits or emotional characteristics
    - Focuses purely on medical expertise and clinical reasoning
    - Serves as a control group for comparison

## Project Structure

```
agent_board_v2/
├── .clinerules
├── .env                 # Environment variables (API Keys, Model Config)
├── .gitignore
├── analyze_outputs_llm.py # Script for LLM-based output analysis
├── cases/               # Medical cases directory
│   ├── case_list.csv    # List of cases with true diagnoses
│   ├── stage_1/         # Initial presentations without lab results
│   └── stage_2/         # Same presentations plus lab results and imaging
├── crewai_documentation.md
├── project_milestone.md # Tracks project milestones and status
├── knowledge/           # Directory for potential medical knowledge base
├── logs.txt
├── medical_case_analysis_backup.md
├── medical_case_analysis.md # Default output file from `crewai run`
├── output/              # Directory for analysis results
│   ├── output_summary.csv # Aggregated raw results
│   └── analysis_summary_llm.csv # LLM-analyzed results
├── pyproject.toml       # Project metadata and dependencies
├── README.md            # This file
├── run_team.py          # Script to run different team configurations
├── src/
│   └── agent_board_v2/
│       ├── __init__.py
│       ├── config/          # Agent and task configurations
│       │   ├── agents.yaml
│       │   ├── agents_team1.yaml
│       │   ├── agents_team2.yaml
│       │   ├── agents_team3.yaml
│       │   ├── agents_team4.yaml
│       │   └── tasks.yaml
│       ├── crew.py          # Defines the CrewAI agents, tasks, and process
│       ├── main.py          # Entry point for running the crew via `crewai run`
│       ├── output_to_csv.py # Script to aggregate raw outputs
│       └── tools/           # Directory for custom CrewAI tools
│           ├── __init__.py
│           ├── custom_tool.py
│           └── role_names.py
├── tests/
└── venv/                # Python virtual environment (created by user)
```

## Implementation Details

### Agent Roles

The system includes three medical professionals:

1.  **Department Chief of Internal Medicine (Senior Internist)**:
    - Acts as the team leader and manager in the hierarchical process
    - Coordinates the diagnostic discussion
    - Delegates tasks to the other internists
    - Synthesizes the team's findings into a final diagnosis

2.  **Primary Diagnostician (Internist One)**:
    - Develops the initial differential diagnosis
    - Provides detailed clinical reasoning for each potential diagnosis
    - Prioritizes diagnoses based on likelihood and clinical significance

3.  **Diagnostic Reviewer (Internist Two)**:
    - Critically reviews the initial differential diagnosis
    - Identifies potential missed diagnoses or misinterpretations
    - Suggests additional diagnostic tests or information
    - Provides alternative assessments of likelihood and priority

### Workflow

The system uses a hierarchical process to simulate a natural clinical discussion:

1.  The Department Chief presents the medical case to the team
2.  The Chief asks the Primary Diagnostician to develop an initial differential diagnosis
3.  The Chief then asks the Diagnostic Reviewer to critique the initial assessment
4.  The Chief facilitates a discussion between both internists to resolve disagreements
5.  The team collaboratively develops a final consensus diagnosis
6.  The Chief finalizes a comprehensive report with management recommendations

### Technical Implementation

- Uses CrewAI's hierarchical process with the Department Chief as manager
- Enables memory for all agents to maintain conversation context
- Implements a single comprehensive task that simulates a realistic clinical discussion
- Outputs a detailed markdown report of the entire diagnostic process

### Output

The system generates a comprehensive report (`medical_case_analysis.md` by default, renamed by `run_team.py`) that includes:

1.  Executive summary of the case
2.  Initial differential diagnosis from the Primary Diagnostician
3.  Critical review from the Diagnostic Reviewer
4.  Discussion points and resolution of disagreements
5.  Final consensus differential diagnosis list (prioritized)
6.  Recommended next steps for diagnosis confirmation
7.  Initial management recommendations

## Documentation

For more detailed information about CrewAI, refer to the `crewai_documentation.md` file in this repository.

For project milestones and current status, see the `project_milestone.md` file.
