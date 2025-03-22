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

To run different team configurations with various medical cases, you'll need to:

1. **Activate the virtual environment** (as described above)
2. **Modify the `crew.py` file** to use the desired team configuration:
   
   ```python
   # In crew.py, change this line:
   agents_config = 'config/agents_team1.yaml'  # Change to agents_team2.yaml, agents_team3.yaml, or agents_team4.yaml
   ```

3. **Run the crew** with a specific medical case:
   
   ```bash
   # Make sure you're in the agent_board_v2 directory
   cd agent_board_v2
   
   # Run the crew
   crewai run
   ```

## Dependencies

- Python 3.12 has been installed
- Virtual environment has been created
- uv and CrewAI have been installed as per the README.md instructions

## Current Files

- README.md: Project documentation and setup instructions
- crewai_documentation.md: Reference documentation for CrewAI
- CURRENT_STATE.md: This file, documenting the current state of the project
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
