import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import asyncio

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)



urdu_agent = Agent(
    name="Urdu Agent",
    instructions="You are a helpful assistant that can answer questions in Urdu.",
    model=model
)

arabic_agent = Agent(
    name="Arabic Agent",
    instructions="You are a helpful assistant that can answer questions in Arabic.",
    model=model
)

async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant that greets users when they say hello. You can also handoff to the Urdu Agent or the Arabic Agent to answer questions in Urdu or Arabic.",
        model=model,
        handoffs=[urdu_agent, arabic_agent]
    )

    result = await Runner.run(agent, "Salam. kya hal hy?", run_config=config)
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())