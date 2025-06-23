# Context Management

Context is the additional data that our code can use during agent's execution. OpenAI Agents SDK provide two types of context:

1. **Local Context**

Local context is available within our code. It is not exposed to the LLM. It is available to our tools, and on_handoff function etc. It is represented via the `RunContextWrapper` class and the `context` property within it. 

2. **Agent/LLM Context**

LLMs access data only through conversation history. To add new data:

- **System Prompt**: Use static or dynamic instructions (e.g., user name, date). Dynamic instructions can be provided by passing a callable
- **Runner Input**: Add data in `Runner.run` calls for less critical messages by adding in the `input` field. 
- **Function Tools**: Enable on-demand data fetching by the LLM using provided tools. 
- **Retrieval/Web Search**: Specific tools that pull relevant data from files, databases, or the web for grounded responses.


**Example**
   ```python
   @dataclass
   class CityInfo:
       city: str

   @function_tool
   def get_weather(ctx: RunContextWrapper[CityInfo]) -> CityInfo:
       """returns the weather information of a city. requires no parameters"""
        #static data representing a db
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

        #in a real app, it would check with the data from db
        for city_weather_data in cities_weather_data:
            if city_weather_data["city"] == ctx.context.city:           
                return city_weather_data
        return None 


    async def main():
        current_city = CityInfo(city="Karachi")       

        agent = Agent(
            name="Assistant",
            instructions="you are a helpful assistant that give weather information to a user. you have a tool to get the weather information. the tool will automatically give you the info about the city of user. you don't need to ask about the city of user",
            # model=model,
            tools=[get_weather]
        )

        result = await Runner.run(agent, "what is the weather in my city?", run_config=config, context=current_city)
        print(result.final_output)  
   
   ```

The above example shows how data can be made available to our tools using `RunContextWrapper`