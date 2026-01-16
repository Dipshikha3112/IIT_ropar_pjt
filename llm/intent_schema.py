# llm/intent_schema.py
from typing import List, Optional
from pydantic import BaseModel, Field


class Intent(BaseModel):
    """
    Structured intent extracted from user query.
    This is the ONLY thing downstream systems trust.
    """

    domain: Optional[str] = Field(
        default=None,
        description="Target domain: movies | news | products | null"
    )

    keywords: List[str] = Field(
        default_factory=list,
        description="Important keywords or concepts"
    )

    mood: Optional[str] = Field(
        default=None,
        description="User mood if detectable (happy, sad, uplifting, serious, etc.)"
    )

    length: Optional[str] = Field(
        default=None,
        description="Content length preference: short | medium | long"
    )

    recency_bias: bool = Field(
        default=False,
        description="Prefer recent content"
    )

    top_k: int = Field(
        default=10,
        description="Number of results desired"
    )
