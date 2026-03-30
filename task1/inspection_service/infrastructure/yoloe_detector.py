from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from typing import Any

from ultralytics import YOLOE

from inspection_service.domain.errors import DetectorError, InspectionTimeoutError
from inspection_service.domain.models import Detection
from inspection_service.domain.ports import DetectorPort


class UltralyticsYoloeDetector(DetectorPort):
    def __init__(self) -> None:
        self._loaded_model_path: str | None = None
        self._model: Any | None = None

    def _get_model(self, model_path: str) -> Any:
        if self._model is None or self._loaded_model_path != model_path:
            self._model = YOLOE(model_path)
            self._loaded_model_path = model_path
        return self._model

    def detect(
        self,
        image_path: str,
        class_name: str,
        model_path: str,
        timeout_s: float,
    ) -> list[Detection]:
        try:
            model = self._get_model(model_path)
            model.set_classes([class_name])

            def _predict() -> Any:
                return model.predict(source=image_path, verbose=False)

            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(_predict)
                try:
                    results = future.result(timeout=timeout_s)
                except FuturesTimeoutError as exc:
                    raise InspectionTimeoutError(
                        f"Prediction timed out after {timeout_s} seconds"
                    ) from exc

            if not results:
                return []

            result = results[0]
            boxes = getattr(result, "boxes", None)
            if boxes is None or boxes.conf is None:
                return []

            confidences = boxes.conf.tolist()
            return [Detection(label=class_name, confidence=float(c)) for c in confidences]
        except InspectionTimeoutError:
            raise
        except Exception as exc:
            raise DetectorError(f"YOLOE detection failed: {exc}") from exc
