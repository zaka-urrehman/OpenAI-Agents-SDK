# OpenAI Agents SDK
The **OpenAI Agents SDK** is a lightweight and powerful framework for developing AI Agents and Multi-Agent systems. It supports both the "Chat Completions" and "Responses" API from OpenAI. It works with alot of diffenent LLMs such as Gemini, Claude, Llama etc. 

## Key Features
The OpenAI Agents SDK is built with a small set of core primitives that provides maximum flexibility and control while keeping things very simple. These features include:

### Agents 
**Agents** are the heart of the SDK. An Agent is a LLM configured with:
- **Intructions**: A set of guidelines or "system prompt" that defines the behavior of Agent
- **Tools**: Capabilities that allow agent to perform actions such as fetching data, running code or interacting with external APIs

### Handoffs
**Handoffs** allow agents to delegate task to other agents. This feature is useful for breaking down complex workflows into smaller and manageable parts. 

### Guardrails
**Guardrails** are safety mechanisms that validates inputs and outputs to ensure they meet some specific criteria. They can stop the workflow if invalid inputs are detected. Guardrails are essential for maintaining the reliability and security of your AI applications, especially in production environments.

### Tracing
**Tracing** is a built-in feature which allows you to visualize and debug your agent workflows. It provides detailed insights into how agents interact, which tools are being used, and where potential bottlenecks or errors occur.

### Function Tools
***Function Tools** enable you to turn any Python function into a tool that agents can use. The SDK automatically generates the necessary schema and validation for these functions, making it easy to integrate custom functionality. This feature is powerful for extending the capabilities of your agents with minimal effort. 
