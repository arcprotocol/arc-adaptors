#!/usr/bin/env python3
"""
Example of using the ARCLangChainAdaptor with a supervisor agent that delegates to specialized agents.
"""

import asyncio
import os
from typing import Dict, List, Any

from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from arc_adaptors.langchain import ARCLangChainAdaptor


class SupervisorAgent:
    """
    A supervisor agent that delegates tasks to specialized agents.
    """
    
    def __init__(
        self,
        adaptor: ARCLangChainAdaptor,
        model_name: str = "gpt-4",
        output_mode: str = "last_message"
    ):
        """
        Initialize the supervisor agent.
        
        Args:
            adaptor: ARCLangChainAdaptor for communication with ARC agents
            model_name: Name of the LLM model to use
            output_mode: Output mode for handoffs ("last_message" or "full_history")
        """
        self.adaptor = adaptor
        self.model_name = model_name
        self.output_mode = output_mode
        self.tools: List[BaseTool] = []
        self.agent_executor = None
        self.chat_history = []
    
    async def initialize(self):
        """Initialize the supervisor agent with handoff tools."""
        # Load the handoff tools
        self.tools = await self.adaptor.load_tools()
        
        # Create the LLM
        llm = ChatOpenAI(model=self.model_name)
        
        # Create a prompt that includes instructions for using handoff tools
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a supervisor agent that delegates tasks to specialized agents.
            When you receive a request that requires specialized knowledge or capabilities,
            use the appropriate handoff tool to transfer the request to a specialized agent.
            
            Always analyze the request carefully to determine which agent is best suited to handle it.
            Only use handoff tools when necessary - if you can answer directly, do so.
            
            Available specialized agents:
            {agent_descriptions}
            """),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create the agent
        agent = create_react_agent(llm, self.tools, prompt)
        
        # Create the agent executor
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
        )
    
    def _get_agent_descriptions(self) -> str:
        """Get descriptions of available specialized agents."""
        descriptions = []
        for tool in self.tools:
            descriptions.append(f"- {tool.name}: {tool.description}")
        return "\n".join(descriptions)
    
    def _process_output(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the output based on the output mode.
        
        Args:
            output: Output from the agent executor
            
        Returns:
            Processed output
        """
        messages = output.get("messages", [])
        
        if self.output_mode == "last_message":
            # Keep only the last message
            if messages:
                messages = [messages[-1]]
        
        return {
            **output,
            "messages": messages
        }
    
    async def process_request(self, user_input: str) -> str:
        """
        Process a user request.
        
        Args:
            user_input: User input text
            
        Returns:
            Response from the supervisor agent or specialized agent
        """
        if not self.agent_executor:
            await self.initialize()
        
        # Add user message to chat history
        self.chat_history.append(HumanMessage(content=user_input))
        
        # Prepare input for the agent executor
        input_data = {
            "input": user_input,
            "chat_history": self.chat_history[:-1],  # Exclude the latest message
            "agent_descriptions": self._get_agent_descriptions()
        }
        
        # Run the agent executor
        result = await self.agent_executor.ainvoke(input_data)
        
        # Process the output
        output = self._process_output(result)
        
        # Add agent response to chat history
        agent_message = output.get("output", "")
        self.chat_history.append(AIMessage(content=agent_message))
        
        return agent_message


async def main():
    """Run the example."""
    # Set up ARC adaptor
    arc_endpoint = "https://api.example.com/arc"  # Replace with your ARC endpoint
    ledger_url = "https://ledger.example.com/arc"  # Replace with your ARC Ledger URL
    agent_ids = ["math-agent", "weather-agent", "news-agent"]  # Replace with your agent IDs
    
    # Create the adaptor
    adaptor = ARCLangChainAdaptor(
        arc_endpoint=arc_endpoint,
        ledger_url=ledger_url,
        agent_ids=agent_ids
    )
    
    # Create the supervisor agent
    supervisor = SupervisorAgent(adaptor, output_mode="last_message")
    
    # Process a sample request
    user_input = "I need to know the weather in New York and also calculate 25 * 16"
    print(f"User: {user_input}")
    
    response = await supervisor.process_request(user_input)
    print(f"Agent: {response}")
    
    # Process a follow-up request
    user_input = "Now I need the latest news about technology"
    print(f"User: {user_input}")
    
    response = await supervisor.process_request(user_input)
    print(f"Agent: {response}")
    
    # Close the adaptor
    await adaptor.close()


if __name__ == "__main__":
    asyncio.run(main())
