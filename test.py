from agent import AgentManager

# Create agent with verbose output disabled (default)
quiet_agent = AgentManager(verbose=False)

# This will only print the final answer
result = quiet_agent.run_query("What's 5+3")
print("Final Answer:", result)

# For debugging purposes, you can enable verbose output
debug_agent = AgentManager(verbose=True)
debug_result = debug_agent.run_query("What's 5+3")  # Will show all intermediate steps