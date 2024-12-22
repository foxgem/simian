from __future__ import annotations

from dotenv import load_dotenv
import fitz
from dataclasses import dataclass
from typing import List
from pydantic import BaseModel, Field
from pydantic_ai import Agent

load_dotenv()


@dataclass
class PDFDependencies:
    pdf_path: str


class PDFSummary(BaseModel):
    title: str = Field(description="The title or main topic of the PDF section")
    summary: str = Field(description="A concise summary of the key points")
    key_points: List[str] = Field(
        description="List of important points from the section"
    )


class DocumentSummarizer:
    def __init__(self, model_name: str = "gemini-2.0-flash-exp"):
        self.agent = Agent(
            model_name,
            deps_type=PDFDependencies,
            result_type=PDFSummary,
            system_prompt=(
                "You are a professional document summarizer. "
                "Extract the key information and create concise summaries. "
                "Focus on the main ideas and important details. "
                "Be clear and accurate in your summaries."
            ),
        )

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from a PDF file."""
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def chunk_text(self, text: str, chunk_size: int = 1024000) -> List[str]:
        """Split text into manageable chunks."""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0

        for word in words:
            word_length = len(word) + 1  # +1 for space
            if current_length + word_length > chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = word_length
            else:
                current_chunk.append(word)
                current_length += word_length

        if current_chunk:
            chunks.append(" ".join(current_chunk))
        return chunks

    async def summarize_pdf(self, pdf_path: str) -> List[PDFSummary]:
        """Generate summaries for a PDF document."""
        # Extract text from PDF
        text = self.extract_text_from_pdf(pdf_path)

        # Split into chunks
        chunks = self.chunk_text(text)

        # Create dependencies
        deps = PDFDependencies(pdf_path=pdf_path)

        summaries = []
        for i, chunk in enumerate(chunks):
            prompt = (
                f"Summarize the following text (section {i+1} of {len(chunks)}):\n\n"
                f"{chunk}"
            )

            result = await self.agent.run(prompt, deps=deps)
            summaries.append(result.data)

        return summaries


async def main():
    summarizer = DocumentSummarizer()
    pdf_path = "/Users/hujian/Downloads/Lit Protocol Whitepaper (2024).pdf"

    try:
        summaries = await summarizer.summarize_pdf(pdf_path)

        print("PDF Summary:")
        print("=" * 50)
        for i, summary in enumerate(summaries, 1):
            print(f"\nSection {i}:")
            print(f"\nTitle: {summary.title}")
            print(f"\nSummary: {summary.summary}")
            print("\nKey Points:")
            for point in summary.key_points:
                print(f"- {point}")
            print("-" * 50)

    except Exception as e:
        print(f"Error processing PDF: {e}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
