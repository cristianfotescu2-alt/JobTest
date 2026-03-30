import os

from dotenv import load_dotenv
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from pydantic import ValidationError

from insight_service.application.prompts import MANAGER_INSIGHT_PROMPT
from insight_service.domain.errors import LlmUnavailableError
from insight_service.domain.ports import ManagerInsightLlmPort
from insight_service.domain.schemas import ManagerInsight, Task1InspectionOutput


class OpenAILangChainClient(ManagerInsightLlmPort):
    def __init__(self) -> None:
        load_dotenv()

        self._api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self._model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()

    def generate(self, context: Task1InspectionOutput) -> ManagerInsight:
        if not self._api_key:
            raise LlmUnavailableError("Missing OPENAI_API_KEY in .env")

        parser = PydanticOutputParser(pydantic_object=ManagerInsight)
        format_instructions = parser.get_format_instructions()

        prompt = (
            f"{MANAGER_INSIGHT_PROMPT}\n\n"
            f"{format_instructions}\n\n"
            "Task1InspectionOutput JSON:\n"
            f"{context.model_dump_json()}\n"
        )

        try:
            llm = ChatOpenAI(model=self._model, api_key=self._api_key, temperature=0)
            response = llm.invoke(prompt)
            content = getattr(response, "content", None)
            if not isinstance(content, str):
                raise LlmUnavailableError("LLM returned non-text content")
            return parser.parse(content)
        except (ValidationError, LlmUnavailableError):
            raise
        except Exception as exc:
            raise LlmUnavailableError(f"LLM request failed: {exc}") from exc
