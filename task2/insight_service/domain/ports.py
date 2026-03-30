from abc import ABC, abstractmethod

from insight_service.domain.schemas import ManagerInsight, Task1InspectionOutput


class ManagerInsightLlmPort(ABC):
    @abstractmethod
    def generate(self, context: Task1InspectionOutput) -> ManagerInsight:
        raise NotImplementedError
