from insight_service.application.fallback import fallback_manager_insight
from insight_service.domain.ports import ManagerInsightLlmPort
from insight_service.domain.schemas import Task1InspectionOutput


class GenerateManagerInsightUseCase:
    def __init__(self, llm_client: ManagerInsightLlmPort) -> None:
        self.llm_client = llm_client

    def execute(self, context: Task1InspectionOutput) -> str:
        try:
            manager_insight = self.llm_client.generate(context=context)
            return manager_insight.insight.strip()
        except Exception:
            return fallback_manager_insight(context)
