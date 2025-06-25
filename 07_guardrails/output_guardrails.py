import os
import asyncio
from pydantic import BaseModel
from dotenv import load_dotenv
from agents import (Agent, 
                    Runner,
                    AsyncOpenAI, 
                    OpenAIChatCompletionsModel, 
                    output_guardrail, 
                    RunContextWrapper, 
                    TResponseInputItem, 
                    GuardrailFunctionOutput
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


class UrduCheckOutputGuardrail(BaseModel):
    is_output_in_urdu: bool 
    reasoning: str 


output_guardrail_agent = Agent(
    name="Output Guardrail Agent",
    instructions="check if the output is in urdu or not",
    output_type=UrduCheckOutputGuardrail,
)


@output_guardrail
async def output_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent, 
    output: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput: 
    result = await Runner.run(output_guardrail_agent, output, context=ctx.context, run_config=config)
    return GuardrailFunctionOutput(
        output_info = result.final_output,
        tripwire_triggered = not result.final_output.is_output_in_urdu,
    )


async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
        output_guardrails=[output_guardrail]
    )

    result = await Runner.run(agent, "tell me about urdu language in urdu?", run_config=config)
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())