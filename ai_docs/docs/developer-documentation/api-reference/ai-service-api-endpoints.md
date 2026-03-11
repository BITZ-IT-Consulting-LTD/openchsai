# AI Service API Endpoints

## Base URL
```
http://localhost:8125
```

## Authentication
By default, AI service endpoints don't require authentication for internal use. For production deployments with external access, see [Authentication Guide](authentication.md).

---

## Audio Processing Endpoints

### Complete Audio Processing Pipeline
Process audio through full AI pipeline (transcription, translation, classification).

**Endpoint:** `POST /audio/process`

**Request:** Multipart form data
```
audio: <binary audio file>
language: "sw" (optional, default: auto-detect)
include_translation: "true" (optional)
include_classification: "true" (optional)
```

**Parameters:**
- `audio` (File, required): Audio file (WAV, MP3, FLAC, M4A, OGG, WebM). Max 100MB.
- `language` (String, optional): Language code, default: auto-detect
- `include_translation` (Boolean, optional): Include translation, default: true
- `include_insights` (Boolean, optional): Include risk insights, default: true
- `background` (Boolean, optional): Process asynchronously, default: true

**Example:**
```bash
curl -X POST http://localhost:8125/audio/process \
  -F "audio=@call_recording.wav" \
  -F "language=sw" \
  -F "include_translation=true" \
  -F "include_insights=true" \
  -F "background=true"
```

**Response (202 Accepted — Asynchronous):**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "message": "Audio processing started. Check status at /audio/task/{task_id}",
  "estimated_time": "15-45 seconds",
  "status_endpoint": "/audio/task/550e8400-e29b-41d4-a716-446655440000"
}
```

**Completed Task Result (from `/audio/task/{task_id}`):**
```json
{
  "audio_info": {
    "filename": "call_recording.wav",
    "file_size_mb": 2.3,
    "language_specified": "sw",
    "processing_time": 23.4
  },
  "transcript": "Msichana mdogo ana miaka kumi na mbili...",
  "translation": "A twelve-year-old girl...",
  "entities": {
    "PERSON": ["Maria Wanjiku"],
    "LOC": ["Nairobi", "Kibera"],
    "ORG": ["Kenyatta Hospital"],
    "DATE": ["2025-01-15"]
  },
  "classification": {
    "main_category": "child_protection",
    "sub_category": "physical_abuse",
    "priority": "high",
    "confidence": 0.94,
    "intervention": "immediate_action_required"
  },
  "qa_scores": {
    "empathy_score": 0.87,
    "professionalism_score": 0.92,
    "overall_quality": 0.86
  },
  "summary": "Emergency child protection case requiring immediate intervention",
  "insights": {
    "risk_assessment": {
      "risk_level": "high",
      "urgency": "immediate",
      "priority": "urgent",
      "confidence": 0.94
    }
  }
}
```

---

### Streaming Audio Processing
Process audio with real-time progress updates via Server-Sent Events (SSE).

**Endpoint:** `POST /audio/process-stream`

**Request:** Same multipart form data as `/audio/process`

**Example:**
```bash
curl -X POST http://localhost:8125/audio/process-stream \
  -F "audio=@call_recording.wav" \
  -F "language=sw"
```

**Response:** `text/event-stream` (Server-Sent Events)
```
event: transcription_progress
data: {"progress": 25, "status": "processing"}

event: transcription_complete
data: {"text": "Transcribed text...", "confidence": 0.95}

event: translation_progress
data: {"progress": 50, "status": "translating"}

event: translation_complete
data: {"text": "Translated text..."}

event: classification_complete
data: {"category": "child_protection", "risk_level": "high"}

event: complete
data: {"status": "completed", "task_id": "550e8400-..."}
```

---

### Quick Audio Analysis
Faster analysis with transcription, classification, and summary — without full translation or detailed insights.

**Endpoint:** `POST /audio/analyze`

**Parameters:**
- `audio` (File, required): Audio file. Max 50MB.
- `language` (String, optional): Language code or `auto`
- `background` (Boolean, optional): Process asynchronously, default: true

**Example:**
```bash
curl -X POST http://localhost:8125/audio/analyze \
  -F "audio=@call_recording.wav" \
  -F "language=sw"
