# Task 1 - Core Python Inspection Service (YOLOE)

This project implements a Python-only image inspection service in a DDD-style structure.

It accepts:
- an image path
- a target defect class name (prompt)

It then uses Ultralytics YOLOE prompt-based prediction and returns a structured JSON response.

## Project structure

- `inspection_service/domain`: core entities, errors, ports, and defect decision rules
- `inspection_service/application`: inspection use case orchestration
- `inspection_service/infrastructure`: YOLOE adapter implementation
- `inspection_service/interfaces`: CLI entrypoint
- `tests`: unit tests

## Output JSON schema

The service returns:
- `filename`
- `status` (`DEFECT_DETECTED`, `NO_DEFECT_DETECTED`, `ERROR`)
- `confidence`
- `defect_type`
- `recommendation`
- `processing_time_ms`

## Setup (conda, Python 3.12)

```bash
conda env create -f environment.yml
conda activate task1-inspection
```

If needed:

```bash
pip install -r requirements.txt
```

## Run

```bash
python -m inspection_service.interfaces.cli \
  --image /path/to/image.jpg \
  --class-name scratch \
  --model yoloe-26n-seg.pt \
  --threshold 0.25 \
  --timeout-s 30
```

## Run tests

```bash
pytest -q
```

## Notes

- YOLOE usage follows Ultralytics predict/set_classes guidance:
  - [Ultralytics YOLOE Predict Usage](https://docs.ultralytics.com/models/yoloe/#predict-usage)
- AI coding assistance disclosure:
  - This codebase was developed with assistance from Cursor AI tooling.
