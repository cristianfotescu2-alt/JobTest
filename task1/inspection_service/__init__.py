def inspect_image(
    image_path: str,
    class_name: str,
    model: str = "yoloe-26n-seg.pt",
    threshold: float = 0.25,
    timeout_s: float = 30.0,
) -> dict:
    from inspection_service.application.use_cases import InspectImageUseCase
    from inspection_service.domain.models import InspectionRequest
    from inspection_service.infrastructure.yoloe_detector import UltralyticsYoloeDetector

    detector = UltralyticsYoloeDetector()
    use_case = InspectImageUseCase(detector=detector)
    request = InspectionRequest(
        image_path=image_path,
        class_name=class_name,
        model=model,
        threshold=threshold,
        timeout_s=timeout_s,
    )
    result = use_case.execute(request)
    return result.to_dict()
