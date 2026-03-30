from abc import ABC, abstractmethod

from inspection_service.domain.models import Detection


class DetectorPort(ABC):
    @abstractmethod
    def detect(
        self,
        image_path: str,
        class_name: str,
        model_path: str,
        timeout_s: float,
    ) -> list[Detection]:
        raise NotImplementedError