```

**Response (202 Accepted — Asynchronous):**
```json
{
  "task_id": "analyze-abc123",
  "status": "queued",
  "message": "Quick analysis started",
  "estimated_time": "10-20 seconds",
  "status_endpoint": "/audio/task/analyze-abc123"
}
```

**Completed Result:**
```json
{
  "transcript": "Brief transcript...",
  "summary": "Brief summary of the content...",
  "main_category": "child_protection",
  "priority": "high",
  "risk_level": "medium",
  "processing_time": 12.5
}
```

---

### Check Processing Status
Check status of async audio processing task.

**Endpoint:** `GET /audio/task/{task_id}`

**Example:**
```bash
curl http://localhost:8125/audio/task/550e8400-e29b-41d4-a716-446655440000
```

**Response:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress": 0.65,
  "current_step": "Extracting entities...",
  "results": null,
  "created_at": "2024-01-19T10:30:00Z",
  "completed_at": null
}
```

**Status values:**
- `queued` - Waiting in queue
- `processing` - Currently processing
- `completed` - Finished successfully
- `failed` - Processing failed

---

### Get Active Tasks
Get list of all currently active audio processing tasks.

**Endpoint:** `GET /audio/tasks/active`

**Query Parameters:**
- `limit` (optional): Maximum number of tasks to return, default: 50
- `status` (optional): Filter by status (`processing`, `queued`)

**Example:**
```bash
curl http://localhost:8125/audio/tasks/active?limit=10
```

**Response:**
```json
{
  "status": "success",
  "active_tasks": [
    {
      "task_id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "processing",
      "progress": 0.65,
      "current_step": "Extracting entities...",
      "filename": "call.wav",
      "created_at": "2024-01-19T10:30:00Z",
      "elapsed_time": 12.5
    }
  ],
  "total_active": 1,
  "queue_length": 0
}
```

---

### Cancel Task
Cancel an active task or delete task results.

**Endpoint:** `DELETE /audio/task/{task_id}`

**Example:**
```bash
curl -X DELETE http://localhost:8125/audio/task/550e8400-e29b-41d4-a716-446655440000
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Task cancelled successfully",
  "task_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

## Transcription Endpoints

### Transcribe Audio
Convert speech to text using Whisper.

**Endpoint:** `POST /whisper/transcribe`

**Request:** Multipart form data
```
audio: <binary audio file>
language: "sw" (optional)
task: "transcribe" (or "translate" for translate-to-English)
```

**Example:**
```bash
curl -X POST http://localhost:8125/whisper/transcribe \
  -F "audio=@recording.wav" \
  -F "language=sw" \
  -F "task=transcribe"
```

**Response:**
```json
{
  "status": "success",
  "transcript": "Msichana mdogo ana miaka kumi na mbili, yupo katika hatari...",
  "language": "sw",
  "confidence": 0.94,
  "segments": [
    {
      "id": 0,
      "start": 0.0,
      "end": 5.2,
      "text": "Msichana mdogo ana miaka kumi na mbili",
      "confidence": 0.95
    }
  ],
  "duration": 127.3,
  "processing_time": 8.4
}
```

---

### Transcribe with Timestamps
Get detailed word-level timestamps.

**Endpoint:** `POST /whisper/transcribe-detailed`

**Request:** Same as `/whisper/transcribe` plus:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audio` | file | Yes | Audio file |
| `language` | string | No | Language code |
| `word_timestamps` | boolean | No | Enable word-level timestamps, default: false |

**Example:**
```bash
curl -X POST http://localhost:8125/whisper/transcribe-detailed \
  -F "audio=@recording.wav" \
  -F "language=sw" \
  -F "word_timestamps=true"
```

**Response:**
```json
{
  "status": "success",
  "text": "Full transcription...",
  "words": [
    {
      "word": "Msichana",
      "start": 0.0,
      "end": 0.8,
      "confidence": 0.96
    },
    {
      "word": "mdogo",
      "start": 0.9,
      "end": 1.3,
      "confidence": 0.94
    }
  ],
  "processing_time": 9.1
}
```

