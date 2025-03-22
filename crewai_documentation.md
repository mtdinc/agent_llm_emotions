Installation
Get started with CrewAI - Install, configure, and build your first AI crew
Python Version Requirements

CrewAI requires Python >=3.10 and <3.13. Here’s how to check your version:


python3 --version
If you need to update Python, visit python.org/downloads
CrewAI uses the uv as its dependency management and package handling tool. It simplifies project setup and execution, offering a seamless experience.

If you haven’t installed uv yet, follow step 1 to quickly get it set up on your system, else you can skip to step 2.

1
Install uv

On macOS/Linux:

Use curl to download the script and execute it with sh:


curl -LsSf https://astral.sh/uv/install.sh | sh
If your system doesn’t have curl, you can use wget:


wget -qO- https://astral.sh/uv/install.sh | sh
On Windows:

Use irm to download the script and iex to execute it:


powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
If you run into any issues, refer to UV’s installation guide for more information.

2
Install CrewAI 🚀

Run the following command to install crewai CLI:


uv tool install crewai
If you encounter a PATH warning, run this command to update your shell:


uv tool update-shell
To verify that crewai is installed, run:


uv tool list
You should see something like:


crewai v0.102.0
- crewai
If you need to update crewai, run:


uv tool install crewai --upgrade
Installation successful! You’re ready to create your first crew! 🎉

Creating a CrewAI Project

We recommend using the YAML template scaffolding for a structured approach to defining agents and tasks. Here’s how to get started:

1
Generate Project Scaffolding

Run the crewai CLI command:


crewai create crew <your_project_name>
This creates a new project with the following structure:


my_project/
├── .gitignore
├── knowledge/
├── pyproject.toml
├── README.md
├── .env
└── src/
    └── my_project/
        ├── __init__.py
        ├── main.py
        ├── crew.py
        ├── tools/
        │   ├── custom_tool.py
        │   └── __init__.py
        └── config/
            ├── agents.yaml
            └── tasks.yaml
2
Customize Your Project

Your project will contain these essential files:

File	Purpose
agents.yaml	Define your AI agents and their roles
tasks.yaml	Set up agent tasks and workflows
.env	Store API keys and environment variables
main.py	Project entry point and execution flow
crew.py	Crew orchestration and coordination
tools/	Directory for custom agent tools
knowledge/	Directory for knowledge base
Start by editing agents.yaml and tasks.yaml to define your crew’s behavior.

Keep sensitive information like API keys in .env.

3
Run your Crew

Before you run your crew, make sure to run:

crewai install
If you need to install additional packages, use:

uv add <package-name>
To run your crew, execute the following command in the root of your project:

crewai run


=====

AI Agent COncept:
Core Concepts
Agents
Detailed guide on creating and managing agents within the CrewAI framework.

Overview of an Agent

In the CrewAI framework, an Agent is an autonomous unit that can:

Perform specific tasks
Make decisions based on its role and goal
Use tools to accomplish objectives
Communicate and collaborate with other agents
Maintain memory of interactions
Delegate tasks when allowed
Think of an agent as a specialized team member with specific skills, expertise, and responsibilities. For example, a Researcher agent might excel at gathering and analyzing information, while a Writer agent might be better at creating content.

Agent Attributes

Attribute   Parameter   Type    Description
Role    role    str Defines the agent’s function and expertise within the crew.
Goal    goal    str The individual objective that guides the agent’s decision-making.
Backstory   backstory   str Provides context and personality to the agent, enriching interactions.
LLM (optional)  llm Union[str, LLM, Any]    Language model that powers the agent. Defaults to the model specified in OPENAI_MODEL_NAME or “gpt-4”.
Tools (optional)    tools   List[BaseTool]  Capabilities or functions available to the agent. Defaults to an empty list.
Function Calling LLM (optional) function_calling_llm    Optional[Any]   Language model for tool calling, overrides crew’s LLM if specified.
Max Iterations (optional)   max_iter    int Maximum iterations before the agent must provide its best answer. Default is 20.
Max RPM (optional)  max_rpm Optional[int]   Maximum requests per minute to avoid rate limits.
Max Execution Time (optional)   max_execution_time  Optional[int]   Maximum time (in seconds) for task execution.
Memory (optional)   memory  bool    Whether the agent should maintain memory of interactions. Default is True.
Verbose (optional)  verbose bool    Enable detailed execution logs for debugging. Default is False.
Allow Delegation (optional) allow_delegation    bool    Allow the agent to delegate tasks to other agents. Default is False.
Step Callback (optional)    step_callback   Optional[Any]   Function called after each agent step, overrides crew callback.
Cache (optional)    cache   bool    Enable caching for tool usage. Default is True.
System Template (optional)  system_template Optional[str]   Custom system prompt template for the agent.
Prompt Template (optional)  prompt_template Optional[str]   Custom prompt template for the agent.
Response Template (optional)    response_template   Optional[str]   Custom response template for the agent.
Allow Code Execution (optional) allow_code_execution    Optional[bool]  Enable code execution for the agent. Default is False.
Max Retry Limit (optional)  max_retry_limit int Maximum number of retries when an error occurs. Default is 2.
Respect Context Window (optional)   respect_context_window  bool    Keep messages under context window size by summarizing. Default is True.
Code Execution Mode (optional)  code_execution_mode Literal["safe", "unsafe"]   Mode for code execution: ‘safe’ (using Docker) or ‘unsafe’ (direct). Default is ‘safe’.
Embedder (optional) embedder    Optional[Dict[str, Any]]    Configuration for the embedder used by the agent.
Knowledge Sources (optional)    knowledge_sources   Optional[List[BaseKnowledgeSource]] Knowledge sources available to the agent.
Use System Prompt (optional)    use_system_prompt   Optional[bool]  Whether to use system prompt (for o1 model support). Default is True.

Creating Agents

There are two ways to create agents in CrewAI: using YAML configuration (recommended) or defining them directly in code.


YAML Configuration (Recommended)

Using YAML configuration provides a cleaner, more maintainable way to define agents. We strongly recommend using this approach in your CrewAI projects.

After creating your CrewAI project as outlined in the Installation section, navigate to the src/latest_ai_development/config/agents.yaml file and modify the template to match your requirements.

Variables in your YAML files (like {topic}) will be replaced with values from your inputs when running the crew:

Code


crew.kickoff(inputs={'topic': 'AI Agents'})
Here’s an example of how to configure agents using YAML:

agents.yaml


# src/latest_ai_development/config/agents.yaml
researcher:
  role: >
    {topic} Senior Data Researcher
  goal: >
    Uncover cutting-edge developments in {topic}
  backstory: >
    You're a seasoned researcher with a knack for uncovering the latest
    developments in {topic}. Known for your ability to find the most relevant
    information and present it in a clear and concise manner.

reporting_analyst:
  role: >
    {topic} Reporting Analyst
  goal: >
    Create detailed reports based on {topic} data analysis and research findings
  backstory: >
    You're a meticulous analyst with a keen eye for detail. You're known for
    your ability to turn complex data into clear and concise reports, making
    it easy for others to understand and act on the information you provide.
To use this YAML configuration in your code, create a crew class that inherits from CrewBase:

Code


# src/latest_ai_development/crew.py
from crewai import Agent, Crew, Process
from crewai.project import CrewBase, agent, crew
from crewai_tools import SerperDevTool

@CrewBase
class LatestAiDevelopmentCrew():
  """LatestAiDevelopment crew"""

  agents_config = "config/agents.yaml"

  @agent
  def researcher(self) -> Agent:
    return Agent(
      config=self.agents_config['researcher'],
      verbose=True,
      tools=[SerperDevTool()]
    )

  @agent
  def reporting_analyst(self) -> Agent:
    return Agent(
      config=self.agents_config['reporting_analyst'],
      verbose=True
    )
The names you use in your YAML files (agents.yaml) should match the method names in your Python code.

Direct Code Definition

You can create agents directly in code by instantiating the Agent class. Here’s a comprehensive example showing all available parameters:

Code


from crewai import Agent
from crewai_tools import SerperDevTool

