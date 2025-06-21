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

