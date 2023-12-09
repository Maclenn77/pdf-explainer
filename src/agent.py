"""An Langchain Agent that uses ChromaDB as a query tool"""
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from src.search import Search


class PDFExplainer:
    """An Agent that uses ChromaDB as a query tool"""

    def __init__(self, llm, chroma_db):
        """Initialize the Agent"""
        search = Search(chroma_db)

        tools = [
            Tool.from_function(
                func=search.run,
                name="Search DB",
                description="Useful when you need to answer questions about a PDF in the collection.",
                handle_parsing_errors=True,
            )
        ]

        self.agent = initialize_agent(
            tools,
            llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
        )
