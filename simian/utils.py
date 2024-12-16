from markdown_pdf import MarkdownPdf
from markdown_pdf import Section


def pdf_report(topic: str, markdown: str) -> str:
    pdf = MarkdownPdf()
    pdf.add_section(Section(markdown))
    pdf.save(f"pdf/{topic}.pdf")
    return
