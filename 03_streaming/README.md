# Streaming in OpenAI Agents SDK

This example demonstrates streaming AI responses using the OpenAI Agents SDK, showcasing how to process real-time output.

## Streaming Concept

Streaming in the OpenAI Agents SDK, enabled by `Runner.run_streamed`, delivers AI responses incrementally as events (e.g., `message_output_item`, `tool_call_item`). The code processes these events asynchronously, printing message outputs or tool interactions as they arrive, rather than waiting for the full response.

## Why Streaming Improves UX

Streaming enhances user experience by:
- **Reducing Wait Time**: Users see partial responses immediately, making the interaction feel faster and more responsive.
- **Real-Time Feedback**: Incremental updates keep users engaged, especially for lengthy responses.
- **Dynamic Interaction**: Supports live tool calls or agent updates, enabling interactive and fluid applications.

