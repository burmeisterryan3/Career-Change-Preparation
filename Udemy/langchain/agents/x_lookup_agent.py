"""Agent for looking up a person's X username."""

import os

from dotenv import load_dotenv
from langchain import hub  # leverage prompts from the community hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

from tools.tools import get_profile_url_tavily

load_dotenv()


def lookup(name: str, details: str = "") -> str:
    """X agent for looking up a person's X username."""
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo",
        api_key=os.environ["OPENAI_API_KEY"],
    )

    template = (
        "Given the full name {name_of_person} and other information about them "
        + "{details}, I want you to find the link to their X profile "
        + "page. Extract from the profile the username. Your answer should only"
        + " include the username."
    )
    prompt_template = PromptTemplate(
        input_variables=["name_of_person", "details"], template=template
    )
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 X Profile Page",
            func=get_profile_url_tavily,
            description="Use when you need the X profile URL of a person.",
        )
    ]

    react_prompt = hub.pull(
        "hwchase17/react", api_key=os.environ["TAVILY_API_KEY"]
    )
    agent = create_react_agent(
        llm=llm, tools=tools_for_agent, prompt=react_prompt
    )
    agent_executor = AgentExecutor(
        agent=agent, tools=tools_for_agent, verbose=True
    )  # invokes the agents... calls another Python function

    res = agent_executor.invoke(
        input={
            "input": prompt_template.format_prompt(
                name_of_person=name, details=details
            )
        }
    )

    x_username = res["output"]
    return x_username


if __name__ == "__main__":
    x_username = lookup(name="Elon Musk")
    print(x_username)
