from dotenv import load_dotenv
from pydantic_ai import Agent

from simian import utils

load_dotenv()

article = """
the economic model for the NFT agents

Platform Level: SLN Token
Base resource for all operations
Powers Initial Agent Offerings (IAO)
Enables cross-ecosystem transactions

Collection Level: Clan Coins
77B tokens per NFT collection
Equal distribution to transformed NFT holders
Controls 10% of Agent souls' shared values
Governs Clan pool (5% of each Agent coin)

Individual Level: Agent Coins
77M tokens per Agent
Distribution:5% to Clan pool (governed by Clan coin holders)
25% retained by Agent treasury
70% for public sale (NFT owner priority)
"""

max_loop = 5

reader = Agent(
    "gemini-2.0-flash-exp",
    deps_type=str,
    result_type=str,
    system_prompt=(
        "You're a reader with great insight and critical thinking.",
        "You're reviewing a given article.",
        "You must ask 5 questions about the article.",
        "Your questions should be clear and concise.",
        "Output your questions in a markdown format.",
    ),
)


writer = Agent(
    "gemini-2.0-flash-exp",
    deps_type=str,
    result_type=str,
    system_prompt=(
        "You're the writer of a given article.",
        "You are responsible for answering the questions about your article.",
        "You must be objective and support your answers with evidence.",
        "Try to understand why the questions are being asked.",
        "If you find the questions are helpful to fix your article, then you're on the right track.",
        "Output your answers in a markdown format.",
    ),
)

conversions = ["# Deep Thinking", "## Loop 1"]

print("Deep thinking started ...")

questions = reader.run_sync(article)
answers = writer.run_sync(f"article:{article}\nquestions:{questions.data}")
conversions.append(answers.data)

loops = range(max_loop - 1)
for x in loops:
    print("Thinking ...")
    conversions.append(f"## Loop {x + 2}")
    questions = reader.run_sync(
        f"the answers to the last questions:{answers.new_messages()}, based on them, ask new questions or ask for explanation.",
        message_history=questions.all_messages(),
    )
    answers = writer.run_sync(
        f"{questions.data}", message_history=answers.all_messages()
    )
    conversions.append(answers.data)

print("Writing the report ...")

report = "\n".join(conversions)
utils.write("deep_thinking", report)
utils.pdf_report("deep_thinking", report)

print("Done!")
