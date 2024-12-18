from markdown_pdf import MarkdownPdf
from markdown_pdf import Section


def pdf_report(topic: str, markdown: str) -> str:
    pdf = MarkdownPdf()
    pdf.add_section(Section(markdown))
    pdf.save(f"pdf/{topic}.pdf")
    return


def write(name: str, markdown: str, append=False) -> str:
    mode = "a" if append else "w"
    with open(f"md/{name}.md", mode) as f:
        f.write(markdown)
    return
