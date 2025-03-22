# Agent Board v2: Medical Differential Diagnosis System

This project uses CrewAI to create a system where a Department Chief of Internal Medicine leads two general medicine internists in a natural clinical discussion to develop a differential diagnosis with detailed reasoning.

## Requirements

- Python >=3.10 and <3.13 (Project is set up with Python 3.12)
- uv (dependency management tool)

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

### 3. Install CrewAI

With the virtual environment activated, install CrewAI:

```bash
uv tool install crewai
```

If you encounter a PATH warning, run:
```bash
uv tool update-shell
```

Verify the installation:
```bash
uv tool list
```

### 4. Project Structure

To generate the project scaffolding, run:

```bash
crewai create crew agent_board_v2
```

This will create the necessary project structure with configuration files for agents and tasks.

### 5. Running the Crew

Before running your crew, install dependencies:

```bash
crewai install
```

To run your crew:

```bash
crewai run
```

## Team Configurations

The project includes four different team configurations to study how team dynamics affect diagnostic accuracy:

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

### Running Different Team Configurations

The project includes a `run_team.py` script that makes it easy to run different team configurations with different medical cases:

```bash
# Make sure you're in the agent_board_v2 directory and the virtual environment is activated
cd agent_board_v2
source ../venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate  # On Windows

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

## Project Structure

```
agent_board_v2/
├── .gitignore
├── knowledge/           # Directory for medical knowledge base
├── output/              # Directory for analysis results
├── pyproject.toml
├── README.md
├── .env
├── run_team.py          # Script to run different team configurations
├── cases/               # Medical cases directory
│   ├── case_list.csv    # List of cases with true diagnoses
│   ├── stage_1/         # Initial presentations without lab results
│   └── stage_2/         # Same presentations plus lab results and imaging
└── src/
    └── agent_board_v2/
        ├── __init__.py
        ├── main.py
        ├── crew.py
        ├── tools/
        │   ├── custom_tool.py
        │   └── __init__.py
        └── config/
            ├── agents.yaml           # Original agent configuration
            ├── agents_team1.yaml     # Collaborative team configuration
            ├── agents_team2.yaml     # Mixed team configuration
            ├── agents_team3.yaml     # Difficult team configuration
            ├── agents_team4.yaml     # Baseline team configuration
            └── tasks.yaml
```

## Implementation Details

### Agent Roles

The system includes three medical professionals:

1. **Department Chief of Internal Medicine (Senior Internist)**: 
   - Acts as the team leader and manager in the hierarchical process
   - Coordinates the diagnostic discussion
   - Delegates tasks to the other internists
   - Synthesizes the team's findings into a final diagnosis

2. **Primary Diagnostician (Internist One)**:
   - Develops the initial differential diagnosis
   - Provides detailed clinical reasoning for each potential diagnosis
   - Prioritizes diagnoses based on likelihood and clinical significance

3. **Diagnostic Reviewer (Internist Two)**:
   - Critically reviews the initial differential diagnosis
   - Identifies potential missed diagnoses or misinterpretations
   - Suggests additional diagnostic tests or information
   - Provides alternative assessments of likelihood and priority

### Workflow

The system uses a hierarchical process to simulate a natural clinical discussion:

1. The Department Chief presents the medical case to the team
2. The Chief asks the Primary Diagnostician to develop an initial differential diagnosis
3. The Chief then asks the Diagnostic Reviewer to critique the initial assessment
4. The Chief facilitates a discussion between both internists to resolve disagreements
5. The team collaboratively develops a final consensus diagnosis
6. The Chief finalizes a comprehensive report with management recommendations

### Technical Implementation

- Uses CrewAI's hierarchical process with the Department Chief as manager
- Enables memory for all agents to maintain conversation context
- Implements a single comprehensive task that simulates a realistic clinical discussion
- Outputs a detailed markdown report of the entire diagnostic process

### Output

The system generates a comprehensive report that includes:

1. Executive summary of the case
2. Initial differential diagnosis from the Primary Diagnostician
3. Critical review from the Diagnostic Reviewer
4. Discussion points and resolution of disagreements
5. Final consensus differential diagnosis list (prioritized)
6. Recommended next steps for diagnosis confirmation
7. Initial management recommendations

## Documentation

For more detailed information about CrewAI, refer to the `crewai_documentation.md` file in this repository.

For the current state of the project and implementation details, see the `CURRENT_STATE.md` file.
