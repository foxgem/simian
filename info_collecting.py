from dataclasses import dataclass
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from duckduckgo_search import DDGS
from markdown_pdf import MarkdownPdf
from markdown_pdf import Section

load_dotenv()


@dataclass
class MyDeps:
    collector: Agent[None, list[str]]


collector = Agent(
    "gemini-2.0-flash-exp",
    deps_type=str,
    system_prompt="You're good at finding information.",
)


@collector.tool_plain
def search(topic: str) -> str:
    results = DDGS().text(topic, max_results=20)
    return results


analyst = Agent(
    "groq:llama-3.1-70b-versatile",
    deps_type=MyDeps,
    result_type=str,
    system_prompt="""
    You are great at analyzing information.
    Use the 'topic_collector' to gather the latest information on {topic}.
    Analyse these information, the output must be a markdown.
    """,
)


@analyst.tool
async def topic_collector(ctx: RunContext[MyDeps], topic: str) -> list[str]:
    r = await ctx.deps.collector.run(f"Please gather information on {topic}")
    return "\n".join(r.data)


def pdf_report(topic: str, markdown: str) -> str:
    pdf = MarkdownPdf()
    pdf.add_section(Section(markdown))
    pdf.save(f"{topic}.pdf")
    return


topic = "Ai16z Eliza"
result = analyst.run_sync(f"Do some research on {topic}", deps=MyDeps(collector))
markdown = result.data

pdf_report(topic, markdown)
