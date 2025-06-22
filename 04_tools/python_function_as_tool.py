from agents.tool import function_tool
from agents import Agent, Runner, AsyncOpenAI,ItemHelpers, set_tracing_disabled, set_default_openai_api, set_default_openai_client, OpenAIChatCompletionsModel
from dotenv import load_dotenv
import asyncio
import os



@function_tool
def get_weather(location: str, unit: str = "C") -> str:
  """
  Fetch the weather for a given location, returning a short description.
  """
  # Example logic
  return f"The weather in {location} is 22 degrees {unit}."


@function_tool
def get_user_info(user_name: str) -> str:
    """
    Fetch user information for a given user name.
    """
    students = [
     {
       "user_name": "johndoe123",
       "name": "John Doe",
       "age": 20,
       "email": "john.doe@example.com"
     },
     {
       "user_name": "janesmith456",
       "name": "Jane Smith",
       "age": 21,
       "email": "jane.smith@example.com"
     },
     {
       "user_name": "jimbeam789",
       "name": "Jim Beam",
       "age": 22,
       "email": "jim.beam@example.com"
     }
   ]
    for student in students:
      if student["user_name"] == user_name:
        return f"Name: {student['name']}, Email: {student['email']}, Age: {student['age']}"
    return f"User {user_name} not found."


load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set.")

external_client = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

set_tracing_disabled(True)
set_default_openai_api("chat_completions")
set_default_openai_client(external_client)



async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant that can use tools to get information.",
        tools=[get_user_info, get_weather],
        model="gemini-2.0-flash"
    )
    result = Runner.run_streamed(agent, "Tell me about jimbeam789?")

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