# Create an agent with all available parameters
agent = Agent(
    role="Senior Data Scientist",
    goal="Analyze and interpret complex datasets to provide actionable insights",
    backstory="With over 10 years of experience in data science and machine learning, "
              "you excel at finding patterns in complex datasets.",
    llm="gpt-4",  # Default: OPENAI_MODEL_NAME or "gpt-4"
    function_calling_llm=None,  # Optional: Separate LLM for tool calling
    memory=True,  # Default: True
    verbose=False,  # Default: False
    allow_delegation=False,  # Default: False
    max_iter=20,  # Default: 20 iterations
    max_rpm=None,  # Optional: Rate limit for API calls
    max_execution_time=None,  # Optional: Maximum execution time in seconds
    max_retry_limit=2,  # Default: 2 retries on error
    allow_code_execution=False,  # Default: False
    code_execution_mode="safe",  # Default: "safe" (options: "safe", "unsafe")
    respect_context_window=True,  # Default: True
    use_system_prompt=True,  # Default: True
    tools=[SerperDevTool()],  # Optional: List of tools
    knowledge_sources=None,  # Optional: List of knowledge sources
    embedder=None,  # Optional: Custom embedder configuration
    system_template=None,  # Optional: Custom system prompt template
    prompt_template=None,  # Optional: Custom prompt template
    response_template=None,  # Optional: Custom response template
    step_callback=None,  # Optional: Callback function for monitoring
)
Let’s break down some key parameter combinations for common use cases:


Basic Research Agent

Code


research_agent = Agent(
    role="Research Analyst",
    goal="Find and summarize information about specific topics",
    backstory="You are an experienced researcher with attention to detail",
    tools=[SerperDevTool()],
    verbose=True  # Enable logging for debugging
)

Code Development Agent

Code


dev_agent = Agent(
    role="Senior Python Developer",
    goal="Write and debug Python code",
    backstory="Expert Python developer with 10 years of experience",
    allow_code_execution=True,
    code_execution_mode="safe",  # Uses Docker for safety
    max_execution_time=300,  # 5-minute timeout
    max_retry_limit=3  # More retries for complex code tasks
)

Long-Running Analysis Agent

Code


analysis_agent = Agent(
    role="Data Analyst",
    goal="Perform deep analysis of large datasets",
    backstory="Specialized in big data analysis and pattern recognition",
    memory=True,
    respect_context_window=True,
    max_rpm=10,  # Limit API calls
    function_calling_llm="gpt-4o-mini"  # Cheaper model for tool calls
)

Custom Template Agent

Code


custom_agent = Agent(
    role="Customer Service Representative",
    goal="Assist customers with their inquiries",
    backstory="Experienced in customer support with a focus on satisfaction",
    system_template="""<|start_header_id|>system<|end_header_id|>
                        {{ .System }}<|eot_id|>""",
    prompt_template="""<|start_header_id|>user<|end_header_id|>
                        {{ .Prompt }}<|eot_id|>""",
    response_template="""<|start_header_id|>assistant<|end_header_id|>
                        {{ .Response }}<|eot_id|>""",
)

Parameter Details


Critical Parameters

role, goal, and backstory are required and shape the agent’s behavior
llm determines the language model used (default: OpenAI’s GPT-4)

Memory and Context

memory: Enable to maintain conversation history
respect_context_window: Prevents token limit issues
knowledge_sources: Add domain-specific knowledge bases

Execution Control

max_iter: Maximum attempts before giving best answer
max_execution_time: Timeout in seconds
max_rpm: Rate limiting for API calls
max_retry_limit: Retries on error

Code Execution

allow_code_execution: Must be True to run code
code_execution_mode:
"safe": Uses Docker (recommended for production)
"unsafe": Direct execution (use only in trusted environments)

Templates

system_template: Defines agent’s core behavior
prompt_template: Structures input format
response_template: Formats agent responses
When using custom templates, you can use variables like {role}, {goal}, and {input} in your templates. These will be automatically populated during execution.

Agent Tools

Agents can be equipped with various tools to enhance their capabilities. CrewAI supports tools from:

CrewAI Toolkit
LangChain Tools
Here’s how to add tools to an agent:

Code


from crewai import Agent
from crewai_tools import SerperDevTool, WikipediaTools

# Create tools
search_tool = SerperDevTool()
wiki_tool = WikipediaTools()

# Add tools to agent
researcher = Agent(
    role="AI Technology Researcher",
    goal="Research the latest AI developments",
    tools=[search_tool, wiki_tool],
    verbose=True
)

Agent Memory and Context

Agents can maintain memory of their interactions and use context from previous tasks. This is particularly useful for complex workflows where information needs to be retained across multiple tasks.

Code


from crewai import Agent

analyst = Agent(
    role="Data Analyst",
    goal="Analyze and remember complex data patterns",
    memory=True,  # Enable memory
    verbose=True
)
When memory is enabled, the agent will maintain context across multiple interactions, improving its ability to handle complex, multi-step tasks.

Important Considerations and Best Practices


Security and Code Execution

When using allow_code_execution, be cautious with user input and always validate it
Use code_execution_mode: "safe" (Docker) in production environments
Consider setting appropriate max_execution_time limits to prevent infinite loops

Performance Optimization

Use respect_context_window: true to prevent token limit issues
Set appropriate max_rpm to avoid rate limiting
Enable cache: true to improve performance for repetitive tasks
Adjust max_iter and max_retry_limit based on task complexity

Memory and Context Management

Use memory: true for tasks requiring historical context
Leverage knowledge_sources for domain-specific information
Configure embedder_config when using custom embedding models
Use custom templates (system_template, prompt_template, response_template) for fine-grained control over agent behavior

Agent Collaboration

Enable allow_delegation: true when agents need to work together
Use step_callback to monitor and log agent interactions
Consider using different LLMs for different purposes:
Main llm for complex reasoning
function_calling_llm for efficient tool usage

Model Compatibility

Set use_system_prompt: false for older models that don’t support system messages
Ensure your chosen llm supports the features you need (like function calling)

Troubleshooting Common Issues

Rate Limiting: If you’re hitting API rate limits:

Implement appropriate max_rpm
Use caching for repetitive operations
Consider batching requests
Context Window Errors: If you’re exceeding context limits:

Enable respect_context_window
Use more efficient prompts
Clear agent memory periodically
Code Execution Issues: If code execution fails:

Verify Docker is installed for safe mode
Check execution permissions
Review code sandbox settings
Memory Issues: If agent responses seem inconsistent:

Verify memory is enabled
Check knowledge source configuration
Review conversation history management
Remember that agents are most effective when configured according to their specific use case. Take time to understand your requirements and adjust these parameters accordingly.
Was this page helpful?

Yes

======
Tasks
Core Concepts
Tasks
Detailed guide on managing and creating tasks within the CrewAI framework.

Overview of a Task

In the CrewAI framework, a Task is a specific assignment completed by an Agent.

Tasks provide all necessary details for execution, such as a description, the agent responsible, required tools, and more, facilitating a wide range of action complexities.

Tasks within CrewAI can be collaborative, requiring multiple agents to work together. This is managed through the task properties and orchestrated by the Crew’s process, enhancing teamwork and efficiency.


Task Execution Flow

Tasks can be executed in two ways:

Sequential: Tasks are executed in the order they are defined
Hierarchical: Tasks are assigned to agents based on their roles and expertise
The execution flow is defined when creating the crew:

Code


crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    process=Process.sequential  # or Process.hierarchical
)

Task Attributes

Attribute   Parameters  Type    Description
Description description str A clear, concise statement of what the task entails.
Expected Output expected_output str A detailed description of what the task’s completion looks like.
Name (optional) name    Optional[str]   A name identifier for the task.
Agent (optional)    agent   Optional[BaseAgent] The agent responsible for executing the task.
Tools (optional)    tools   List[BaseTool]  The tools/resources the agent is limited to use for this task.
Context (optional)  context Optional[List["Task"]]  Other tasks whose outputs will be used as context for this task.
Async Execution (optional)  async_execution Optional[bool]  Whether the task should be executed asynchronously. Defaults to False.
Human Input (optional)  human_input Optional[bool]  Whether the task should have a human review the final answer of the agent. Defaults to False.
Config (optional)   config  Optional[Dict[str, Any]]    Task-specific configuration parameters.
Output File (optional)  output_file Optional[str]   File path for storing the task output.
Output JSON (optional)  output_json Optional[Type[BaseModel]]   A Pydantic model to structure the JSON output.
Output Pydantic (optional)  output_pydantic Optional[Type[BaseModel]]   A Pydantic model for task output.
Callback (optional) callback    Optional[Any]   Function/object to be executed after task completion.

