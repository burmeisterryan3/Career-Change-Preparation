from langchain_community.tools.tavily_search import TavilySearchResults


def get_profile_url_tavily(name: str) -> str:
    """Given the full name of a person, find their profile URL using Tavily Search."""
    # TODO: Add an argument for profile type, e.g., LinkedIn, Twitter, etc. Create a dictionary of profile types and domains to ensure only the appropriate domain is searched.
    search = TavilySearchResults(
        include_domains=["www.linkedin.com/in/", "x.com"]
    )
    result = search.run(f"{name}")
    return result[0]["url"]