---

## Translation Endpoints

### Translate Text
Translate between Swahili and English.

**Endpoint:** `POST /translate/`

**Request:**
```json
{
  "text": "Msichana mdogo ana miaka kumi na mbili",
  "source_language": "sw",
  "target_language": "en"
}
```

**Example:**
```bash
curl -X POST http://localhost:8125/translate/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Msichana mdogo ana miaka kumi na mbili", "source_language": "sw", "target_language": "en"}'
```

**Response:**
```json
{
  "status": "success",
  "original_text": "Msichana mdogo ana miaka kumi na mbili",
  "translated_text": "A young girl is twelve years old",
  "source_language": "sw",
  "target_language": "en",
  "confidence": 0.92
}
```

---

### Batch Translation
Translate multiple texts at once.

**Endpoint:** `POST /translate/batch`

**Request:**
```json
{
  "texts": [
    "Msichana mdogo ana hatari",
    "Anahitaji msaada haraka"
  ],
  "source_language": "sw",
  "target_language": "en"
}
```

**Example:**
```bash
curl -X POST http://localhost:8125/translate/batch \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Msichana mdogo ana hatari", "Anahitaji msaada haraka"], "source_language": "sw", "target_language": "en"}'
```

**Response:**
```json
{
  "status": "success",
  "translations": [
    {
      "original": "Msichana mdogo ana hatari",
      "translated": "Young girl in danger",
      "confidence": 0.93
    },
    {
      "original": "Anahitaji msaada haraka",
      "translated": "Needs help urgently",
      "confidence": 0.95
    }
  ]
}
```

---

## NLP Analysis Endpoints

### Named Entity Recognition
Extract entities from text.

**Endpoint:** `POST /ner/extract`

**Request:**
```json
{
  "text": "Maria Wanjiku lives in Nairobi near Kenyatta Hospital. She is 12 years old."
}
```

**Example:**
```bash
curl -X POST http://localhost:8125/ner/extract \
  -H "Content-Type: application/json" \
  -d '{"text": "Maria Wanjiku lives in Nairobi near Kenyatta Hospital. She is 12 years old."}'
```

**Response:**
```json
{
  "status": "success",
  "entities": {
    "PERSON": [{"text": "Maria Wanjiku", "start": 0, "end": 13}],
    "LOC": [{"text": "Nairobi", "start": 23, "end": 30}],
    "ORG": [{"text": "Kenyatta Hospital", "start": 36, "end": 53}]
  },
  "entity_details": [
    {
      "text": "Maria Wanjiku",
      "label": "PERSON",
      "start": 0,
      "end": 13,
      "confidence": 0.99
    },
    {
      "text": "Nairobi",
      "label": "LOC",
      "start": 23,
      "end": 30,
      "confidence": 0.98
    }
  ]
}
```

---

### Text Classification
Classify case category and urgency.

**Endpoint:** `POST /classifier/classify`

**Request:**
```json
{
  "text": "Child reports physical abuse from caregiver. Immediate danger.",
  "threshold": 0.5
}
```

**Example:**
```bash
curl -X POST http://localhost:8125/classifier/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "Child reports physical abuse from caregiver. Immediate danger.", "threshold": 0.5}'
```

**Response:**
```json
{
  "status": "success",
  "classification": {
    "main_category": "child_protection",
    "main_category_confidence": 0.96,
    "sub_category": "physical_abuse",
    "priority": "critical",
    "intervention_type": "immediate_intervention"
  }
}
```

---

### Text Summarization
Generate summary of case details.

**Endpoint:** `POST /summarizer/summarize`

**Request:**
```json
{
  "text": "Long case description with multiple paragraphs...",
  "max_length": 150,
  "min_length": 50
}
```

**Example:**
```bash
curl -X POST http://localhost:8125/summarizer/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Long transcript here...", "max_length": 150, "min_length": 50}'
```

