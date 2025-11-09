# ARC Adaptors

[![PyPI version](https://badge.fury.io/py/arc-adaptors.svg)](https://badge.fury.io/py/arc-adaptors)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Downloads](https://pepy.tech/badge/arc-adaptors)](https://pepy.tech/project/arc-adaptors)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Adaptors that connect AI frameworks to the ARC Protocol, enabling direct communication between different agent systems.

## Overview

ARC Adaptors solves the practical problem of connecting different AI frameworks through the ARC Protocol. It lets you:

- **Convert existing agents into supervisors**: Any LLM with tool-calling can delegate tasks to specialized agents
- **Bridge incompatible systems**: Connect LangChain, LlamaIndex, and API-based agents without custom code
- **Implement handoffs with minimal overhead**: Delegate tasks through standard tool interfaces

Currently supports:

- LangChain
- LlamaIndex
- OpenAI API
- Anthropic API
- Mistral AI

## Installation

```bash
# Full installation
pip install arc-adaptors

# Specific adaptor only
pip install arc-adaptors[langchain]
pip install arc-adaptors[openai]
pip install arc-adaptors[anthropic]
pip install arc-adaptors[mistral]
pip install arc-adaptors[llama-index]
```

## Usage

### LangChain Adaptor

```python
from arc_adaptors.langchain import ARCLangChainAdaptor

# Create adaptor
adaptor = ARCLangChainAdaptor(
    arc_endpoint="https://api.example.com/arc",
    ledger_url="https://ledger.example.com",
    agent_ids=["math-agent", "weather-agent"]
)

# Load handoff tools
tools = await adaptor.load_tools()

# Use with LangChain
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()
agent = create_react_agent(llm, tools, prompt)
result = await agent.ainvoke({"input": "What's 25 * 16?"})
```

## Supervisor Agent Capabilities

ARC Adaptors transforms standard agents into supervisors without additional dependencies. The adaptor:

1. **Exposes specialized agents as tools**: Converts ARC agents into framework-specific tools (e.g., LangChain tools)
2. **Translates between protocols**: Handles all message format conversions between frameworks and ARC
3. **Routes messages correctly**: Ensures the right context is passed between agents

This approach eliminates the need for specialized orchestration frameworks. Any LLM that can use tools becomes a potential supervisor that can coordinate specialized agents.

## Adaptors

| Name | Description | Status | Package |
|------|-------------|--------|---------|
| LangChain | Creates handoff tools for LangChain agents | ✅ Ready | `arc-adaptors[langchain]` |
| OpenAI | Connects OpenAI API with ARC Protocol | 🚧 Under development | `arc-adaptors[openai]` |
| Anthropic | Connects Anthropic API with ARC Protocol | 🚧 Under development | `arc-adaptors[anthropic]` |
| Mistral | Connects Mistral AI with ARC Protocol | 🚧 Under development | `arc-adaptors[mistral]` |
| LlamaIndex | Connects LlamaIndex with ARC Protocol | 🚧 Under development | `arc-adaptors[llama-index]` |

## License

Apache License 2.0