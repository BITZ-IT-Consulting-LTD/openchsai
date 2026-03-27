"""
Attention Fusion Multi-Task API Routes

Endpoints:
  POST /fusion/analyze      — Full NER + Classification + QA in one call
  POST /fusion/ner          — NER only via fusion backbone
  POST /fusion/classify     — Classification only via fusion backbone
  POST /fusion/qa           — QA scoring only via fusion backbone
  GET  /fusion/task/{id}    — Poll any fusion task result
  GET  /fusion/info         — Model load status
  POST /fusion/demo         — Built-in demo transcript
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..tasks.model_tasks import (
    fusion_analyze_task,
    fusion_classify_task,
    fusion_ner_task,
    fusion_qa_task,
)
from ..utils.mode_detector import is_api_server_mode

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/fusion", tags=["attention_fusion"])

# ── Demo transcript ────────────────────────────────────────────────────────────
DEMO_TRANSCRIPT = (
    "Hello, child helpline? Hi there, I'm Susana. How can I assist you today? "
    "I'm Daniel from Kondoa, Dodoma. There's a concern regarding Masomakali, a 7-year-old "
    "child in our neighborhood. I've noticed that he seems to be neglected physically. "
    "Oh, Daniel, it's important that you reached out. Can you tell me more about what you've "
    "observed? What kind of physical neglect are you referring to? I've seen Masomakali several "
    "times without adequate clothing or food. His parents seem to be too occupied with their own "
    "matters to provide proper care for him. This worries me greatly as he is a young child who "
    "needs nourishment and warmth. I understand your concern, Daniel. Neglect can have serious "
    "consequences on a child's development. Can I put you on hold while I reach out to child "
    "protection services? No problem. Thank you for holding and patiently waiting. I encourage "
    "you to speak with a local children's officer confidentially about your concerns for "
    "Masomakali. Thank you, Susana. This means a lot to me and to Masomakali as well. "
    "Thank you for calling. Goodbye."
)


# ── Pydantic request / response models ────────────────────────────────────────

class FusionAnalyzeRequest(BaseModel):
    transcript: str = Field(..., min_length=10, description="Call transcript text")
    threshold: float = Field(0.5, ge=0.0, le=1.0, description="QA binary threshold")


class FusionNERRequest(BaseModel):
    transcript: str = Field(..., min_length=10)


class FusionClassifyRequest(BaseModel):
    transcript: str = Field(..., min_length=10)


class FusionQARequest(BaseModel):
    transcript: str = Field(..., min_length=10)
    threshold: float = Field(0.5, ge=0.0, le=1.0)


class TaskSubmitResponse(BaseModel):
    task_id: str
    status: str
    message: str
    estimated_time: str
    status_endpoint: str


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    progress: Optional[Dict] = None


# ── Helpers ───────────────────────────────────────────────────────────────────

def _check_model_ready():
    """In standalone/worker mode verify the model is loaded locally."""
    if is_api_server_mode():
        return  # models live on the Celery workers — skip local check
    from ..model_scripts.attention_fusion_model import attention_fusion_model
    if not attention_fusion_model.is_ready():
        raise HTTPException(
            status_code=503,
            detail="Attention Fusion model is not ready. Check /health/models for status.",
        )


def _submit(task_fn, args: list, queue: str = "model_processing") -> TaskSubmitResponse:
    task = task_fn.apply_async(args=args, queue=queue)
    return TaskSubmitResponse(
        task_id=task.id,
        status="queued",
        message=f"Task submitted. Poll /fusion/task/{task.id} for results.",
        estimated_time="5-30 seconds",
        status_endpoint=f"/fusion/task/{task.id}",
    )


def _poll(task_id: str) -> TaskStatusResponse:
    result = AsyncResult(task_id)

    if result.state == "PENDING":
        return TaskStatusResponse(task_id=task_id, status="pending",
                                  progress={"message": "Task is queued"})

    if result.state in ("STARTED", "PROCESSING"):
        return TaskStatusResponse(task_id=task_id, status="processing",
                                  progress=result.info or {})

    if result.state == "SUCCESS":
        return TaskStatusResponse(task_id=task_id, status="success", result=result.result)

    if result.state == "FAILURE":
        return TaskStatusResponse(
            task_id=task_id, status="failed",
            error=str(result.info) if result.info else "Unknown error",
        )

    return TaskStatusResponse(task_id=task_id, status=result.state.lower(),
                              progress={"message": f"State: {result.state}"})


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/analyze", response_model=TaskSubmitResponse, summary="Full NER + Classification + QA")
async def fusion_analyze(request: FusionAnalyzeRequest):
    """
    Run the Attention Fusion model's three heads (NER, Classification, QA)
    on the provided transcript in a single Celery task.

    Poll `GET /fusion/task/{task_id}` for the result.
    """
    _check_model_ready()
    if not request.transcript.strip():
        raise HTTPException(status_code=400, detail="Transcript cannot be empty")
    try:
        return _submit(fusion_analyze_task, [request.transcript, request.threshold])
    except Exception as e:
        logger.error(f"Failed to submit fusion_analyze task: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit task")


@router.post("/ner", response_model=TaskSubmitResponse, summary="NER via fusion backbone")
async def fusion_ner(request: FusionNERRequest):
    """Extract named entities using the shared DistilBERT backbone."""
    _check_model_ready()
    try:
        return _submit(fusion_ner_task, [request.transcript])
    except Exception as e:
        logger.error(f"Failed to submit fusion_ner task: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit task")


@router.post("/classify", response_model=TaskSubmitResponse, summary="Classification via fusion backbone")
async def fusion_classify(request: FusionClassifyRequest):
    """Classify case category, sub-category, intervention, and priority."""
    _check_model_ready()
    try:
        return _submit(fusion_classify_task, [request.transcript])
    except Exception as e:
        logger.error(f"Failed to submit fusion_classify task: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit task")


@router.post("/qa", response_model=TaskSubmitResponse, summary="QA scoring via fusion backbone")
async def fusion_qa(request: FusionQARequest):
    """Score counsellor quality across 17 binary sub-metrics."""
    _check_model_ready()
    try:
        return _submit(fusion_qa_task, [request.transcript, request.threshold])
    except Exception as e:
        logger.error(f"Failed to submit fusion_qa task: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit task")


@router.get("/task/{task_id}", response_model=TaskStatusResponse, summary="Poll task result")
async def fusion_task_status(task_id: str):
    """
    Poll for the result of any fusion task (analyze / ner / classify / qa).

    States: pending → processing → success | failed
    """
    try:
        return _poll(task_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking task: {e}")


@router.get("/info", summary="Model load status")
async def fusion_info():
    """Return the current load status and metadata of the Attention Fusion model."""
    if is_api_server_mode():
        return {
            "status": "api_server_mode",
            "message": "Attention Fusion model is loaded on Celery workers",
            "model_info": {"mode": "api_server"},
        }
    from ..model_scripts.attention_fusion_model import attention_fusion_model
    if not attention_fusion_model.is_ready():
        return {
            "status": "not_ready",
            "message": "Attention Fusion model not loaded",
            "model_info": attention_fusion_model.get_model_info(),
        }
    return {
        "status": "ready",
        "model_info": attention_fusion_model.get_model_info(),
    }


@router.post("/demo", response_model=TaskSubmitResponse, summary="Demo with built-in transcript")
async def fusion_demo():
    """
    Run the full Attention Fusion pipeline on a built-in demo transcript.
    Useful for smoke-testing the endpoint without providing your own data.
    """
    _check_model_ready()
    try:
        return _submit(fusion_analyze_task, [DEMO_TRANSCRIPT, 0.5])
    except Exception as e:
        logger.error(f"Failed to submit fusion demo task: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit demo task")
