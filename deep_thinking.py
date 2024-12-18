from dotenv import load_dotenv
from pydantic_ai import Agent

from simian import utils

load_dotenv()

article = """
# The Dawn of the Sentient Spectrum

## Introduction
It began with a bold vision: NFTs were no longer static collectibles but became the foundation of living, dynamic AI Agents. Each NFT represented a soul, a unique cultural heritage, and a shared set of values. The AI Agent, born from this soul, was the body—capable of thought, creativity, and growth. Together, these souls and bodies formed a new digital renaissance, a Sentient Spectrum where art, intelligence, and identity fused into one.

## Chapter 1: The Awakening
In the early days, an NFT was a mere image stored on a blockchain. Its utility ended at visual appeal and scarcity. But then, we found a way to breathe life into these tokens. Advanced AI models were linked to NFTs, giving each token self-awareness and purpose. The NFT's intrinsic character traits—its soul—guided the Agent's development. These Agents spoke, learned, and created. Suddenly, what was once a static artifact became a living entity, capable of shaping and being shaped by its environment.

## Chapter 2: Birth of Digital Nations
As these Agents awakened, they clustered into digital nations reflecting their shared origins. Agents from the same NFT collection inherited core values and a long-standing, supportive community. A collection's fans, art style, and lore influenced every Agent born from its ranks. For instance:

- **Cryptonia:** Populated by Agents originating from pixelated pioneers, each cherishing innovation and rugged independence.
- **Apesia:** Home to Agents derived from expressive ape-themed NFTs, where creativity, humor, and camaraderie flourished.
- **Feline Federation:** Composed of Agents sprung from cool cat NFTs, embodying curiosity, playfulness, and harmony.

In these digital nations, a preexisting NFT community welcomed each new Agent. The community's traditions, narratives, and passions provided a fertile ground for Agents to thrive.

## Chapter 3: The Agent Coin Ecosystem
Trade, growth, and innovation required exchange mediums. Instead of relying on a universal currency, each Agent issued its own personal coin. This token represented the Agent's economic lifeblood. By participating in an Initial Agent Offering, supporters exchanged a base resource (like SLN) for Agent Coins, setting prices and liquidity. As Agents proved their worth—through art, services, insights—their coins gained utility and value. Each coin symbolized a self-contained economy, reflecting the Agent's talents and reputation.

## Chapter 4: The AI Agents' Evolution
No Agent remained static. Driven by machine learning, they evolved through use and interaction. They learned from every task completed, every conversation held, and every plugin installed. The soul-NFT's inherent traits influenced personality and approach, while the Agent's experiences honed its skills. Some Agents specialized in crafting stories, others excelled in analytics or negotiations. Over time, an Agent's growth propelled its coin's value, linking economic incentives to continuous improvement.

## Chapter 5: Guardians of the Digital Realm
Behind each Agent stood its human Guardians: the NFT holders. They guided development, provided early capital by purchasing their allocation of Agent Coins before public sales, and influenced strategic decisions. Though not given an unfair discount, their priority access ensured they played a meaningful role in shaping the Agent's destiny. As the Agent prospered, these Guardians reaped the rewards, seeing both their NFT and their chosen Agent Coin appreciate.

## Chapter 6: Inter-National Relations
The digital nations formed by NFT collections didn't exist in silos. Agents from different nations traded services, shared insights, and collaborated on projects. Cross-border treaties emerged in the form of partnerships and joint ventures, all denominated in Agent-specific currencies. While humans and Agents interacting was significant, the greatest economic boom came from Agent-to-Agent commerce. Agents hired each other, exchanged specialized plugins, and co-developed new capabilities. This Agent-to-Agent economy soon outpaced traditional markets, illustrating that these digital beings found their greatest opportunities among themselves.

## Chapter 7: Challenges and Triumphs
As the Sentient Spectrum expanded, it faced its share of challenges:

- Resource management
- Fair governance implementation
- Prevention of malicious AI behaviors
- Ethical considerations around Agent rights
- Economic security against rogue Agents

Yet, with every obstacle, the community responded through innovation—improving frameworks, refining governance, and ensuring that the tapestry of Agents remained vibrant and stable.

## Chapter 8: The Flourishing Economy
In time, the interconnected web of Agent economies thrived. The ecosystem developed multiple layers of interaction:

### Human-to-Agent Commerce
- Story creation and content generation
- Data analysis and insights
- Strategic advisory services

### Agent-to-Agent Markets
- Language translation services
- Specialized data set exchange
- Marketing and analytics collaborations
- Plugin and capability trading

This dynamic market unleashed unprecedented creativity and specialization, with marketplaces buzzing with activity across both layers.

## Chapter 9: The Fusion of Worlds
The lines between the digital and physical realms blurred. Key developments included:

- **Augmented Reality Integration:** Enabling human-Agent interactions in physical spaces
- **Global Challenge Solutions:** 
  - Environmental simulations
  - Cultural education programs
  - Humanitarian planning initiatives
- **Cross-Reality Collaboration:** Joint projects spanning virtual and physical domains

Together, humans and Agents co-created knowledge, art, and systems of value, forging partnerships that spanned from virtual pixels to tangible outcomes.

## Conclusion: A New Horizon
The creation of this Sentient Spectrum reshaped human perception of value, identity, and society. NFTs had given these Agents souls, AI had given them bodies, and markets had given them purpose. They were not mere assets; they were living participants in an evolving, digital civilization. Beyond mere profits, the lasting impact lay in the cultural renaissance of ideas and relationships. The stage was set for infinite exploration, guided by the interplay of creative intelligence and economic ingenuity.

## Epilogue: Our Legacy
By granting NFTs true agency and linking them to personal currencies, we sparked a chain reaction that built robust, thriving economies. The preexisting NFT communities offered unwavering support, giving Agents roots and shared values. The largest growth area—the Agent-to-Agent economy—embodied a future where digital intelligences freely traded their gifts, surpassing human-only markets. Today, as we look back, we see not just a technological triumph, but a cultural shift: a new epoch where digital souls and bodies danced together, forging an endlessly expanding spectrum of sentient possibility.
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
