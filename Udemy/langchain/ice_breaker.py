import os
from typing import Tuple

from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_ollama import ChatOllama  # noqa: F401
from langchain_openai import ChatOpenAI  # noqa: F401

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.x_lookup_agent import lookup as x_lookup_agent
from output_parsers import Summary, summary_parser
from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweets


def ice_break_with(name: str, details: str = "") -> Tuple[Summary, str]:
    linkedin_url = linkedin_lookup_agent(name=name, details=details)
    linkedin_data = scrape_linkedin_profile(linkedin_url, mock=True)

    x_username = x_lookup_agent(name=name, details=details)
    tweets = scrape_user_tweets(username=x_username, mock=True)

    summary_template = """
        Given information about a person from LinkedIn {information}
        and X posts {x_posts}, I want you to create:
        1. A short summary about them and
        2. Two interesting facts about them.

        Use both information from X and LinkedIn.
        \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information", "x_posts"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

    # llm = ChatOllama(model="llama3")
    # llm = ChatOllama(model="mistral")
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo",
        api_key=os.environ["OPENAI_API_KEY"],
    )

    chain = summary_prompt_template | llm | summary_parser
    res: Summary = chain.invoke(
        input={"information": linkedin_data, "x_posts": tweets}
    )

    return res, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    load_dotenv()

    print("Ice Breaker Enter")
    ice_break_with("Eden Marco", "Udemy Instructor and Google Engineer")
