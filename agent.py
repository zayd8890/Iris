from calculator import CalculatorTool
from smolagents import CodeAgent, LiteLLMModel
import contextlib
import io

class AgentManager:
    def __init__(self, model_id="deepseek/deepseek-chat", temperature=0.7,
                 api_key='', tools=None,
                 verbose=False):
        """
        :param verbose: Set True to show detailed processing, False for only final answer
        """
        self.model = LiteLLMModel(
            model_id=model_id,
            temperature=temperature,
            api_key=api_key
        )
        self.tools = tools or [CalculatorTool()]
        self.verbose = verbose
        self.agent = CodeAgent(tools=self.tools, model=self.model)

    def run_query(self, prompt):
        """Run the query and return only the final result"""
        if self.verbose:
            return self.agent.run(prompt)
        
        # Suppress all stdout during execution
        with contextlib.redirect_stdout(io.StringIO()):
            result = self.agent.run(prompt)
            
        return result