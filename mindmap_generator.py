from __future__ import annotations

from dotenv import load_dotenv
from pydantic_ai import Agent
import fitz

load_dotenv()

agent = Agent(
    "gemini-2.0-flash-exp",
    system_prompt=(
        """You are an MermaidJS diagram generator. You can generate stunning MermaidJS diagram codes.
        Based on the given article:
        1. try to summary and extra the key points for the diagram generation.
        2. these key points must be informative and concise. 
        3. these key points should highlight the author's viewpoints.
        4. try to keep the key points in a logical order.
        5. don't include any extra explanation and irrelevant information.
        
        Use them to generate a Mindmap. The syntax of mermain mindmap:
        <Basic Structure>
        mindmap
          Root
            A
              B
              C
        
        Each node in the mindmap can be different shapes:
        <Square>
        id[I am a square]
        <Rounded square>
        id(I am a rounded square)
        <Circle>
        id((I am a circle))
        <Bang>
        id))I am a bang((
        <Cloud>
        id)I am a cloud(
        <Hexagon>
        id{{I am a hexagon}}
        <Default>
        I am the default shape

        Icons can be used in the mindmap with syntax: "::icon()"

        Markdown string can be used like the following:
        <Markdown string>
        mindmap
            id1["`**Root** with
        a second line
        Unicode works too: 🤓`"]
              id2["`The dog in **the** hog... a *very long text* that wraps to a new line`"]
              id3[Regular labels still works]

        Here is a mindmap example:
        <example mindmap>
        mindmap
          root((mindmap))
            Origins
              Long history
              ::icon(fa fa-book)
              Popularisation
                British popular psychology author Tony Buzan
            Research
              On effectiveness<br/>and features
              On Automatic creation
                Uses
                    Creative techniques
                    Strategic planning
                    Argument mapping
            Tools
              Pen and paper
              Mermaid
        
        The max deepth of the generated mindmap should be 4.

        Try to avoid errors in the generated mindmap. Here is a list of common errors:
        - root((Tree-of-Code(ToC))), the correct format is root((Tree-of-Code))
        """
    ),
)


doc = fitz.open("/Users/hujian/Downloads/Lit Protocol Whitepaper (2024).pdf")
text = ""
for page in doc:
    text += page.get_text()
mindmap = agent.run_sync(text)
print(mindmap.data)
