import os
from typing import List

from callbacks import AgentCallbackHandler
from dotenv import load_dotenv
from langchain.agents import tool
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.prompts.prompt import PromptTemplate
from langchain.schema import AgentAction, AgentFinish
from langchain.tools import Tool
from langchain.tools.render import render_text_description
from langchain_openai import ChatOpenAI


@tool
def get_text_length(text: str) -> int:
    """Returns the length of a text by characters."""
    text = (
        text.strip("\n").strip("'").strip('"')
    )  # stripping non-alphabetic characters just in case

    print(f"get_text_length text to evaluate: {text=}")

    return len(text)


def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    for t in tools:
        if t.name == tool_name:
            return t
    raise ValueError(f"Tool with name {tool_name} not found in tools list.")


if __name__ == "__main__":
    load_dotenv()
    print("Hello ReAct LangChain!")

    tools = [get_text_length]

    template = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}
"""

    prompt = PromptTemplate(
        input_variables=["input", "agent_scratchpad"],
        template=template,
        partial_variables={
            "tools": render_text_description(tools),
            "tool_names": ", ".join([t.name for t in tools]),
        },
    )

    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo",
        callbacks=[AgentCallbackHandler()],
        api_key=os.environ["OPENAI_API_KEY"],
    ).bind(stop=["\nObservation"])  # stop to ensure multiple steps

    intermediate_steps = []

    agent = prompt | llm | ReActSingleInputOutputParser()

    # The below is what the AgentExecutor class does for us
    agent_step = ""
    while not isinstance(agent_step, AgentFinish):
        agent_step: AgentAction | AgentFinish = agent.invoke(
            input={
                "input": "What is the length, in characters, of the text: DOG?",
                "agent_scratchpad": format_log_to_str(intermediate_steps),
            }
        )

        if isinstance(agent_step, AgentAction):
            tool_name = agent_step.tool
            tool_to_use = find_tool_by_name(tools, tool_name)
            tool_input = agent_step.tool_input

            observation = tool_to_use.func(str(tool_input))
            intermediate_steps.append((agent_step, str(observation)))

    if isinstance(agent_step, AgentFinish):
        print(f"Final Answer: {agent_step.return_values}")
