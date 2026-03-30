from insight_service.application.fallback import fallback_manager_insight
from insight_service.domain.schemas import Task1InspectionOutput


def test_fallback_defect_detected_message() -> None:
    ctx = Task1InspectionOutput(
        filename="part.jpg",
        status="DEFECT_DETECTED",
        confidence=0.87,
        defect_type="surface scratch",
        recommendation="REVIEW/REWORK",
        processing_time_ms=123,
    )
    msg = fallback_manager_insight(ctx)
    assert "surface scratch" in msg
    assert "87%" in msg
    assert "REVIEW/REWORK" in msg


def test_fallback_error_message_includes_retry() -> None:
    ctx = Task1InspectionOutput(
        filename="part.jpg",
        status="ERROR",
        confidence=0.0,
        defect_type="none",
        recommendation="RETRY",
        processing_time_ms=50,
        error="Prediction timed out",
    )
    msg = fallback_manager_insight(ctx)
    assert "could not be completed" in msg
    assert "retry" in msg.lower()
    assert "Prediction timed out" in msg
