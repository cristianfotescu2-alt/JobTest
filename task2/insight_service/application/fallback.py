from insight_service.domain.schemas import Task1InspectionOutput


def fallback_manager_insight(context: Task1InspectionOutput) -> str:
    if context.status == "ERROR":
        base = (
            f"Automated inspection could not be completed for {context.filename}. "
            "Please retry the scan, and if it still fails, send the part to manual QA."
        )
        if context.error:
            return f"{base} Error detail: {context.error}"
        return base

    confidence_pct = int(round(context.confidence * 100))
    if context.status == "DEFECT_DETECTED":
        defect = context.defect_type or "a defect"
        return (
            f"A {defect} was detected on {context.filename} with {confidence_pct}% confidence. "
            f"The part is flagged as '{context.recommendation}'. "
            "Likely causes include tooling wear or rough material handling; please inspect and correct upstream conditions."
        )

    return (
        f"No defect was detected on {context.filename} (confidence {confidence_pct}%). "
        f"Recommendation: '{context.recommendation}'."
    )
