import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType

# Add the tools directory to the Python path
sys.path.append(str(Path(__file__).parent))
from tools.project_scanner import project_scanner_tool

# Load environment variables
load_dotenv()

class AgenticAssistant:
    def __init__(self):
        """
        Initialize the Agentic Assistant with a language model and tools.
        """
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",  # Using gemini-2.5-flash for consistency with prompted_model.py
            google_api_key=os.getenv("API_KEY"),
            convert_system_message_to_human=True,
            temperature=0.7
        )
        
        # Initialize tools
        self.tools = [project_scanner_tool]
        
        # Initialize agent
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True
        )
    
    def run(self, query: str) -> str:
        """
        Execute a query using the agentic assistant.
        
        Args:
            query (str): The user's query or instruction
            
        Returns:
            str: The agent's response
        """
        try:
            response = self.agent.run(query)
            return response
        except Exception as e:
            return f"An error occurred: {str(e)}"

# Example usage
if __name__ == "__main__":
    assistant = AgenticAssistant()
    
    # Example query - this would be replaced with user input in a real application
    example_query = r"Scan my project folder at 'C:\Users\user\vscode\summer\learn\09_ai' and summarize the README files."
    
    print("Agentic Assistant - Type 'exit' to quit")
    print("Example query:", example_query)
    print("\n" + "="*50 + "\n")
    
    while True:
        user_input = input("\nYour query: ")
        if user_input.lower() == 'exit':
            break
            
        response = assistant.run(user_input)
        print("\nResponse:")
        print(response)
