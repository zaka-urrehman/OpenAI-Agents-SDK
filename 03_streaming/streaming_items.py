import asyncio
import os
from agents import Agent, Runner, AsyncOpenAI,ItemHelpers, set_tracing_disabled, set_default_openai_api, set_default_openai_client, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key, 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
  )

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client = external_client
)

set_default_openai_client(external_client)
set_tracing_disabled(True)
set_default_openai_api("chat_completions")


async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant",
        model=model
    )

    result = Runner.run_streamed(agent, input="Explain the capital of Pakistan in 20 lines.")

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