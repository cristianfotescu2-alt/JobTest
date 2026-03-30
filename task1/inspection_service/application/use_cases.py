from pathlib import Path
from time import perf_counter

from inspection_service.domain.errors import FileValidationError, UnsupportedImageFormatError
from inspection_service.domain.models import InspectionRequest, InspectionResult
from inspection_service.domain.ports import DetectorPort
from inspection_service.domain.services import DefectDecisionService

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


class InspectImageUseCase:
    def __init__(self, detector: DetectorPort) -> None:
        self.detector = detector

    def execute(self, request: InspectionRequest) -> InspectionResult:
        start = perf_counter()

        image_path = Path(request.image_path)
        if not image_path.exists():
            raise FileValidationError(f"File not found: {request.image_path}")
        if image_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise UnsupportedImageFormatError(
                f"Unsupported image format: {image_path.suffix}"
            )

        detections = self.detector.detect(
            image_path=str(image_path),
            class_name=request.class_name,
            model_path=request.model,
            timeout_s=request.timeout_s,
        )
        status, confidence, defect_type, recommendation = DefectDecisionService.evaluate(
            detections=detections,
            class_name=request.class_name,
            threshold=request.threshold,
        )
        elapsed_ms = int((perf_counter() - start) * 1000)
        return InspectionResult(
            filename=image_path.name,
            status=status,
            confidence=confidence,
            defect_type=defect_type,
            recommendation=recommendation,
            processing_time_ms=elapsed_ms,
        )
