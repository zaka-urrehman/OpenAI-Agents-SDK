import os
import asyncio
from pydantic import BaseModel
from dotenv import load_dotenv
from agents import (Agent,
                    Runner, 
                    AsyncOpenAI, 
                    OpenAIChatCompletionsModel, 
                    input_guardrail, 
                    RunContextWrapper, 
                    TResponseInputItem, 
                    GuardrailFunctionOutput, 
                    function_tool
                    )
from agents.run import RunConfig

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


class WeatherInputGuardrail(BaseModel):
    is_weather_query: bool 
    reasoning: str 


guardrail_agent = Agent(
    name="Guardrail Agent",
    instructions="check if user is asking about weather or not",
    output_type=WeatherInputGuardrail,
)


@input_guardrail
async def weather_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent, 
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput: 
    result = await Runner.run(guardrail_agent, input, context=ctx.context, run_config=config)
    return GuardrailFunctionOutput(
        output_info = result.final_output,
        tripwire_triggered = not result.final_output.is_weather_query,
    )



@function_tool
def get_weather(city: str) -> str:
    """returns the weather of a city"""
    return f"The weather of {city} is sunny"


async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
        input_guardrails=[weather_guardrail],
        tools=[get_weather]
    )

    result = await Runner.run(agent, "how is the weather in islamabad?", run_config=config)
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())