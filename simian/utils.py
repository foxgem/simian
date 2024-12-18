from markdown_pdf import MarkdownPdf
from markdown_pdf import Section

report_dir = "pdf"


def pdf_report(topic: str, markdown: str) -> str:
    pdf = MarkdownPdf()
    pdf.add_section(Section(markdown))
    pdf.save(f"{report_dir}/{topic}.pdf")
    return


def write(name: str, markdown: str, append=False) -> str:
    mode = "a" if append else "w"
    with open(f"{report_dir}/{name}.md", mode) as f:
        f.write(markdown)
    return