Creating Tasks

There are two ways to create tasks in CrewAI: using YAML configuration (recommended) or defining them directly in code.


YAML Configuration (Recommended)

Using YAML configuration provides a cleaner, more maintainable way to define tasks. We strongly recommend using this approach to define tasks in your CrewAI projects.

After creating your CrewAI project as outlined in the Installation section, navigate to the src/latest_ai_development/config/tasks.yaml file and modify the template to match your specific task requirements.

Variables in your YAML files (like {topic}) will be replaced with values from your inputs when running the crew:

Code


crew.kickoff(inputs={'topic': 'AI Agents'})
Here’s an example of how to configure tasks using YAML:

tasks.yaml


research_task:
  description: >
    Conduct a thorough research about {topic}
    Make sure you find any interesting and relevant information given
    the current year is 2025.
  expected_output: >
    A list with 10 bullet points of the most relevant information about {topic}
  agent: researcher

reporting_task:
  description: >
    Review the context you got and expand each topic into a full section for a report.
    Make sure the report is detailed and contains any and all relevant information.
  expected_output: >
    A fully fledge reports with the mains topics, each with a full section of information.
    Formatted as markdown without '```'
  agent: reporting_analyst
  output_file: report.md
To use this YAML configuration in your code, create a crew class that inherits from CrewBase:

crew.py


# src/latest_ai_development/crew.py

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

@CrewBase
class LatestAiDevelopmentCrew():
  """LatestAiDevelopment crew"""

  @agent
  def researcher(self) -> Agent:
    return Agent(
      config=self.agents_config['researcher'],
      verbose=True,
      tools=[SerperDevTool()]
    )

  @agent
  def reporting_analyst(self) -> Agent:
    return Agent(
      config=self.agents_config['reporting_analyst'],
      verbose=True
    )

  @task
  def research_task(self) -> Task:
    return Task(
      config=self.tasks_config['research_task']
    )

  @task
  def reporting_task(self) -> Task:
    return Task(
      config=self.tasks_config['reporting_task']
    )

  @crew
  def crew(self) -> Crew:
    return Crew(
      agents=[
        self.researcher(),
        self.reporting_analyst()
      ],
      tasks=[
        self.research_task(),
        self.reporting_task()
      ],
      process=Process.sequential
    )
The names you use in your YAML files (agents.yaml and tasks.yaml) should match the method names in your Python code.

Direct Code Definition (Alternative)

Alternatively, you can define tasks directly in your code without using YAML configuration:

task.py


from crewai import Task

research_task = Task(
    description="""
        Conduct a thorough research about AI Agents.
        Make sure you find any interesting and relevant information given
        the current year is 2025.
    """,
    expected_output="""
        A list with 10 bullet points of the most relevant information about AI Agents
    """,
    agent=researcher
)

reporting_task = Task(
    description="""
        Review the context you got and expand each topic into a full section for a report.
        Make sure the report is detailed and contains any and all relevant information.
    """,
    expected_output="""
        A fully fledge reports with the mains topics, each with a full section of information.
        Formatted as markdown without '```'
    """,
    agent=reporting_analyst,
    output_file="report.md"
)
Directly specify an agent for assignment or let the hierarchical CrewAI’s process decide based on roles, availability, etc.

Task Output

Understanding task outputs is crucial for building effective AI workflows. CrewAI provides a structured way to handle task results through the TaskOutput class, which supports multiple output formats and can be easily passed between tasks.

The output of a task in CrewAI framework is encapsulated within the TaskOutput class. This class provides a structured way to access results of a task, including various formats such as raw output, JSON, and Pydantic models.

By default, the TaskOutput will only include the raw output. A TaskOutput will only include the pydantic or json_dict output if the original Task object was configured with output_pydantic or output_json, respectively.


Task Output Attributes

Attribute   Parameters  Type    Description
Description description str Description of the task.
Summary summary Optional[str]   Summary of the task, auto-generated from the first 10 words of the description.
Raw raw str The raw output of the task. This is the default format for the output.
Pydantic    pydantic    Optional[BaseModel] A Pydantic model object representing the structured output of the task.
JSON Dict   json_dict   Optional[Dict[str, Any]]    A dictionary representing the JSON output of the task.
Agent   agent   str The agent that executed the task.
Output Format   output_format   OutputFormat    The format of the task output, with options including RAW, JSON, and Pydantic. The default is RAW.

Task Methods and Properties

Method/Property Description
json    Returns the JSON string representation of the task output if the output format is JSON.
to_dict Converts the JSON and Pydantic outputs to a dictionary.
str Returns the string representation of the task output, prioritizing Pydantic, then JSON, then raw.

Accessing Task Outputs

Once a task has been executed, its output can be accessed through the output attribute of the Task object. The TaskOutput class provides various ways to interact with and present this output.


Example

Code


# Example task
task = Task(
    description='Find and summarize the latest AI news',
    expected_output='A bullet list summary of the top 5 most important AI news',
    agent=research_agent,
    tools=[search_tool]
)

# Execute the crew
crew = Crew(
    agents=[research_agent],
    tasks=[task],
    verbose=True
)

result = crew.kickoff()

# Accessing the task output
task_output = task.output

print(f"Task Description: {task_output.description}")
print(f"Task Summary: {task_output.summary}")
print(f"Raw Output: {task_output.raw}")
if task_output.json_dict:
    print(f"JSON Output: {json.dumps(task_output.json_dict, indent=2)}")
if task_output.pydantic:
    print(f"Pydantic Output: {task_output.pydantic}")

Task Dependencies and Context

Tasks can depend on the output of other tasks using the context attribute. For example:

Code


research_task = Task(
    description="Research the latest developments in AI",
    expected_output="A list of recent AI developments",
    agent=researcher
)

analysis_task = Task(
    description="Analyze the research findings and identify key trends",
    expected_output="Analysis report of AI trends",
    agent=analyst,
    context=[research_task]  # This task will wait for research_task to complete
)

Task Guardrails

Task guardrails provide a way to validate and transform task outputs before they are passed to the next task. This feature helps ensure data quality and provides feedback to agents when their output doesn’t meet specific criteria.


Using Task Guardrails

To add a guardrail to a task, provide a validation function through the guardrail parameter:

Code


from typing import Tuple, Union, Dict, Any

def validate_blog_content(result: str) -> Tuple[bool, Union[Dict[str, Any], str]]:
    """Validate blog content meets requirements."""
    try:
        # Check word count
        word_count = len(result.split())
        if word_count > 200:
            return (False, {
                "error": "Blog content exceeds 200 words",
                "code": "WORD_COUNT_ERROR",
                "context": {"word_count": word_count}
            })

        # Additional validation logic here
        return (True, result.strip())
    except Exception as e:
        return (False, {
            "error": "Unexpected error during validation",
            "code": "SYSTEM_ERROR"
        })

blog_task = Task(
    description="Write a blog post about AI",
    expected_output="A blog post under 200 words",
    agent=blog_agent,
    guardrail=validate_blog_content  # Add the guardrail function
)

Guardrail Function Requirements

Function Signature:

Must accept exactly one parameter (the task output)
Should return a tuple of (bool, Any)
Type hints are recommended but optional
Return Values:

Success: Return (True, validated_result)
Failure: Return (False, error_details)

Error Handling Best Practices

Structured Error Responses:
Code


