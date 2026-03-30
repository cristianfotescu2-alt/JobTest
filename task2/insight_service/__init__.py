from insight_service.application.use_cases import GenerateManagerInsightUseCase
from insight_service.domain.schemas import Task1InspectionOutput
from insight_service.infrastructure.openai_langchain_client import OpenAILangChainClient


def generate_manager_insight(task1_output: dict) -> str:
    use_case = GenerateManagerInsightUseCase(llm_client=OpenAILangChainClient())
    validated = Task1InspectionOutput.model_validate(task1_output)
    return use_case.execute(validated)