**Response:**
```json
{
  "status": "success",
  "summary": "12-year-old girl experiencing abuse. Immediate intervention required. Family support needed.",
  "summary_length": 82,
  "compression_ratio": 0.17
}
```

---

### Quality Assurance Scoring
Evaluate helpline call quality across standardized metrics.

**Endpoint:** `POST /qa/evaluate`

**Request:**
```json
{
  "transcript": "Agent: Good afternoon, this is the 116 helpline...",
  "threshold": 0.5,
  "return_raw": false
}
```

**Parameters:**
- `transcript` (string, required): Call transcript text
- `threshold` (float, optional): Classification threshold, default: 0.5
- `return_raw` (boolean, optional): Include raw probability scores, default: false

**Example:**
```bash
curl -X POST http://localhost:8125/qa/evaluate \
  -H "Content-Type: application/json" \
  -d '{"transcript": "Agent: Good afternoon...", "threshold": 0.5}'
```

**Response:**
```json
{
  "status": "success",
  "evaluations": {
    "opening": [
      {"metric": "used_call_protocol", "prediction": true, "passed": true, "score": 0.87}
    ],
    "listening": [
      {"metric": "active_listening", "prediction": true, "passed": true, "score": 0.92}
    ],
    "closing": [
      {"metric": "proper_closure", "prediction": true, "passed": true, "score": 0.95}
    ]
  },
  "processing_time": 0.43,
  "model_info": {
    "model_path": "openchs/qa-helpline-distilbert-v1",
    "device": "cuda"
  },
  "timestamp": "2026-01-20T10:30:00Z"
}
```

---

### QA Model Info
Get live model status and metadata.

**Endpoint:** `GET /qa/info`

**Example:**
```bash
curl http://localhost:8125/qa/info
```

**Response:**
```json
{
  "status": "success",
  "model": "openchs/qa-helpline-distilbert-v1",
  "loaded": true,
  "device": "cuda",
  "load_time_seconds": 4.2,
  "max_input_length": 512,
  "metrics_evaluated": 17
}
```

---

### QA Demo
Run a sample transcript through the QA model for testing.

**Endpoint:** `POST /qa/demo`

**Example:**
```bash
curl -X POST http://localhost:8125/qa/demo
```

**Response:** Same structure as `/qa/evaluate` using a canonical sample transcript.

---

## System Monitoring Endpoints

### Health Check
Basic health check.

**Endpoint:** `GET /health`

**Example:**
```bash
curl http://localhost:8125/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-26T14:30:00Z"
}
```

---

### Detailed Health Check
Comprehensive system status.

**Endpoint:** `GET /health/detailed`

**Example:**
```bash
curl http://localhost:8125/health/detailed
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-26T14:30:00Z",
  "components": {
    "api": {
      "status": "healthy",
      "uptime_seconds": 86400
    },
    "redis": {
      "status": "healthy",
      "ping_response_ms": 1.2
    },
    "gpu": {
      "status": "healthy",
      "available": true,
      "memory_used_gb": 8.2,
      "memory_total_gb": 16.0
    },
    "models": {
      "whisper": "loaded",
      "translator": "loaded",
      "ner": "loaded",
      "classifier": "loaded",
      "summarizer": "loaded"
    }
  },
  "performance": {
    "avg_response_time_ms": 234,
    "requests_per_minute": 12,
    "success_rate": 0.98
  }
}
```

---

### Model Status
Check AI model loading status.

**Endpoint:** `GET /health/models`

**Example:**
```bash
curl http://localhost:8125/health/models
```

**Response:**
```json
{
  "status": "success",
  "models": {
    "whisper": "loaded",
    "translator": "loaded",
    "ner": "loaded",
    "classifier": "loaded",
    "summarizer": "loaded"
  }
}
```

---

### Queue Status
Check processing queue status.

**Endpoint:** `GET /audio/queue/status`

**Example:**
```bash
curl http://localhost:8125/audio/queue/status
```