def validate_with_context(result: str) -> Tuple[bool, Union[Dict[str, Any], str]]:
    try:
        # Main validation logic
        validated_data = perform_validation(result)
        return (True, validated_data)
    except ValidationError as e:
        return (False, {
            "error": str(e),
            "code": "VALIDATION_ERROR",
            "context": {"input": result}
        })
    except Exception as e:
        return (False, {
            "error": "Unexpected error",
            "code": "SYSTEM_ERROR"
        })
Error Categories:

Use specific error codes
Include relevant context
Provide actionable feedback
Validation Chain:

Code


from typing import Any, Dict, List, Tuple, Union

def complex_validation(result: str) -> Tuple[bool, Union[str, Dict[str, Any]]]:
    """Chain multiple validation steps."""
    # Step 1: Basic validation
    if not result:
        return (False, {"error": "Empty result", "code": "EMPTY_INPUT"})

    # Step 2: Content validation
    try:
        validated = validate_content(result)
        if not validated:
            return (False, {"error": "Invalid content", "code": "CONTENT_ERROR"})

        # Step 3: Format validation
        formatted = format_output(validated)
        return (True, formatted)
    except Exception as e:
        return (False, {
            "error": str(e),
            "code": "VALIDATION_ERROR",
            "context": {"step": "content_validation"}
        })

Handling Guardrail Results

When a guardrail returns (False, error):

The error is sent back to the agent
The agent attempts to fix the issue
The process repeats until:
The guardrail returns (True, result)
Maximum retries are reached
Example with retry handling:

Code


from typing import Optional, Tuple, Union

def validate_json_output(result: str) -> Tuple[bool, Union[Dict[str, Any], str]]:
    """Validate and parse JSON output."""
    try:
        # Try to parse as JSON
        data = json.loads(result)
        return (True, data)
    except json.JSONDecodeError as e:
        return (False, {
            "error": "Invalid JSON format",
            "code": "JSON_ERROR",
            "context": {"line": e.lineno, "column": e.colno}
        })

task = Task(
    description="Generate a JSON report",
    expected_output="A valid JSON object",
    agent=analyst,
    guardrail=validate_json_output,
    max_retries=3  # Limit retry attempts
)

Getting Structured Consistent Outputs from Tasks

It’s also important to note that the output of the final task of a crew becomes the final output of the actual crew itself.

Using output_pydantic

The output_pydantic property allows you to define a Pydantic model that the task output should conform to. This ensures that the output is not only structured but also validated according to the Pydantic model.

Here’s an example demonstrating how to use output_pydantic:

Code


import json

from crewai import Agent, Crew, Process, Task
from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    content: str


blog_agent = Agent(
    role="Blog Content Generator Agent",
    goal="Generate a blog title and content",
    backstory="""You are an expert content creator, skilled in crafting engaging and informative blog posts.""",
    verbose=False,
    allow_delegation=False,
    llm="gpt-4o",
)

task1 = Task(
    description="""Create a blog title and content on a given topic. Make sure the content is under 200 words.""",
    expected_output="A compelling blog title and well-written content.",
    agent=blog_agent,
    output_pydantic=Blog,
)

# Instantiate your crew with a sequential process
crew = Crew(
    agents=[blog_agent],
    tasks=[task1],
    verbose=True,
    process=Process.sequential,
)

result = crew.kickoff()

# Option 1: Accessing Properties Using Dictionary-Style Indexing
print("Accessing Properties - Option 1")
title = result["title"]
content = result["content"]
print("Title:", title)
print("Content:", content)

# Option 2: Accessing Properties Directly from the Pydantic Model
print("Accessing Properties - Option 2")
title = result.pydantic.title
content = result.pydantic.content
print("Title:", title)
print("Content:", content)

# Option 3: Accessing Properties Using the to_dict() Method
print("Accessing Properties - Option 3")
output_dict = result.to_dict()
title = output_dict["title"]
content = output_dict["content"]
print("Title:", title)
print("Content:", content)

# Option 4: Printing the Entire Blog Object
print("Accessing Properties - Option 5")
print("Blog:", result)

In this example:

A Pydantic model Blog is defined with title and content fields.
The task task1 uses the output_pydantic property to specify that its output should conform to the Blog model.
After executing the crew, you can access the structured output in multiple ways as shown.

Explanation of Accessing the Output

Dictionary-Style Indexing: You can directly access the fields using result[“field_name”]. This works because the CrewOutput class implements the getitem method.
Directly from Pydantic Model: Access the attributes directly from the result.pydantic object.
Using to_dict() Method: Convert the output to a dictionary and access the fields.
Printing the Entire Object: Simply print the result object to see the structured output.

Using output_json

The output_json property allows you to define the expected output in JSON format. This ensures that the task’s output is a valid JSON structure that can be easily parsed and used in your application.

Here’s an example demonstrating how to use output_json:

Code


import json

from crewai import Agent, Crew, Process, Task
from pydantic import BaseModel


# Define the Pydantic model for the blog
class Blog(BaseModel):
    title: str
    content: str


# Define the agent
blog_agent = Agent(
    role="Blog Content Generator Agent",
    goal="Generate a blog title and content",
    backstory="""You are an expert content creator, skilled in crafting engaging and informative blog posts.""",
    verbose=False,
    allow_delegation=False,
    llm="gpt-4o",
)

# Define the task with output_json set to the Blog model
task1 = Task(
    description="""Create a blog title and content on a given topic. Make sure the content is under 200 words.""",
    expected_output="A JSON object with 'title' and 'content' fields.",
    agent=blog_agent,
    output_json=Blog,
)

# Instantiate the crew with a sequential process
crew = Crew(
    agents=[blog_agent],
    tasks=[task1],
    verbose=True,
    process=Process.sequential,
)

# Kickoff the crew to execute the task
result = crew.kickoff()

# Option 1: Accessing Properties Using Dictionary-Style Indexing
print("Accessing Properties - Option 1")
title = result["title"]
content = result["content"]
print("Title:", title)
print("Content:", content)

# Option 2: Printing the Entire Blog Object
print("Accessing Properties - Option 2")
print("Blog:", result)
In this example:

A Pydantic model Blog is defined with title and content fields, which is used to specify the structure of the JSON output.
The task task1 uses the output_json property to indicate that it expects a JSON output conforming to the Blog model.
After executing the crew, you can access the structured JSON output in two ways as shown.

Explanation of Accessing the Output

Accessing Properties Using Dictionary-Style Indexing: You can access the fields directly using result[“field_name”]. This is possible because the CrewOutput class implements the getitem method, allowing you to treat the output like a dictionary. In this option, we’re retrieving the title and content from the result.
Printing the Entire Blog Object: By printing result, you get the string representation of the CrewOutput object. Since the str method is implemented to return the JSON output, this will display the entire output as a formatted string representing the Blog object.
By using output_pydantic or output_json, you ensure that your tasks produce outputs in a consistent and structured format, making it easier to process and utilize the data within your application or across multiple tasks.


Integrating Tools with Tasks

Leverage tools from the CrewAI Toolkit and LangChain Tools for enhanced task performance and agent interaction.


Creating a Task with Tools

Code


import os
os.environ["OPENAI_API_KEY"] = "Your Key"
os.environ["SERPER_API_KEY"] = "Your Key" # serper.dev API key

from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool

research_agent = Agent(
  role='Researcher',
  goal='Find and summarize the latest AI news',
  backstory="""You're a researcher at a large company.
  You're responsible for analyzing data and providing insights
  to the business.""",
  verbose=True
)

# to perform a semantic search for a specified query from a text's content across the internet
search_tool = SerperDevTool()

task = Task(
  description='Find and summarize the latest AI news',
  expected_output='A bullet list summary of the top 5 most important AI news',
  agent=research_agent,
  tools=[search_tool]
)

crew = Crew(
    agents=[research_agent],
    tasks=[task],
    verbose=True
)

result = crew.kickoff()
print(result)
This demonstrates how tasks with specific tools can override an agent’s default set for tailored task execution.


Referring to Other Tasks

In CrewAI, the output of one task is automatically relayed into the next one, but you can specifically define what tasks’ output, including multiple, should be used as context for another task.

This is useful when you have a task that depends on the output of another task that is not performed immediately after it. This is done through the context attribute of the task:

Code


# ...

