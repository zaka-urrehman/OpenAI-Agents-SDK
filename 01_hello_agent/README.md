# OpenAI Agents SDK with Gemini API - step 1
Since the OpenAI API key is paid, this example uses Gemini API key to integrate with the framework, creating an agent. 

## Features
- Async agent with `asyncio`. 
- Gemini API integration. 

## Setup

1. **Initialize** `uv` project:
   ```bash
   uv init openai_agents_example
   cd openai_agents_example
   ```

2. **Install dependencies**:
   ```bash
   uv add openai-agents python-dotenv
   ```

3. **Create** a `.env` file 

4. **Add Gemini API key**:
   ```env
   GEMINI_API_KEY=your-gemini-key-here
   ```

## Usage
In the main.py: 

1. **Import necessary stuff**:
   ```python
   import os
   from dotenv import load_dotenv
   from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
   from agents.run import RunConfig
   import asyncio
   ```

2. **Load API key**
   ```python
   load_dotenv()
   gemini_api_key = os.getenv("GEMINI_API_KEY")
   
   if not gemini_api_key:
       raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")
   ```

3. **Create external client**:
   ```python
   #Reference: https://ai.google.com/dev/ai/grok-api/docs/openai/agents-api
   external_client = AsyncOpenAI(
       api_key=gemini_api_key,
       base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
   )
   ```
   Sets up an OpenAI-compatible client for Gemini API. This step is not included if you are using OpenAI key. 

4. **Create a config**:
   ```python
   model = OpenAIChatCompletionsModel(
       model="gemini-2.0-flash",
       openai_client=external_client
   )
   
   config = RunConfig(
       model=model,
       model_provider=external_client,
       tracing_disabled=True
   )
   ```
   Configures the Gemini model and run settings.

5. **Define an async function to create and run Agent**:
   ```python
   async def main():
       agent = Agent(
           name="Assistant",
           instructions="You are a helpful assistant that greets users when they say hello.",
           model=model
       )
   
       result = await Runner.run(agent, "Hello how are you?", run_config=config)
       print(result.final_output)
   ```
   Creates an async agent, queries it, and prints the response.

6. **Run using `asyncio`**
   ```python
   if __name__ == "__main__":
       asyncio.run(main())
    ```

    asyncio is used because the `Runner.run` runs the agent asynchronously by default. so we have to await it and wrap in an async function. 


## Final Output
Run the following command to see the output of your agent:
```bash
uv run python main.py
```

## Next Steps

- Model configuration
- See how streaming works. 
- Add tools 
- Try other queries or models.
- See [OpenAI Agents SDK](http://openai.github.io/openai-agents-python/) and [Gemini API](https://ai.google.com/dev/ai/grok-api/docs/openai) docs.

