import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, trace, set_trace_processors
from agents.tracing.processor_interface import TracingProcessor
from agents.run import RunConfig
import asyncio

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
agentops_api_key = os.getenv("AGENTOPS_API_KEY")


class LocalTraceProcessor(TracingProcessor):
    def __init__(self):
        self.traces = []
        self.spans = []

    def on_trace_start(self, trace):
        self.traces.append(trace)
        print(f"Trace started: {trace.trace_id}")

    def on_trace_end(self, trace):
        # self.traces.append(trace)
        print(f"Trace ended: {trace.export()}")

    def on_span_start(self, span):
        self.spans.append(span)
        print(f"Span started: {span.span_id}")
        print(f"span details: {span.export()}")

    def on_span_end(self, span):
        print(f"Span ended: {span.span_id}")
        print(f"span details: {span.export()}")

    def force_flush(self):
        print("Forcing Flush of span data")

    def shutdown(self):
        print("----SHUTTING DOWN TRACE PROCESSOR----")

        for trace in self.traces:
            print(f"{trace.export()}")
        print("Collected Spans: ")
        for span in self.spans:
            print(f"{span.export()}")




local_processor = LocalTraceProcessor()
set_trace_processors([local_processor])


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


async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant that greets users when they say hello.",
        model=model
    )
    
    with trace("Example Workflow"):
        result = await Runner.run(agent, "Hello how are you?", run_config=config)
        print(f"Final Output: {result.final_output}")

    # result = await Runner.run(agent, "Hello how are you?", run_config=config)
    # print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())