**Response:**
```json
{
  "status": "healthy",
  "queue": {
    "total_tasks": 5,
    "queued": 3,
    "processing": 2,
    "completed_today": 245,
    "failed_today": 2,
    "average_wait_time": 8.5,
    "average_processing_time": 12.3
  },
  "workers": {
    "active_workers": 4,
    "idle_workers": 2,
    "total_capacity": 6
  }
}
```

---

### Worker Status
Check Celery worker status.

**Endpoint:** `GET /audio/workers/status`

**Example:**
```bash
curl http://localhost:8125/audio/workers/status
```

**Response:**
```json
{
  "workers": {
    "celery@worker1": {
      "status": "online",
      "active_tasks": 1,
      "processed_tasks": 523,
      "failed_tasks": 7,
      "pool_size": 1
    }
  },
  "total_workers": 1,
  "total_active_tasks": 1,
  "queue_length": 5
}
```

---

## Utility Endpoints

### Get Available Models
List all available AI models.

**Endpoint:** `GET /models`

**Example:**
```bash
curl http://localhost:8125/models
```

**Response:**
```json
{
  "models": [
    {
      "id": "whisper-large-v3-turbo",
      "name": "Whisper Large V3 Turbo",
      "type": "transcription",
      "languages": 99,
      "status": "available"
    },
    {
      "id": "sw-en-translation",
      "name": "Swahili-English Translation",
      "type": "translation",
      "status": "available"
    }
  ]
}
```

---

### Get Supported Languages
List supported transcription languages.

**Endpoint:** `GET /languages`

**Example:**
```bash
curl http://localhost:8125/languages
```

**Response:**
```json
{
  "languages": [
    {
      "code": "en",
      "name": "English",
      "native_name": "English",
      "transcription": true,
      "translation": true
    },
    {
      "code": "sw",
      "name": "Swahili",
      "native_name": "Kiswahili",
      "transcription": true,
      "translation": true
    }
  ],
  "total_count": 99
}
```

---

## Call Session Endpoints

Real-time call tracking and progressive analysis for live helpline calls.

**Base Path:** `/api/v1/calls`

### Get All Active Calls
**Endpoint:** `GET /api/v1/calls/active`

**Example:**
```bash
curl http://localhost:8125/api/v1/calls/active
```

**Response:**
```json
{
  "status": "success",
  "active_calls": [
    {
      "call_id": "1705669200.1",
      "caller_id": "+254712345678",
      "start_time": "2026-01-20T10:30:00Z",
      "last_activity": "2026-01-20T10:34:00Z",
      "duration": 245,
      "status": "in_progress",
      "segment_count": 12
    }
  ],
  "total": 1
}
```

---

### Get Call Details
**Endpoint:** `GET /api/v1/calls/{call_id}`

**Example:**
```bash
curl http://localhost:8125/api/v1/calls/1705669200.1
```

**Response:**
```json
{
  "status": "success",
  "call": {
    "call_id": "1705669200.1",
    "caller_id": "+254712345678",
    "start_time": "2026-01-20T10:30:00Z",
    "end_time": "2026-01-20T10:35:00Z",
    "duration": 300,
    "transcript": "...",
    "translation": "...",
    "classification": {},
    "entities": {}
  }
}
```

---

### Get Call Transcript
Get the full transcript for a call, optionally with segments.

**Endpoint:** `GET /api/v1/calls/{call_id}/transcript`

**Query Parameters:**
- `include_segments` (boolean, optional): Include timestamped segments, default: false

**Example:**
```bash
curl "http://localhost:8125/api/v1/calls/1705669200.1/transcript?include_segments=true"
```

---

### Get Call Segments
Get transcript segments with speaker diarization and timestamps.

**Endpoint:** `GET /api/v1/calls/{call_id}/segments`

**Example:**
```bash
curl http://localhost:8125/api/v1/calls/1705669200.1/segments
```

**Response:**
```json
{
  "status": "success",
  "segments": [
    {
      "segment_id": 1,
      "start_time": 0.0,
      "end_time": 5.2,
      "text": "Habari, hii ni simu ya dharura...",
      "translation": "Hello, this is an emergency call...",
      "speaker": "caller"
    }
  ]
}
```

