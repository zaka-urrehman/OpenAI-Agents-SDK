import os 
import asyncio
from agents import (Agent,
                    Runner,
                    AsyncOpenAI,
                    ItemHelpers,
                    enable_verbose_stdout_logging,
                    set_tracing_disabled,
                    set_default_openai_api,
                    set_default_openai_client,
                    OpenAIChatCompletionsModel
                    )
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    print("GEMINI_API_KEY is not set.")

set_tracing_disabled(True)
enable_verbose_stdout_logging()

external_client = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)


# Agents as tools
spanish_agent = Agent(
    name="Spanish Agent",
    instructions="You are a helpful assistant that can translate English to Spanish.",
    handoff_description="an expert in Spanish language which translates English to Spanish.",
    model=model
)

italian_agent = Agent(
    name="Italian Agent",
    instructions="You are a helpful assistant that can translate English to Italian.",
    handoff_description="an expert in Italian language which translates English to Italian.",
    model=model
)

french_agent = Agent(
    name="French Agent",
    instructions="You are a helpful assistant that can translate English to French.",
    handoff_description="an expert in French language which translates English to French.",
    model=model
)


# Orchestrator Agent (the main agent)
orchestrator_agent = Agent(
    name="Orchestrator Agent",
    instructions="""
        You are a translation orchestrator with three tools:

        • translate_to_spanish(input: str) → returns Spanish  
        • translate_to_italian(input: str) → returns Italian  
        • translate_to_french(input: str) → returns French  

        When the user asks for translations into multiple languages, follow this exact **step-by-step** process:

        1. Parse the user’s request and build a list of the languages they want (e.g. [Spanish, French]).  
        2. **For each** language in that list, **in sequence**:
        - Emit **exactly one** function call to the corresponding tool     
        - Wait for the tool to return its translation.
        3. After you’ve gathered all individual translations, send a final plain-text message that lists each result, like:
        - Spanish: …  
        - French: …  

        If the user only asks for a single language, call that tool once and then reply.  
        If the user’s question isn’t about translating text, answer normally without calling any tool.
    """,
    model=model,
    tools=[
      spanish_agent.as_tool("translate_to_spanish", "Translate English to Spanish."),
      italian_agent.as_tool("translate_to_italian", "Translate English to Italian."),
      french_agent.as_tool("translate_to_french", "Translate English to French."),
    ]
)



async def main():
    result =  Runner.run_streamed(orchestrator_agent, "Translate 'Hello, how are you?' to Spanish and frensh")

    async for event in result.stream_events():
        if event.type == "raw_response_event":
            continue
        elif event.type == "agent_updated_stream_event":
            print(f"Agent Updated: {event.new_agent.name}")
            continue
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"-- Message Output: \n {ItemHelpers.text_message_output(event.item)}")
            else:
                pass

    

if __name__ == "__main__":
    asyncio.run(main())