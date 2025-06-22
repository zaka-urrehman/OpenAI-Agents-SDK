# Tools and Tool Calls in OpenAI Agents SDK

LLMs are stateless, meaning they rely solely on their training data and lack persistent context or external capabilities. To give agents extra powers, such as querying APIs, executing code, or retrieving data, you can define custom Python functions as tools. Tool calls enable agents to dynamically invoke these functions based on user input or task requirements, significantly enhancing their functionality. 

OpenAI Agents SDK provides three types of tools:

1. **Hosted Tools**:
   These are prebuilt tools running on OpenAI's server accessible via `OpenAIResponsesModel`. These tools include:
   - WebSearchTool
   - FileSearchTool
   - ComputerTool
   - CodeInterpreterTool
   - HostedMCPTool
   - ImageGenerationTool
   - LocalShellTool

2. **Function Calling**:
   These are python functions that are used as tools. Any python function when decorated with `@function_tool()` can be passed as tool to the Agent. 

3. **Agent As Tools**: 
   Agents can have other agents as tools, which give an agent the ability to use other agent for a particular task without transfering full control to the other agent. 