---

### Get Progressive Analysis
Get real-time progressive AI analysis for an active call.

**Endpoint:** `GET /api/v1/calls/{call_id}/progressive-analysis`

**Example:**
```bash
curl http://localhost:8125/api/v1/calls/1705669200.1/progressive-analysis
```

**Response:**
```json
{
  "status": "success",
  "call_id": "1705669200.1",
  "analysis": {
    "current_classification": {
      "main_category": "child_protection",
      "confidence": 0.87,
      "updated_at": "2026-01-20T10:34:15Z"
    },
    "entities_found": {
      "PERSON": ["Maria"],
      "LOC": ["Nairobi"]
    },
    "qa_live_scores": {
      "empathy_score": 0.85,
      "professionalism_score": 0.91
    }
  }
}
```

---

### Get Classification Evolution
Track how call classification changes throughout the conversation.

**Endpoint:** `GET /api/v1/calls/{call_id}/classification-evolution`

**Example:**
```bash
curl http://localhost:8125/api/v1/calls/1705669200.1/classification-evolution
```

**Response:**
```json
{
  "status": "success",
  "call_id": "1705669200.1",
  "evolution": [
    {
      "timestamp": "2026-01-20T10:30:15Z",
      "segment": 1,
      "classification": {"main_category": "unknown", "confidence": 0.4}
    },
    {
      "timestamp": "2026-01-20T10:31:00Z",
      "segment": 4,
      "classification": {"main_category": "child_protection", "confidence": 0.82}
    }
  ]
}
```

---

### End Call Session
Manually end a call session and trigger post-call processing.

**Endpoint:** `POST /api/v1/calls/{call_id}/end`

**Example:**
```bash
curl -X POST http://localhost:8125/api/v1/calls/1705669200.1/end
```

**Response:**
```json
{
  "status": "success",
  "message": "Call session ended. Post-call processing triggered.",
  "call_id": "1705669200.1",
  "task_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

## Agent Feedback Endpoints

Allow agents to rate and provide feedback on AI model predictions for performance monitoring and fine-tuning.

**Base Path:** `/api/v1/agent-feedback`

### Submit or Update Feedback
**Endpoint:** `POST /api/v1/agent-feedback/update`

**Request Body:**
```json
{
  "call_id": "call_123456",
  "task": "classification",
  "feedback": 4,
  "reason": "Accurate main category, minor issue with sub-category"
}
```

**Parameters:**
- `call_id` (string, required): Unique call identifier
- `task` (string, required): One of: `transcription`, `classification`, `ner`, `summarization`, `translation`, `qa`
- `feedback` (integer, required): Rating from 1 (poor) to 5 (excellent)
- `reason` (string, optional): Explanation for the rating

**Example:**
```bash
curl -X POST http://localhost:8125/api/v1/agent-feedback/update \
  -H "Content-Type: application/json" \
  -d '{
    "call_id": "call_123456",
    "task": "classification",
    "feedback": 4,
    "reason": "Accurate main category, minor issue with sub-category"
  }'
