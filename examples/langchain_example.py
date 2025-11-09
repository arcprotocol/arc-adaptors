#!/usr/bin/env python3
"""
Example of using the ARCLangChainAdaptor to integrate ARC Protocol with LangChain.
"""

import asyncio
import os
from typing import List

from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from arc_adaptors.langchain import ARCLangChainAdaptor


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
    
    # Load the handoff tools
    tools: List[BaseTool] = await adaptor.load_tools()
    
    # Print the available tools
    print(f"Loaded {len(tools)} handoff tools:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")
    
    # Create a LangChain agent with the handoff tools
    llm = ChatOpenAI(model="gpt-4")
    
    # Create a prompt that includes instructions for using handoff tools
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful assistant that can delegate tasks to specialized agents.
        When you need help with a specific task, use the appropriate handoff tool to transfer the request.
        Only use the handoff tools when necessary for specialized knowledge or capabilities."""),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Create the agent
    agent = create_react_agent(llm, tools, prompt)
    
    # Create the agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
    )
    
    # Run the agent with a sample query
    result = await agent_executor.ainvoke(
        {"input": "What's the weather like in New York and can you also solve 25 * 16?"}
    )
    
    print("\nAgent response:")
    print(result["output"])
    
    # Close the adaptor
    await adaptor.close()


if __name__ == "__main__":
    asyncio.run(main())
