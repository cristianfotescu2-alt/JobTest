import argparse
import json
import sys
from pathlib import Path
from time import perf_counter

from inspection_service.application.use_cases import InspectImageUseCase
from inspection_service.domain.errors import (
    DetectorError,
    FileValidationError,
    InspectionTimeoutError,
    UnsupportedImageFormatError,
)
from inspection_service.domain.models import InspectionRequest, InspectionResult
from inspection_service.infrastructure.yoloe_detector import UltralyticsYoloeDetector


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="YOLOE image defect inspection service")
    parser.add_argument("--image", required=True, help="Input image file path")
    parser.add_argument(
        "--class-name",
        required=True,
        help="Defect class prompt for YOLOE, e.g. scratch",
    )
    parser.add_argument(
        "--model",
        default="yoloe-26n-seg.pt",
        help="YOLOE model weights path or name",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.25,
        help="Confidence threshold for defect detection decision",
    )
    parser.add_argument(
        "--timeout-s",
        type=float,
        default=30.0,
        help="Prediction timeout in seconds",
    )
    return parser


def _error_result(filename: str, elapsed_ms: int) -> InspectionResult:
    return InspectionResult(
        filename=filename,
        status="ERROR",
        confidence=0.0,
        defect_type="none",
        recommendation="RETRY",
        processing_time_ms=elapsed_ms,
    )


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    start = perf_counter()
    filename = Path(args.image).name

    try:
        detector = UltralyticsYoloeDetector()
        use_case = InspectImageUseCase(detector=detector)
        request = InspectionRequest(
            image_path=args.image,
            class_name=args.class_name,
            model=args.model,
            threshold=args.threshold,
            timeout_s=args.timeout_s,
        )
        result = use_case.execute(request)
        print(json.dumps(result.to_dict(), indent=2))
        return 0
    except (
        FileValidationError,
        UnsupportedImageFormatError,
        InspectionTimeoutError,
        DetectorError,
    ) as exc:
        elapsed_ms = int((perf_counter() - start) * 1000)
        error_payload = _error_result(filename=filename, elapsed_ms=elapsed_ms).to_dict()
        error_payload["error"] = str(exc)
        print(json.dumps(error_payload, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