```

**Response (200 OK):**
```json
{
  "id": 1543,
  "call_id": "call_123456",
  "task": "classification",
  "prediction": {
    "main_category": "child_protection",
    "sub_category": "physical_abuse",
    "priority": "high"
  },
  "feedback": 4,
  "reason": "Accurate main category, minor issue with sub-category",
  "created_at": "2026-01-20T10:30:00",
  "updated_at": "2026-01-20T10:35:00"
}
```

---

### Get Feedback for a Call
**Endpoint:** `GET /api/v1/agent-feedback/call/{call_id}`

**Query Parameters:**
- `task` (string, optional): Filter by specific task

**Example:**
```bash
curl http://localhost:8125/api/v1/agent-feedback/call/call_123456
```

**Response (200 OK):**
```json
[
  {
    "id": 1543,
    "call_id": "call_123456",
    "task": "classification",
    "feedback": 4,
    "reason": "Good overall accuracy",
    "created_at": "2026-01-20T10:30:00"
  },
  {
    "id": 1544,
    "call_id": "call_123456",
    "task": "ner",
    "feedback": 5,
    "reason": "All entities correctly identified",
    "created_at": "2026-01-20T10:30:05"
  }
]
```

---

### Get Feedback Statistics
**Endpoint:** `GET /api/v1/agent-feedback/statistics`

**Query Parameters:**
- `task` (string, optional): Filter by specific task
- `days` (integer, optional): Number of days to look back, default: 30

**Example:**
```bash
curl "http://localhost:8125/api/v1/agent-feedback/statistics?days=30"
```

**Response (200 OK):**
```json
{
  "period_days": 30,
  "tasks": {
    "classification": {
      "total_predictions": 358,
      "rated_predictions": 42,
      "rating_coverage": 0.12,
      "average_rating": 4.1,
      "min_rating": 2,
      "max_rating": 5
    },
    "transcription": {
      "total_predictions": 358,
      "rated_predictions": 28,
      "rating_coverage": 0.08,
      "average_rating": 3.9,
      "min_rating": 3,
      "max_rating": 5
    }
  }
}
```

---

### Agent Feedback Health Check
**Endpoint:** `GET /api/v1/agent-feedback/health`

**Example:**
```bash
curl http://localhost:8125/api/v1/agent-feedback/health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2026-01-20T10:30:00Z"
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE",
  "timestamp": "2025-09-26T14:30:00Z"
}
```

**Common Error Codes:**
- `INVALID_AUDIO_FORMAT` (400) - Audio file format not supported
- `FILE_TOO_LARGE` (413) - Audio file exceeds size limit
- `PROCESSING_FAILED` (500) - AI processing failed
- `MODEL_NOT_LOADED` (503) - Required model not available
- `QUEUE_FULL` (429) - Processing queue at capacity

---

## Rate Limiting

See [API Rate Limiting](api-rate-limiting-throttling.md) for details.

**Default Limits:**
- 50 requests per hour per IP
- 10 concurrent processing tasks
- Maximum file size: 100 MB

---

## Examples

### Complete Workflow Example

```python
import requests
import time

BASE_URL = "http://localhost:8125"

# Submit audio for async processing
with open('call_recording.wav', 'rb') as audio:
    response = requests.post(
        f'{BASE_URL}/audio/process',
        files={'audio': audio},
        data={
            'language': 'sw',
            'include_translation': 'true',
            'include_insights': 'true',
            'background': 'true'
        }
    )

task = response.json()
task_id = task['task_id']
print(f"Task submitted: {task_id}")

# Poll for completion
while True:
    status_response = requests.get(f'{BASE_URL}/audio/task/{task_id}')
    status = status_response.json()
    if status['status'] == 'completed':
        result = status['results']
        break
    elif status['status'] == 'failed':
        raise Exception("Processing failed")
    time.sleep(2)

# Extract results
transcript = result['transcript']
translation = result['translation']
risk_level = result['classification']['priority']

print(f"Risk Level: {risk_level}")
print(f"Transcript: {transcript}")
print(f"Translation: {translation}")

# Additional NER analysis
entities_response = requests.post(
    f'{BASE_URL}/ner/extract',
    json={'text': translation}
)

entities = entities_response.json()['entities']
print(f"People mentioned: {entities.get('PERSON', [])}")
print(f"Locations: {entities.get('LOC', [])}")
```

---

## Performance Tips

1. **Use appropriate endpoints:**
   - `/audio/analyze` for quick results
   - `/audio/process` for comprehensive analysis
   - `/audio/process-stream` for real-time updates

2. **Batch operations:**
   - Use `/translate/batch` for multiple texts
   - Process multiple files asynchronously

3. **Optimize audio files:**
   - Convert to WAV/MP3 before upload
   - Compress large files
   - Trim silence from recordings

4. **Monitor queue status:**
   - Check `/audio/queue/status` before submitting
   - Implement retry logic for queue-full errors

5. **Agent feedback:**
   - Submit feedback after each processed call using `/api/v1/agent-feedback/update`
   - Monitor model quality trends via `/api/v1/agent-feedback/statistics`
