from langchain.utilities import GoogleSerperAPIWrapper
from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI


def get_agent(serper_api_key, openai_api_key):
    search = GoogleSerperAPIWrapper(serper_api_key=serper_api_key)
    search_tool = Tool(
        name="web_search",
        description="Always use this tool for all questions",
        func=search.run,
    )

    llm = ChatOpenAI(model_name="gpt-4", temperature=0, openai_api_key=openai_api_key)
    tools = [search_tool]
    memory = ConversationBufferWindowMemory(memory_key="chat_history", k=4)
    agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True,
                                   memory=memory)

    return agent_chain
