from dotenv import load_dotenv
from pydantic_ai import Agent

from simian import utils

load_dotenv()

article = """
NFT as the Soul: The NFT represents the Agent’s unique identity, origin story, and personality—its “soul.” This ties it to a cultural or thematic heritage (the clan) and ensures each Agent is more than just an AI tool; it’s a character or digital being.

AI Agent as the Body: The AI is the Agent’s functional aspect—its “body” that can learn, act, create, and serve the community. The Agent uses AI capabilities to fulfill the intentions, stories, and potential encoded in its NFT soul.
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

conversions = []

print("Deep thinking started ...")

questions = reader.run_sync(article)
answers = writer.run_sync(f"article:{article}\nquestions:{questions.data}")
conversions.append(answers.data)

loops = range(max_loop - 1)
for x in loops:
    print("Thinking ...")
    questions = reader.run_sync(
        f"the answers to the last questions:{answers.new_messages()}, based on them, ask new questions or ask for explanation.",
        message_history=questions.all_messages(),
    )
    answers = writer.run_sync(
        f"{questions.data}", message_history=answers.all_messages()
    )
    conversions.append(answers.data)

print("Writing the report ...")

utils.pdf_report("deep_thinking", "\n".join(conversions))

print("Done!")
