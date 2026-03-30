from dataclasses import dataclass


@dataclass(frozen=True)
class Detection:
    label: str
    confidence: float


@dataclass(frozen=True)
class InspectionRequest:
    image_path: str
    class_name: str
    model: str = "yoloe-26n-seg.pt"
    threshold: float = 0.25
    timeout_s: float = 30.0


@dataclass(frozen=True)
class InspectionResult:
    filename: str
    status: str
    confidence: float
    defect_type: str
    recommendation: str
    processing_time_ms: int

    def to_dict(self) -> dict:
        return {
            "filename": self.filename,
            "status": self.status,
            "confidence": self.confidence,
            "defect_type": self.defect_type,
            "recommendation": self.recommendation,
            "processing_time_ms": self.processing_time_ms,
        }
