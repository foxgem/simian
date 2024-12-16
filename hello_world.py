from dotenv import load_dotenv
from pydantic_ai import Agent

load_dotenv()

agent = Agent(
    # gemini-2.0-flash-exp
    "groq:llama-3.1-70b-versatile",
    system_prompt="Be concise, reply with one sentence.",
)

result = agent.run_sync('Where does "hello world" come from?')
print(result.data)
