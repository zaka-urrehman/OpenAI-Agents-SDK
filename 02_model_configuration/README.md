# Model Configuration in OpenAI Agents SDK

In the OpenAI Agents SDK, you can configure the model used by your agents in three distinct ways: the Global method, the Agent method, and the Run method. This flexibility allows you to tailor model usage to your application's requirements. Since the OpenAI API key is paid, this guide demonstrates how to integrate the Gemini API key for each method.

**Note:** Ensure you have the `openai-agents` and `python-dotenv` packages installed. Set your Gemini API key in a `.env` file as `GEMINI_API_KEY`.

## 1. Global Method

The Global method involves setting a default client for the entire application using `set_default_openai_client`. This client is used to resolve model names across all agents unless overridden, making it ideal when you want all agents to default to the same provider, such as Gemini.

**Example:**
    ```python
    import os
    from dotenv import load_dotenv
    from agents import Agent, Runner, AsyncOpenAI, set_tracing_disabled, set_default_openai_api, set_default_openai_client
    import asyncio

    # Load the Gemini API key
    load_dotenv()
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not set.")

    # Set up the Gemini client
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    # Set the default client globally
    set_default_openai_client(external_client)
    set_tracing_disabled(True)
    set_default_openai_api("chat_completions")

    # Create the agent with a model name
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
        model="gemini-2.0-flash"  
    )

    async def main():
        result = await Runner.run(agent, "Tell me about recursion.")
        print(result.final_output)

    if __name__ == "__main__":
        asyncio.run(main())
    ```

In this example, setting the default client to Gemini allows the SDK to use the Gemini API for the specified model name.

## 2. Agent Method

The Agent method lets you specify the model when creating an agent by passing a model instance. This is useful when you want a specific agent to consistently use a particular model, such as Gemini's "gemini-2.0-flash".

**Example:**
    ```python
    import os
    import asyncio
    from dotenv import load_dotenv
    from agents import Agent, OpenAIChatCompletionsModel, Runner, RunConfig, AsyncOpenAI
    # Load the Gemini API key
    load_dotenv()
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not set.")

    # Set up the Gemini client
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    # Create the model instance
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    # Create the agent with the specified model
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
        model=model
    )

    async def main():
        result = await Runner.run(agent, "Tell me about recursion.")
        print(result.final_output)

    if __name__ == "__main__":
        asyncio.run(main())
    ```

Here, the agent is configured with a model instance tied to the Gemini API, ensuring it uses that model for all operations.

## 3. Run Method

The Run method allows you to set the model for a specific execution of an agent by passing it in the `RunConfig` when calling `Runner.run`. This method is perfect for scenarios where you need to use different models for different runs of the same or different agents.

**Example:**
    ```python
    import os
    from dotenv import load_dotenv
    from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig, AsyncOpenAI
    import asyncio

    # Load the Gemini API key
    load_dotenv()
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not set.")

    # Set up the Gemini client
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    # Create the model instance
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    # Create the agent without a model
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant that responds in haiku."
    )

    # Define the RunConfig with the Gemini model
    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )

    async def main():
        result = await Runner.run(agent, "Tell me about recursion.", run_config=config) # pass the config here
        print(result.final_output)

    if __name__ == "__main__":
        asyncio.run(main())
    ```

In this case, the model is specified at runtime, allowing flexibility to switch models (e.g., between Gemini models) for different tasks.

---

These three methods—Global, Agent, and Run—provide versatile options for configuring models in the OpenAI Agents SDK with the Gemini API key, catering to both broad and specific use cases.