research_ai_task = Task(
    description="Research the latest developments in AI",
    expected_output="A list of recent AI developments",
    async_execution=True,
    agent=research_agent,
    tools=[search_tool]
)

research_ops_task = Task(
    description="Research the latest developments in AI Ops",
    expected_output="A list of recent AI Ops developments",
    async_execution=True,
    agent=research_agent,
    tools=[search_tool]
)

write_blog_task = Task(
    description="Write a full blog post about the importance of AI and its latest news",
    expected_output="Full blog post that is 4 paragraphs long",
    agent=writer_agent,
    context=[research_ai_task, research_ops_task]
)

#...

Asynchronous Execution

You can define a task to be executed asynchronously. This means that the crew will not wait for it to be completed to continue with the next task. This is useful for tasks that take a long time to be completed, or that are not crucial for the next tasks to be performed.

You can then use the context attribute to define in a future task that it should wait for the output of the asynchronous task to be completed.

Code


#...

list_ideas = Task(
    description="List of 5 interesting ideas to explore for an article about AI.",
    expected_output="Bullet point list of 5 ideas for an article.",
    agent=researcher,
    async_execution=True # Will be executed asynchronously
)

list_important_history = Task(
    description="Research the history of AI and give me the 5 most important events.",
    expected_output="Bullet point list of 5 important events.",
    agent=researcher,
    async_execution=True # Will be executed asynchronously
)

write_article = Task(
    description="Write an article about AI, its history, and interesting ideas.",
    expected_output="A 4 paragraph article about AI.",
    agent=writer,
    context=[list_ideas, list_important_history] # Will wait for the output of the two tasks to be completed
)

#...

Callback Mechanism

The callback function is executed after the task is completed, allowing for actions or notifications to be triggered based on the task’s outcome.

Code


# ...

def callback_function(output: TaskOutput):
    # Do something after the task is completed
    # Example: Send an email to the manager
    print(f"""
        Task completed!
        Task: {output.description}
        Output: {output.raw}
    """)

research_task = Task(
    description='Find and summarize the latest AI news',
    expected_output='A bullet list summary of the top 5 most important AI news',
    agent=research_agent,
    tools=[search_tool],
    callback=callback_function
)

#...

Accessing a Specific Task Output

Once a crew finishes running, you can access the output of a specific task by using the output attribute of the task object:

Code


# ...
task1 = Task(
    description='Find and summarize the latest AI news',
    expected_output='A bullet list summary of the top 5 most important AI news',
    agent=research_agent,
    tools=[search_tool]
)

#...

crew = Crew(
    agents=[research_agent],
    tasks=[task1, task2, task3],
    verbose=True
)

result = crew.kickoff()

# Returns a TaskOutput object with the description and results of the task
print(f"""
    Task completed!
    Task: {task1.output.description}
    Output: {task1.output.raw}
""")

Tool Override Mechanism

Specifying tools in a task allows for dynamic adaptation of agent capabilities, emphasizing CrewAI’s flexibility.


Error Handling and Validation Mechanisms

While creating and executing tasks, certain validation mechanisms are in place to ensure the robustness and reliability of task attributes. These include but are not limited to:

Ensuring only one output type is set per task to maintain clear output expectations.
Preventing the manual assignment of the id attribute to uphold the integrity of the unique identifier system.
These validations help in maintaining the consistency and reliability of task executions within the crewAI framework.


Task Guardrails

Task guardrails provide a powerful way to validate, transform, or filter task outputs before they are passed to the next task. Guardrails are optional functions that execute before the next task starts, allowing you to ensure that task outputs meet specific requirements or formats.


Basic Usage

Code


from typing import Tuple, Union
from crewai import Task

def validate_json_output(result: str) -> Tuple[bool, Union[dict, str]]:
    """Validate that the output is valid JSON."""
    try:
        json_data = json.loads(result)
        return (True, json_data)
    except json.JSONDecodeError:
        return (False, "Output must be valid JSON")

task = Task(
    description="Generate JSON data",
    expected_output="Valid JSON object",
    guardrail=validate_json_output
)

How Guardrails Work

Optional Attribute: Guardrails are an optional attribute at the task level, allowing you to add validation only where needed.
Execution Timing: The guardrail function is executed before the next task starts, ensuring valid data flow between tasks.
Return Format: Guardrails must return a tuple of (success, data):
If success is True, data is the validated/transformed result
If success is False, data is the error message
Result Routing:
On success (True), the result is automatically passed to the next task
On failure (False), the error is sent back to the agent to generate a new answer

Common Use Cases


Data Format Validation

Code


def validate_email_format(result: str) -> Tuple[bool, Union[str, str]]:
    """Ensure the output contains a valid email address."""
    import re
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(email_pattern, result.strip()):
        return (True, result.strip())
    return (False, "Output must be a valid email address")

Content Filtering

Code


def filter_sensitive_info(result: str) -> Tuple[bool, Union[str, str]]:
    """Remove or validate sensitive information."""
    sensitive_patterns = ['SSN:', 'password:', 'secret:']
    for pattern in sensitive_patterns:
        if pattern.lower() in result.lower():
            return (False, f"Output contains sensitive information ({pattern})")
    return (True, result)

Data Transformation

Code


def normalize_phone_number(result: str) -> Tuple[bool, Union[str, str]]:
    """Ensure phone numbers are in a consistent format."""
    import re
    digits = re.sub(r'\D', '', result)
    if len(digits) == 10:
        formatted = f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        return (True, formatted)
    return (False, "Output must be a 10-digit phone number")

Advanced Features


Chaining Multiple Validations

Code


def chain_validations(*validators):
    """Chain multiple validators together."""
    def combined_validator(result):
        for validator in validators:
            success, data = validator(result)
            if not success:
                return (False, data)
            result = data
        return (True, result)
    return combined_validator

# Usage
task = Task(
    description="Get user contact info",
    expected_output="Email and phone",
    guardrail=chain_validations(
        validate_email_format,
        filter_sensitive_info
    )
)

Custom Retry Logic

Code


task = Task(
    description="Generate data",
    expected_output="Valid data",
    guardrail=validate_data,
    max_retries=5  # Override default retry limit
)

Creating Directories when Saving Files

You can now specify if a task should create directories when saving its output to a file. This is particularly useful for organizing outputs and ensuring that file paths are correctly structured.

Code


# ...

save_output_task = Task(
    description='Save the summarized AI news to a file',
    expected_output='File saved successfully',
    agent=research_agent,
    tools=[file_save_tool],
    output_file='outputs/ai_news_summary.txt',
    create_directory=True
)

#...


===== CREWS
Crews
Understanding and utilizing crews in the crewAI framework with comprehensive attributes and functionalities.

What is a Crew?

A crew in crewAI represents a collaborative group of agents working together to achieve a set of tasks. Each crew defines the strategy for task execution, agent collaboration, and the overall workflow.


Crew Attributes

