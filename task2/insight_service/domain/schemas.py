from typing import Any

from pydantic import BaseModel, Field


class Task1InspectionOutput(BaseModel):
    filename: str
    status: str = Field(description="DEFECT_DETECTED | NO_DEFECT_DETECTED | ERROR")
    confidence: float = Field(ge=0.0, le=1.0)
    defect_type: str
    recommendation: str
    processing_time_ms: int = Field(ge=0)
    error: str | None = None

    @classmethod
    def from_json_obj(cls, obj: Any) -> "Task1InspectionOutput":
        return cls.model_validate(obj)


class ManagerInsight(BaseModel):
    insight: str = Field(
        description="Plain-English insight for a non-technical factory floor manager."
    )
