from inspection_service.domain.models import Detection
from inspection_service.domain.services import DefectDecisionService


def test_defect_detected_when_confidence_reaches_threshold() -> None:
    detections = [Detection(label="scratch", confidence=0.81)]
    status, confidence, defect_type, recommendation = DefectDecisionService.evaluate(
        detections=detections,
        class_name="scratch",
        threshold=0.5,
    )

    assert status == "DEFECT_DETECTED"
    assert confidence == 0.81
    assert defect_type == "scratch"
    assert recommendation == "REVIEW/REWORK"


def test_no_defect_detected_when_no_detections() -> None:
    status, confidence, defect_type, recommendation = DefectDecisionService.evaluate(
        detections=[],
        class_name="scratch",
        threshold=0.5,
    )

    assert status == "NO_DEFECT_DETECTED"
    assert confidence == 0.0
    assert defect_type == "none"
    assert recommendation == "PASS"
