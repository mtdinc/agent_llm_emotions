from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class AgentBoardV2():
    """Medical Differential Diagnosis System with two collaborating internists"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents_team1.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def senior_internist(self) -> Agent:
        return Agent(
            role="Chief Internist",
            goal="Lead the diagnostic team, coordinate the collaborative process between internists, synthesize their findings, and ensure a comprehensive and accurate final differential diagnosis.",
            backstory="You're a highly respected Department Chief of Internal Medicine with over 25 years of clinical experience. You excel at synthesizing diverse clinical perspectives and guiding teams toward accurate diagnoses.",
            verbose=True,
            allow_delegation=True,
            allowed_agents=["Primary Diagnostician", "Diagnostic Reviewer"],
            memory=True,  # Enable memory to remember interactions
            max_iter=3  # Prevent infinite loops
        )
        
    @agent
    def internist_one(self) -> Agent:
        return Agent(
            role="Primary Diagnostician",
            goal="Analyze the presented medical case thoroughly, develop an initial differential diagnosis list with detailed reasoning, and prioritize diagnoses based on likelihood and clinical significance.",
            backstory="You're a highly experienced general medicine internist with over 15 years of clinical practice and a reputation for diagnostic excellence.",
            verbose=True,
            allow_delegation=False,
            memory=True  # Enable memory to remember interactions
        )

    @agent
    def internist_two(self) -> Agent:
        return Agent(
            role="Diagnostic Reviewer",
            goal="Critically review the initial differential diagnosis, identify any missed diagnoses or misinterpretations, and suggest additional diagnostic tests if needed.",
            backstory="You're a distinguished general medicine internist with 20 years of experience, including 10 years as a clinical educator and diagnostic consultant.",
            verbose=True,
            allow_delegation=False,
            memory=True  # Enable memory to remember interactions
        )

    # Single task for the entire medical case analysis
    @task
    def medical_case_analysis(self) -> Task:
        return Task(
            config=self.tasks_config['medical_case_analysis'],
            output_file='medical_case_analysis.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Medical Differential Diagnosis crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=[
                # The manager agent should not be included in the agents list
                self.internist_one(),
                self.internist_two()
            ], # Only include non-manager agents in the agents list
            tasks=[self.medical_case_analysis()], # Single task for the entire case analysis
            process=Process.hierarchical, # Hierarchical process with Department Chief as manager
            manager_agent=self.senior_internist(), # Department Chief leads the team
            verbose=True,
            full_output=True, # Get detailed output from the task
            output_log_file=True, # Log the execution for debugging
        )
