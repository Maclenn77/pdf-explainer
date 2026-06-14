"""An Langchain Agent that uses ChromaDB as a query tool"""
import os
from pathlib import Path

from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.tools import Tool
from langchain.schema import SystemMessage
from gnosis.search import Search

def load_system_prompt() -> SystemMessage:
    """Load system prompt from a markdown file defined in SYSTEM_PROMPT_PATH,
    or fall back to SYSTEM_PROMPT env var, or use a default."""
    prompt_path = os.getenv("SYSTEM_PROMPT_PATH")
    if prompt_path:
        path = Path(prompt_path)
        if path.exists():
            return SystemMessage(content=path.read_text(encoding="utf-8"))

    fallback = os.getenv("SYSTEM_PROMPT")
    if fallback:
        return SystemMessage(content=fallback)

    return SystemMessage(content=(
        "You are a helpful assistant with access to a private document database. "
        "Only use information retrieved from the database or Wikipedia if tool is enabled. "
        "If the answer is not there, say so clearly."
    ))

class PDFExplainer:
    """An Agent that uses ChromaDB as a query tool"""

    def __init__(self, llm, chroma_db, extra_tools=False):
        """Initialize the Agent"""
        search = Search(chroma_db)

        self.tools = [
            Tool.from_function(
                func=search.run,
                name="Search_on_ChromaDB",
                description="Useful when you need more context for answering a question.",
                handle_parsing_errors=True,
                agent_kwargs={"system_message": load_system_prompt()},
            )
        ]

        if extra_tools:
            self.tools.extend(load_tools(["wikipedia"]))

        self.agent = initialize_agent(
            self.tools,
            llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=False,
            handle_parsing_errors=True,
        )

    def add_tools(self, tools: list[Tool]):
        """Add tools to the Agent"""
        self.tools.extend(tools)

    def replace_agent(self, agent: AgentType, llm):
        """Replace the Agent"""
        self.agent = initialize_agent(
            self.tools,
            llm,
            agent=agent,
            verbose=False,
            handle_parsing_errors=True,
        )