Attribute   Parameters  Description
Tasks   tasks   A list of tasks assigned to the crew.
Agents  agents  A list of agents that are part of the crew.
Process (optional)  process The process flow (e.g., sequential, hierarchical) the crew follows. Default is sequential.
Verbose (optional)  verbose The verbosity level for logging during execution. Defaults to False.
Manager LLM (optional)  manager_llm The language model used by the manager agent in a hierarchical process. Required when using a hierarchical process.
Function Calling LLM (optional) function_calling_llm    If passed, the crew will use this LLM to do function calling for tools for all agents in the crew. Each agent can have its own LLM, which overrides the crew’s LLM for function calling.
Config (optional)   config  Optional configuration settings for the crew, in Json or Dict[str, Any] format.
Max RPM (optional)  max_rpm Maximum requests per minute the crew adheres to during execution. Defaults to None.
Language (optional) language    Language used for the crew, defaults to English.
Language File (optional)    language_file   Path to the language file to be used for the crew.
Memory (optional)   memory  Utilized for storing execution memories (short-term, long-term, entity memory).
Memory Config (optional)    memory_config   Configuration for the memory provider to be used by the crew.
Cache (optional)    cache   Specifies whether to use a cache for storing the results of tools’ execution. Defaults to True.
Embedder (optional) embedder    Configuration for the embedder to be used by the crew. Mostly used by memory for now. Default is {"provider": "openai"}.
Full Output (optional)  full_output Whether the crew should return the full output with all tasks outputs or just the final output. Defaults to False.
Step Callback (optional)    step_callback   A function that is called after each step of every agent. This can be used to log the agent’s actions or to perform other operations; it won’t override the agent-specific step_callback.
Task Callback (optional)    task_callback   A function that is called after the completion of each task. Useful for monitoring or additional operations post-task execution.
Share Crew (optional)   share_crew  Whether you want to share the complete crew information and execution with the crewAI team to make the library better, and allow us to train models.
Output Log File (optional)  output_log_file Set to True to save logs as logs.txt in the current directory or provide a file path. Logs will be in JSON format if the filename ends in .json, otherwise .txt. Defautls to None.
Manager Agent (optional)    manager_agent   manager sets a custom agent that will be used as a manager.
Prompt File (optional)  prompt_file Path to the prompt JSON file to be used for the crew.
Planning (optional) planning    Adds planning ability to the Crew. When activated before each Crew iteration, all Crew data is sent to an AgentPlanner that will plan the tasks and this plan will be added to each task description.
Planning LLM (optional) planning_llm    The language model used by the AgentPlanner in a planning process.
Crew Max RPM: The max_rpm attribute sets the maximum number of requests per minute the crew can perform to avoid rate limits and will override individual agents’ max_rpm settings if you set it.

Creating Crews

There are two ways to create crews in CrewAI: using YAML configuration (recommended) or defining them directly in code.


YAML Configuration (Recommended)

Using YAML configuration provides a cleaner, more maintainable way to define crews and is consistent with how agents and tasks are defined in CrewAI projects.

After creating your CrewAI project as outlined in the Installation section, you can define your crew in a class that inherits from CrewBase and uses decorators to define agents, tasks, and the crew itself.


Example Crew Class with Decorators

code


from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff


@CrewBase
class YourCrewName:
    """Description of your crew"""

    # Paths to your YAML configuration files
    # To see an example agent and task defined in YAML, checkout the following:
    # - Task: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    # - Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    agents_config = 'config/agents.yaml' 
    tasks_config = 'config/tasks.yaml' 

    @before_kickoff
    def prepare_inputs(self, inputs):
        # Modify inputs before the crew starts
        inputs['additional_data'] = "Some extra information"
        return inputs

    @after_kickoff
    def process_output(self, output):
        # Modify output after the crew finishes
        output.raw += "\nProcessed after kickoff."
        return output

    @agent
    def agent_one(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_one'],
            verbose=True
        )

    @agent
    def agent_two(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_two'],
            verbose=True
        )

    @task
    def task_one(self) -> Task:
        return Task(
            config=self.tasks_config['task_one']
        )

    @task
    def task_two(self) -> Task:
        return Task(
            config=self.tasks_config['task_two']
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # Automatically collected by the @agent decorator
            tasks=self.tasks,    # Automatically collected by the @task decorator. 
            process=Process.sequential,
            verbose=True,
        )
Tasks will be executed in the order they are defined.
The CrewBase class, along with these decorators, automates the collection of agents and tasks, reducing the need for manual management.


Decorators overview from annotations.py

CrewAI provides several decorators in the annotations.py file that are used to mark methods within your crew class for special handling:

@CrewBase: Marks the class as a crew base class.
@agent: Denotes a method that returns an Agent object.
@task: Denotes a method that returns a Task object.
@crew: Denotes the method that returns the Crew object.
@before_kickoff: (Optional) Marks a method to be executed before the crew starts.
@after_kickoff: (Optional) Marks a method to be executed after the crew finishes.
These decorators help in organizing your crew’s structure and automatically collecting agents and tasks without manually listing them.


Direct Code Definition (Alternative)

Alternatively, you can define the crew directly in code without using YAML configuration files.

code


from crewai import Agent, Crew, Task, Process
from crewai_tools import YourCustomTool

class YourCrewName:
    def agent_one(self) -> Agent:
        return Agent(
            role="Data Analyst",
            goal="Analyze data trends in the market",
            backstory="An experienced data analyst with a background in economics",
            verbose=True,
            tools=[YourCustomTool()]
        )

    def agent_two(self) -> Agent:
        return Agent(
            role="Market Researcher",
            goal="Gather information on market dynamics",
            backstory="A diligent researcher with a keen eye for detail",
            verbose=True
        )

    def task_one(self) -> Task:
        return Task(
            description="Collect recent market data and identify trends.",
            expected_output="A report summarizing key trends in the market.",
            agent=self.agent_one()
        )

    def task_two(self) -> Task:
        return Task(
            description="Research factors affecting market dynamics.",
            expected_output="An analysis of factors influencing the market.",
            agent=self.agent_two()
        )

    def crew(self) -> Crew:
        return Crew(
            agents=[self.agent_one(), self.agent_two()],
            tasks=[self.task_one(), self.task_two()],
            process=Process.sequential,
            verbose=True
        )
In this example:

Agents and tasks are defined directly within the class without decorators.
We manually create and manage the list of agents and tasks.
This approach provides more control but can be less maintainable for larger projects.

Crew Output

The output of a crew in the CrewAI framework is encapsulated within the CrewOutput class. This class provides a structured way to access results of the crew’s execution, including various formats such as raw strings, JSON, and Pydantic models. The CrewOutput includes the results from the final task output, token usage, and individual task outputs.


Crew Output Attributes

Attribute   Parameters  Type    Description
Raw raw str The raw output of the crew. This is the default format for the output.
Pydantic    pydantic    Optional[BaseModel] A Pydantic model object representing the structured output of the crew.
JSON Dict   json_dict   Optional[Dict[str, Any]]    A dictionary representing the JSON output of the crew.
Tasks Output    tasks_output    List[TaskOutput]    A list of TaskOutput objects, each representing the output of a task in the crew.
Token Usage token_usage Dict[str, Any]  A summary of token usage, providing insights into the language model’s performance during execution.

Crew Output Methods and Properties

Method/Property Description
json    Returns the JSON string representation of the crew output if the output format is JSON.
to_dict Converts the JSON and Pydantic outputs to a dictionary.
**str** Returns the string representation of the crew output, prioritizing Pydantic, then JSON, then raw.

Accessing Crew Outputs

Once a crew has been executed, its output can be accessed through the output attribute of the Crew object. The CrewOutput class provides various ways to interact with and present this output.


Example

Code


# Example crew execution
crew = Crew(
    agents=[research_agent, writer_agent],
    tasks=[research_task, write_article_task],
    verbose=True
)

crew_output = crew.kickoff()

# Accessing the crew output
print(f"Raw Output: {crew_output.raw}")
if crew_output.json_dict:
    print(f"JSON Output: {json.dumps(crew_output.json_dict, indent=2)}")
if crew_output.pydantic:
    print(f"Pydantic Output: {crew_output.pydantic}")
print(f"Tasks Output: {crew_output.tasks_output}")
print(f"Token Usage: {crew_output.token_usage}")

Accessing Crew Logs

You can see real time log of the crew execution, by setting output_log_file as a True(Boolean) or a file_name(str). Supports logging of events as both file_name.txt and file_name.json. In case of True(Boolean) will save as logs.txt.

In case of output_log_file is set as False(Booelan) or None, the logs will not be populated.

Code


# Save crew logs
crew = Crew(output_log_file = True)  # Logs will be saved as logs.txt
crew = Crew(output_log_file = file_name)  # Logs will be saved as file_name.txt
crew = Crew(output_log_file = file_name.txt)  # Logs will be saved as file_name.txt
crew = Crew(output_log_file = file_name.json)  # Logs will be saved as file_name.json

Memory Utilization

Crews can utilize memory (short-term, long-term, and entity memory) to enhance their execution and learning over time. This feature allows crews to store and recall execution memories, aiding in decision-making and task execution strategies.


Cache Utilization

Caches can be employed to store the results of tools’ execution, making the process more efficient by reducing the need to re-execute identical tasks.


Crew Usage Metrics

