# llm/query_parser.py
import json
from llm.intent_schema import Intent
from llm.prompt_templates import INTENT_EXTRACTION_PROMPT


class IntentParser:
    def __init__(self, llm_client):
        self.llm = llm_client

    def parse(self, user_query: str) -> Intent:
        """
        1. Ask LLM for structured intent
        2. Validate with Pydantic
        3. Fallback safely if LLM fails
        """

        prompt = INTENT_EXTRACTION_PROMPT.format(query=user_query)

        raw_output = self.llm.generate(prompt, max_new_tokens=200)

        try:
            data = json.loads(raw_output)
            intent = Intent(**data)
            return intent

        except Exception as e:
            print("⚠️ LLM intent parsing failed:", e)
            print("Raw output:", raw_output)

            # SAFE FALLBACK
            return Intent(
                domain=None,
                keywords=user_query.split(),
                top_k=10
            )
