from inspection_service.domain.models import Detection


class DefectDecisionService:
    @staticmethod
    def evaluate(
        detections: list[Detection],
        class_name: str,
        threshold: float,
    ) -> tuple[str, float, str, str]:
        max_conf = max((d.confidence for d in detections), default=0.0)
        if max_conf >= threshold:
            return (
                "DEFECT_DETECTED",
                round(float(max_conf), 4),
                class_name,
                "REVIEW/REWORK",
            )

        return ("NO_DEFECT_DETECTED", round(float(max_conf), 4), "none", "PASS")
