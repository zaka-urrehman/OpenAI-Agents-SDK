import os
import asyncio
from dataclasses import dataclass
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, RunContextWrapper, enable_verbose_stdout_logging
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

enable_verbose_stdout_logging()
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

@dataclass
class WeatherInfo:
    city: str



@function_tool
def get_weather(ctx: RunContextWrapper[WeatherInfo]) -> WeatherInfo:
    """returns the weather information of a city. requires no parameters"""

    cities_weather_data = [
        {
            "city": "Islamabad",
            "temperature": 32.5,
            "description": "Sunny"
        },
        {
            "city": "Lahore",
            "temperature": 25.5,
            "description": "Cloudy"
        },
        {
            "city": "Karachi",
            "temperature": 30.5,
            "description": "Rainy"
        }
    ]

    for city_weather_data in cities_weather_data:
        if city_weather_data["city"] == ctx.context.city:
            # return city=city_weather_data["city"], temperature=city_weather_data["temperature"], description=city_weather_data["description"])
           
            return city_weather_data
    return None


async def main():
    current_city = WeatherInfo(city="Karachi")
    

    agent = Agent(
        name="Assistant",
        instructions="you are a helpful assistant that give weather information to a user. you have a tool to get the weather information. the tool will automatically give you the info about the city of user. you don't need to ask about the city of user",
        # model=model,
        tools=[get_weather]
    )

    result = await Runner.run(agent, "what is the weather in my city?", run_config=config, context=current_city)
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())