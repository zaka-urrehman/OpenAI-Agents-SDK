# Tracing

The Agents SDK includes built-in tracing, collecting a comprehensive record of events during an agent run: LLM generations, tool calls, handoffs, guardrails, and even custom events that occur. Tracing provides a detailed view of an agent's workflow, enabling developers to debug, monitor, and optimize their agent's performance. Traces can be visualized in the OpenAI Traces dashboard or sent to alternative destinations using custom trace processors.

## Understanding Traces and Spans

### What is a Trace?
A **trace** is a complete record of an agent's workflow during a single execution, initiated by calling `agent.run()`. It captures the entire sequence of operations from start to finish, including all significant events that occur. Each trace is represented as a timeline that contains one or more spans, providing a structured overview of the agent's activities.

### What is a Span?
A **span** is an individual unit of work or event within a trace. It represents a specific action the agent performs, such as:
- **LLM Generation**: When the agent uses a language model to process input or generate output (e.g., parsing a user request or creating a response).
- **Tool Call**: When the agent interacts with an external tool (e.g., calling a flight search API).
- **Guardrail**: When the agent applies a check or constraint (e.g., verifying a budget limit).
- **Handoff**: When the agent transfers control to another agent or system.
- **Custom Event**: Any user-defined event logged during the run.

Each span includes:
- **Start and End Time**: To measure the duration of the event.
- **Metadata**: Details such as inputs, outputs, prompts, or results specific to the event.
- **Optional Tags**: Additional context for categorization or analysis.

Spans can be nested, allowing for a hierarchical view of the workflow. For example, a tool call span might be a child of the root span for the entire agent run.

### Example Scenario
Consider an agent tasked with booking a flight based on the request: "Book a flight from New York to London on June 1st for under $500." The trace for this task might include the following spans:

- **Root Span**: Represents the entire `agent.run()` process.
  - **Metadata**: Includes the user request and final output.
- **Span 1: LLM Generation (Parse Request)**: Extracts details like origin, destination, date, and budget.
  - **Metadata**: Prompt and extracted details (e.g., `{ "origin": "New York", "destination": "London", "date": "June 1st", "budget": "$500" }`).
- **Span 2: Tool Call (Search Flights)**: Calls a flight search tool.
  - **Metadata**: Tool name, input parameters, and results (e.g., list of available flights).
- **Span 3: LLM Generation (Select Flight)**: Chooses a flight under $500.
  - **Metadata**: Prompt and selected flight details (e.g., `{ "flight_id": "F123", "price": "$450" }`).
- **Span 4: Guardrail (Check Budget)**: Verifies the flight price is within budget.
  - **Metadata**: Condition, input, and outcome (e.g., "Pass" if price < $500).
- **Span 5: Tool Call (Book Flight)**: Reserves the selected flight.
  - **Metadata**: Tool name, input, and confirmation details (e.g., `{ "confirmation_number": "ABC123" }`).
- **Span 6: LLM Generation (Confirmation Message)**: Creates a user-friendly confirmation.
  - **Metadata**: Prompt and generated message (e.g., "Your flight is booked...").

This trace provides a clear timeline of events, with each span documenting a specific action, its inputs, outputs, and duration.

## Disabling Tracing
Tracing is enabled by default in the SDK. There are two ways to disable it:

1. **Globally Disable Tracing**: Set the environment variable `OPENAI_AGENTS_DISABLE_TRACING=1`. This prevents tracing for all agent runs, ensuring no trace data is sent to OpenAI's backend.
2. **Disable Tracing for a Single Run**: Set `agents.run.RunConfig.tracing_disabled` to `True` for a specific run. This allows you to disable tracing selectively without affecting other runs.

## Customizing Tracing
If you need to comply with a Zero Data Retention (ZDR) policy or prefer to store traces elsewhere, you can customize tracing using custom trace processors. By configuring `add_trace_processor()` or `set_trace_processors()`, you can redirect trace data to alternative destinations, such as a local server or third-party tools like Logfire or Braintrust. This ensures compliance with privacy requirements while maintaining the ability to monitor and debug workflows.

## Why Use Tracing?
Tracing is invaluable for:
- **Debugging**: Identify where and why an agent fails or behaves unexpectedly.
- **Performance Monitoring**: Analyze the duration and efficiency of each step in the workflow.
- **Optimization**: Understand how the agent processes tasks to improve its design or reduce costs.
- **Compliance and Auditing**: Maintain a record of actions for accountability (when using custom processors).

For more details, refer to the [OpenAI Agents SDK Tracing Documentation](https://openai.github.io/openai-agents-python/tracing/).