After the crew execution, you can access the usage_metrics attribute to view the language model (LLM) usage metrics for all tasks executed by the crew. This provides insights into operational efficiency and areas for improvement.

Code


# Access the crew's usage metrics
crew = Crew(agents=[agent1, agent2], tasks=[task1, task2])
crew.kickoff()
print(crew.usage_metrics)

Crew Execution Process

Sequential Process: Tasks are executed one after another, allowing for a linear flow of work.
Hierarchical Process: A manager agent coordinates the crew, delegating tasks and validating outcomes before proceeding. Note: A manager_llm or manager_agent is required for this process and it’s essential for validating the process flow.

Kicking Off a Crew

Once your crew is assembled, initiate the workflow with the kickoff() method. This starts the execution process according to the defined process flow.

Code


# Start the crew's task execution
result = my_crew.kickoff()
print(result)

Different Ways to Kick Off a Crew

Once your crew is assembled, initiate the workflow with the appropriate kickoff method. CrewAI provides several methods for better control over the kickoff process: kickoff(), kickoff_for_each(), kickoff_async(), and kickoff_for_each_async().

kickoff(): Starts the execution process according to the defined process flow.
kickoff_for_each(): Executes tasks sequentially for each provided input event or item in the collection.
kickoff_async(): Initiates the workflow asynchronously.
kickoff_for_each_async(): Executes tasks concurrently for each provided input event or item, leveraging asynchronous processing.
Code


# Start the crew's task execution
result = my_crew.kickoff()
print(result)

# Example of using kickoff_for_each
inputs_array = [{'topic': 'AI in healthcare'}, {'topic': 'AI in finance'}]
results = my_crew.kickoff_for_each(inputs=inputs_array)
for result in results:
    print(result)

# Example of using kickoff_async
inputs = {'topic': 'AI in healthcare'}
async_result = my_crew.kickoff_async(inputs=inputs)
print(async_result)

# Example of using kickoff_for_each_async
inputs_array = [{'topic': 'AI in healthcare'}, {'topic': 'AI in finance'}]
async_results = my_crew.kickoff_for_each_async(inputs=inputs_array)
for async_result in async_results:
    print(async_result)
These methods provide flexibility in how you manage and execute tasks within your crew, allowing for both synchronous and asynchronous workflows tailored to your needs.


Replaying from a Specific Task

You can now replay from a specific task using our CLI command replay.

The replay feature in CrewAI allows you to replay from a specific task using the command-line interface (CLI). By running the command crewai replay -t <task_id>, you can specify the task_id for the replay process.

Kickoffs will now save the latest kickoffs returned task outputs locally for you to be able to replay from.


Replaying from a Specific Task Using the CLI

To use the replay feature, follow these steps:

Open your terminal or command prompt.
Navigate to the directory where your CrewAI project is located.
Run the following command:
To view the latest kickoff task IDs, use:



crewai log-tasks-outputs
Then, to replay from a specific task, use:



crewai replay -t <task_id>
These commands let you replay from your latest kickoff tasks, still retaining context from previously executed tasks.


=== Memory
Memory
Leveraging memory systems in the CrewAI framework to enhance agent capabilities.

Introduction to Memory Systems in CrewAI

The crewAI framework introduces a sophisticated memory system designed to significantly enhance the capabilities of AI agents. This system comprises short-term memory, long-term memory, entity memory, and contextual memory, each serving a unique purpose in aiding agents to remember, reason, and learn from past interactions.


Memory System Components

Component   Description
Short-Term Memory   Temporarily stores recent interactions and outcomes using RAG, enabling agents to recall and utilize information relevant to their current context during the current executions.
Long-Term Memory    Preserves valuable insights and learnings from past executions, allowing agents to build and refine their knowledge over time.
Entity Memory   Captures and organizes information about entities (people, places, concepts) encountered during tasks, facilitating deeper understanding and relationship mapping. Uses RAG for storing entity information.
Contextual Memory   Maintains the context of interactions by combining ShortTermMemory, LongTermMemory, and EntityMemory, aiding in the coherence and relevance of agent responses over a sequence of tasks or a conversation.
User Memory Stores user-specific information and preferences, enhancing personalization and user experience.

How Memory Systems Empower Agents

Contextual Awareness: With short-term and contextual memory, agents gain the ability to maintain context over a conversation or task sequence, leading to more coherent and relevant responses.

Experience Accumulation: Long-term memory allows agents to accumulate experiences, learning from past actions to improve future decision-making and problem-solving.

Entity Understanding: By maintaining entity memory, agents can recognize and remember key entities, enhancing their ability to process and interact with complex information.


Implementing Memory in Your Crew

When configuring a crew, you can enable and customize each memory component to suit the crew’s objectives and the nature of tasks it will perform. By default, the memory system is disabled, and you can ensure it is active by setting memory=True in the crew configuration. The memory will use OpenAI embeddings by default, but you can change it by setting embedder to a different model. It’s also possible to initialize the memory instance with your own instance.

The ‘embedder’ only applies to Short-Term Memory which uses Chroma for RAG. The Long-Term Memory uses SQLite3 to store task results. Currently, there is no way to override these storage implementations. The data storage files are saved into a platform-specific location found using the appdirs package, and the name of the project can be overridden using the CREWAI_STORAGE_DIR environment variable.


Example: Configuring Memory for a Crew

Code


from crewai import Crew, Agent, Task, Process

# Assemble your crew with memory capabilities
my_crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.sequential,
    memory=True,
    verbose=True
)

Example: Use Custom Memory Instances e.g FAISS as the VectorDB

Code


from crewai import Crew, Process
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from typing import List, Optional

# Assemble your crew with memory capabilities
my_crew: Crew = Crew(
    agents = [...],
    tasks = [...],
    process = Process.sequential,
    memory = True,
    # Long-term memory for persistent storage across sessions
    long_term_memory = LongTermMemory(
        storage=LTMSQLiteStorage(
            db_path="/my_crew1/long_term_memory_storage.db"
        )
    ),
    # Short-term memory for current context using RAG
    short_term_memory = ShortTermMemory(
        storage = RAGStorage(
                embedder_config={
                    "provider": "openai",
                    "config": {
                        "model": 'text-embedding-3-small'
                    }
                },
                type="short_term",
                path="/my_crew1/"
            )
        ),
    ),
    # Entity memory for tracking key information about entities
    entity_memory = EntityMemory(
        storage=RAGStorage(
            embedder_config={
                "provider": "openai",
                "config": {
                    "model": 'text-embedding-3-small'
                }
            },
            type="short_term",
            path="/my_crew1/"
        )
    ),
    verbose=True,
)

Security Considerations

When configuring memory storage:

Use environment variables for storage paths (e.g., CREWAI_STORAGE_DIR)
Never hardcode sensitive information like database credentials
Consider access permissions for storage directories
Use relative paths when possible to maintain portability
Example using environment variables:



import os
from crewai import Crew
from crewai.memory import LongTermMemory
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage

# Configure storage path using environment variable
storage_path = os.getenv("CREWAI_STORAGE_DIR", "./storage")
crew = Crew(
    memory=True,
    long_term_memory=LongTermMemory(
        storage=LTMSQLiteStorage(
            db_path="{storage_path}/memory.db".format(storage_path=storage_path)
        )
    )
)

Configuration Examples


Basic Memory Configuration



from crewai import Crew
from crewai.memory import LongTermMemory

# Simple memory configuration
crew = Crew(memory=True)  # Uses default storage locations

Custom Storage Configuration



from crewai import Crew
from crewai.memory import LongTermMemory
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage

# Configure custom storage paths
crew = Crew(
    memory=True,
    long_term_memory=LongTermMemory(
        storage=LTMSQLiteStorage(db_path="./memory.db")
    )
)

Integrating Mem0 for Enhanced User Memory

Mem0 is a self-improving memory layer for LLM applications, enabling personalized AI experiences.

To include user-specific memory you can get your API key here and refer the docs for adding user preferences.

Code


import os
from crewai import Crew, Process
from mem0 import MemoryClient

# Set environment variables for Mem0
os.environ["MEM0_API_KEY"] = "m0-xx"

