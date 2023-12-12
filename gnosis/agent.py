"""An Langchain Agent that uses ChromaDB as a query tool"""
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.tools import Tool
from gnosis.search import Search


class PDFExplainer:
    """An Agent that uses ChromaDB as a query tool"""

    def __init__(self, llm, chroma_db, extra_tools=False):
        """Initialize the Agent"""
        search = Search(chroma_db)

        self.tools = [
            Tool.from_function(
                func=search.run,
                name="Search on ChromaDB",
                description="Useful when you need more context for answering a question.",
                handle_parsing_errors=True,
            )
        ]

        if extra_tools:
            self.tools.extend(load_tools(["wikipedia"]))

        self.agent = initialize_agent(
            self.tools,
            llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
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
