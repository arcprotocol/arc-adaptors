# LangChain Adaptor for ARC Protocol

This module provides integration between the ARC Protocol and LangChain, enabling LangChain agents to communicate with ARC Protocol agents through handoff tools.

## Features

- Create handoff tools for ARC Protocol agents
- Retrieve agent information from ARC Ledger
- Convert between LangChain and ARC Protocol message formats
- Support for "last_message" mode in handoffs
- Integration with LangChain agents and workflows

## Usage

### Basic Usage

```python
from arc_adaptors.langchain import ARCLangChainAdaptor

# Create the adaptor
adaptor = ARCLangChainAdaptor(
    arc_endpoint="https://api.example.com/arc",
    ledger_url="https://ledger.example.com/arc",
    agent_ids=["math-agent", "weather-agent", "news-agent"]
)

# Load the handoff tools
tools = await adaptor.load_tools()

# Create a LangChain agent with the handoff tools
llm = ChatOpenAI(model="gpt-4")
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# Run the agent
result = await agent_executor.ainvoke({"input": "What's the weather like in New York?"})
```

### Supervisor Agent

```python
from arc_adaptors.langchain import ARCLangChainAdaptor

# Create the adaptor
adaptor = ARCLangChainAdaptor(
    arc_endpoint="https://api.example.com/arc",
    ledger_url="https://ledger.example.com/arc",
    agent_ids=["math-agent", "weather-agent", "news-agent"]
)

# Create a supervisor agent
class SupervisorAgent:
    def __init__(self, adaptor):
        self.adaptor = adaptor
        self.tools = []
        
    async def initialize(self):
        self.tools = await self.adaptor.load_tools()
        # Create LangChain agent with tools...
        
    async def process_request(self, user_input):
        # Process user request and delegate to specialized agents...
        pass

# Use the supervisor agent
supervisor = SupervisorAgent(adaptor)
await supervisor.initialize()
response = await supervisor.process_request("What's the weather like in New York?")
```

## Handoff Mechanism

The handoff mechanism allows a LangChain agent to delegate tasks to specialized ARC Protocol agents. When a handoff occurs:

1. The LangChain agent calls a handoff tool (e.g., `transfer_to_math_expert`)
2. The handoff tool creates a task with the target ARC agent
3. The task includes the last message from the conversation
4. The ARC agent processes the task and returns a response
5. The response is converted back to LangChain format and returned to the agent

## Agent Information

Agent information is retrieved from the ARC Ledger and includes:

- `id`: Agent ID used for ARC Protocol communication
- `name`: Human-readable name of the agent
- `url`: ARC endpoint URL for the agent
- `description`: Description of the agent's capabilities

## Output Modes

The adaptor supports different output modes for handoffs:

- `last_message`: Only the last message is passed to the sub-agent (default)
- `full_history`: The entire conversation history is passed to the sub-agent

## Error Handling

The adaptor includes error handling for common scenarios:

- Agent not found
- Communication errors
- Timeout waiting for task completion
- Invalid responses
