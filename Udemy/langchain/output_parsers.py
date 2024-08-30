from typing import Any, Dict, List

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field


class Summary(BaseModel):
    """Define the output of the ice breaker agent."""

    summary: str = Field(description="summary")
    facts: List[str] = Field(description="interesting facts about them")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the object to a dictionary."""
        return {"summary": self.summary, "facts": self.facts}


summary_parser = PydanticOutputParser(pydantic_object=Summary)
