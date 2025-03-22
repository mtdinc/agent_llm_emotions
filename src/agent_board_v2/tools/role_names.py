"""
Helper module for getting the correct role names for delegation in the CrewAI hierarchical process.
"""

# Role names from agents.yaml
ROLE_NAMES = {
    "senior_internist": "Chief Internist",
    "internist_one": "Primary Diagnostician",
    "internist_two": "Diagnostic Reviewer"
}

def get_role_name(agent_method_name):
    """
    Convert an agent method name to its corresponding role name.
    
    Args:
        agent_method_name: The method name of the agent (e.g., 'internist_one')
        
    Returns:
        The corresponding role name from agents.yaml
    """
    return ROLE_NAMES.get(agent_method_name, "Unknown agent")

# Example usage:
# from agent_board_v2.tools.role_names import get_role_name
# primary_diagnostician_role = get_role_name("internist_one")
# diagnostic_reviewer_role = get_role_name("internist_two")