# Step 1: Record preferences based on past conversation or user input
client = MemoryClient()
messages = [
    {"role": "user", "content": "Hi there! I'm planning a vacation and could use some advice."},
    {"role": "assistant", "content": "Hello! I'd be happy to help with your vacation planning. What kind of destination do you prefer?"},
    {"role": "user", "content": "I am more of a beach person than a mountain person."},
    {"role": "assistant", "content": "That's interesting. Do you like hotels or Airbnb?"},
    {"role": "user", "content": "I like Airbnb more."},
]
client.add(messages, user_id="john")

# Step 2: Create a Crew with User Memory

crew = Crew(
    agents=[...],
    tasks=[...],
    verbose=True,
    process=Process.sequential,
    memory=True,
    memory_config={
        "provider": "mem0",
        "config": {"user_id": "john"},
    },
)

Memory Configuration Options

If you want to access a specific organization and project, you can set the org_id and project_id parameters in the memory configuration.

Code


from crewai import Crew

crew = Crew(
    agents=[...],
    tasks=[...],
    verbose=True,
    memory=True,
    memory_config={
        "provider": "mem0",
        "config": {"user_id": "john", "org_id": "my_org_id", "project_id": "my_project_id"},
    },
)

Additional Embedding Providers


Using OpenAI embeddings (already default)

Code


from crewai import Crew, Agent, Task, Process

my_crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.sequential,
    memory=True,
    verbose=True,
    embedder={
        "provider": "openai",
        "config": {
            "model": 'text-embedding-3-small'
        }
    }
)
Alternatively, you can directly pass the OpenAIEmbeddingFunction to the embedder parameter.

Example:

Code


from crewai import Crew, Agent, Task, Process
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

my_crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.sequential,
    memory=True,
    verbose=True,
    embedder={
        "provider": "openai",
        "config": {
            "model": 'text-embedding-3-small'
        }
    }
)

Using Ollama embeddings

Code


from crewai import Crew, Agent, Task, Process

my_crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.sequential,
    memory=True,
    verbose=True,
    embedder={
        "provider": "ollama",
        "config": {
            "model": "mxbai-embed-large"
        }
    }
)

Using Google AI embeddings


Prerequisites

Before using Google AI embeddings, ensure you have:

Access to the Gemini API
The necessary API keys and permissions
You will need to update your pyproject.toml dependencies:



dependencies = [
    "google-generativeai>=0.8.4", #main version in January/2025 - crewai v.0.100.0 and crewai-tools 0.33.0
    "crewai[tools]>=0.100.0,<1.0.0"
]
Code


from crewai import Crew, Agent, Task, Process

my_crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.sequential,
    memory=True,
    verbose=True,
    embedder={
        "provider": "google",
        "config": {
            "api_key": "<YOUR_API_KEY>",
            "model": "<model_name>"
        }
    }
)

Using Azure OpenAI embeddings

Code


from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from crewai import Crew, Agent, Task, Process

my_crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.sequential,
    memory=True,
    verbose=True,
    embedder={
        "provider": "openai",
        "config": {
            "api_key": "YOUR_API_KEY",
            "api_base": "YOUR_API_BASE_PATH",
            "api_version": "YOUR_API_VERSION",
            "model_name": 'text-embedding-3-small'
        }
    }
)

Using Vertex AI embeddings

Code


from chromadb.utils.embedding_functions import GoogleVertexEmbeddingFunction
from crewai import Crew, Agent, Task, Process

my_crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.sequential,
    memory=True,
    verbose=True,
    embedder={
        "provider": "vertexai",
        "config": {
            "project_id"="YOUR_PROJECT_ID",
            "region"="YOUR_REGION",
            "api_key"="YOUR_API_KEY",
            "model_name"="textembedding-gecko"
        }
    }
)

Using Cohere embeddings

Code


from crewai import Crew, Agent, Task, Process

my_crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.sequential,
    memory=True,
    verbose=True,
    embedder={
        "provider": "cohere",
        "config": {
            "api_key": "YOUR_API_KEY",
            "model": "<model_name>"
        }
    }
)

Using VoyageAI embeddings

Code


from crewai import Crew, Agent, Task, Process

my_crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.sequential,
    memory=True,
    verbose=True,
    embedder={
        "provider": "voyageai",
        "config": {
            "api_key": "YOUR_API_KEY",
            "model": "<model_name>"
        }
    }
)

Using HuggingFace embeddings

Code


from crewai import Crew, Agent, Task, Process

my_crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.sequential,
    memory=True,
    verbose=True,
    embedder={
        "provider": "huggingface",
        "config": {
            "api_url": "<api_url>",
        }
    }
)

Using Watson embeddings

Code


from crewai import Crew, Agent, Task, Process

# Note: Ensure you have installed and imported `ibm_watsonx_ai` for Watson embeddings to work.

my_crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.sequential,
    memory=True,
    verbose=True,
    embedder={
        "provider": "watson",
        "config": {
            "model": "<model_name>",
            "api_url": "<api_url>",
            "api_key": "<YOUR_API_KEY>",
            "project_id": "<YOUR_PROJECT_ID>",
        }
    }
)

Using Amazon Bedrock embeddings

Code


# Note: Ensure you have installed `boto3` for Bedrock embeddings to work.

import os
import boto3
from crewai import Crew, Agent, Task, Process

boto3_session = boto3.Session(
    region_name=os.environ.get("AWS_REGION_NAME"),
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
)

my_crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.sequential,
    memory=True,
    embedder={
    "provider": "bedrock",
        "config":{
            "session": boto3_session,
            "model": "amazon.titan-embed-text-v2:0",
            "vector_dimension": 1024
        }
    }
    verbose=True
)

Adding Custom Embedding Function

Code


from crewai import Crew, Agent, Task, Process
from chromadb import Documents, EmbeddingFunction, Embeddings

# Create a custom embedding function
class CustomEmbedder(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        # generate embeddings
        return [1, 2, 3] # this is a dummy embedding

my_crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.sequential,
    memory=True,
    verbose=True,
    embedder={
        "provider": "custom",
        "config": {
            "embedder": CustomEmbedder()
        }
    }
)

Resetting Memory via cli



crewai reset-memories [OPTIONS]

Resetting Memory Options

Option  Description Type    Default
-l, --long  Reset LONG TERM memory. Flag (boolean)  False
-s, --short Reset SHORT TERM memory.    Flag (boolean)  False
-e, --entities  Reset ENTITIES memory.  Flag (boolean)  False
-k, --kickoff-outputs   Reset LATEST KICKOFF TASK OUTPUTS.  Flag (boolean)  False
-kn, --knowledge    Reset KNOWLEDEGE storage    Flag (boolean)  False
-a, --all   Reset ALL memories. Flag (boolean)  False
Note: To use the cli command you need to have your crew in a file called crew.py in the same directory.


Resetting Memory via crew object




my_crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.sequential,
    memory=True,
    verbose=True,
    embedder={
        "provider": "custom",
        "config": {
            "embedder": CustomEmbedder()
        }
    }
)

my_crew.reset_memories(command_type = 'all') # Resets all the memory

Resetting Memory Options

Command Type    Description
long    Reset LONG TERM memory.
short   Reset SHORT TERM memory.
entities    Reset ENTITIES memory.
kickoff_outputs Reset LATEST KICKOFF TASK OUTPUTS.
knowledge   Reset KNOWLEDGE memory.
all Reset ALL memories.

Benefits of Using CrewAI’s Memory System

🦾 Adaptive Learning: Crews become more efficient over time, adapting to new information and refining their approach to tasks.
🫡 Enhanced Personalization: Memory enables agents to remember user preferences and historical interactions, leading to personalized experiences.
🧠 Improved Problem Solving: Access to a rich memory store aids agents in making more informed decisions, drawing on past learnings and contextual insights.

Conclusion

Integrating CrewAI’s memory system into your projects is straightforward. By leveraging the provided memory components and configurations, you can quickly empower your agents with the ability to remember, reason, and learn from their interactions, unlocking new levels of intelligence and capability.

