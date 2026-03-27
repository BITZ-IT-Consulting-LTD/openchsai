# API Reference

## Base URL
```
http://localhost:8125
```

## Authentication
- **Current**: No authentication (implement JWT as needed)
- **Planned**: JWT-based token authentication

## Async Pattern

All model inference endpoints are **asynchronous by default**. They return a `task_id` immediately, and results are retrieved by polling the corresponding task status endpoint.

```
POST /model/endpoint  →  { "task_id": "...", "status": "queued", "status_endpoint": "/model/task/{task_id}" }
GET  /model/task/{task_id}  →  { "status": "success", "result": { ... } }
```

**Task status values:**
- `queued` — Waiting to be picked up by a worker
- `pending` — Acknowledged, not yet started
- `success` — Completed successfully; `result` field is populated
- `failure` — Processing failed; `error` field has details

---

## Service Info

### App Info
**GET** `/info`

Returns application metadata and runtime mode.

```bash
curl http://localhost:8125/info
```

**Response:**
```json
{
  "app": {
    "name": "AI Pipeline",
    "version": "0.1.0",
    "site_id": "dev-site-001",
    "debug": true,
    "mode": "api_server"
  },
  "system": {
    "platform": "Linux-...",
    "cpu_count": 32,
    "memory_total": 33400012800,
    "memory_available": 21053788160,
    "memory_percent": 37.0
  },
  "gpu": {
    "gpu_available": true,
    "message": "CUDA available"
  }
}
```

---

## Audio Processing Endpoints

### 1. Process Audio (Complete Pipeline)
**POST** `/audio/process`

Process audio through the full AI pipeline: transcription → translation → NER → classification → summarization → QA scoring → insights.

**Request**:
```bash
curl -X POST \
  -F "audio=@call.wav" \
  -F "language=sw" \
  -F "include_translation=true" \
  -F "include_insights=true" \
  -F "background=true" \
  http://localhost:8125/audio/process
```

**Parameters**:
- `audio` (File, required): Audio file — WAV, MP3, FLAC, M4A, OGG, WebM. Max 100MB.
- `language` (String, optional): Language code, default: auto-detect
- `include_translation` (Boolean, optional): Include translation, default: true
- `include_insights` (Boolean, optional): Include NER, classification, QA, and insights, default: true
- `background` (Boolean, optional): Process asynchronously, default: true

**Response (202 Accepted):**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "message": "Audio processing started. Check status at /audio/task/{task_id}",
  "estimated_time": "15-45 seconds",
  "status_endpoint": "/audio/task/550e8400-e29b-41d4-a716-446655440000"
}
```

**Completed Task Result** (from `GET /audio/task/{task_id}`):
```json
{
  "audio_info": {
    "filename": "call.wav",
    "file_size_mb": 2.3,
    "language_specified": "sw",
    "processing_time": 23.4
  },
  "transcript": "Msichana mdogo ana miaka 12...",
  "translation": "A 12-year-old girl...",
  "entities": [
    {"text": "Maria", "label": "PER", "start": 0, "end": 5, "confidence": 0.91},
    {"text": "Nairobi", "label": "LOC", "start": 16, "end": 23, "confidence": 0.86}
  ],
  "classification": {
    "main_category": "Advice and Counselling",
    "sub_category": "Physical Abuse",
    "sub_category_2": "Physical Health",
    "intervention": "Referral",
    "priority": "1",
    "confidence_scores": {
      "main_category": 0.87,
      "sub_category": 0.72,
      "intervention": 0.74,
      "priority": 0.56
    }
  },
  "summary": "Emergency call regarding a 12-year-old girl experiencing abuse...",
  "qa_scores": {
    "evaluations": {
      "opening": [{"submetric": "Use of call opening phrase", "prediction": true, "score": "✓", "probability": 0.90}],
      "listening": [{"submetric": "Empathizes with the caller", "prediction": true, "score": "✓", "probability": 0.85}]
    }
  },
  "insights": {
    "risk_assessment": {"risk_level": "high", "priority": "urgent"},
    "key_information": {"main_category": "Advice and Counselling", "intervention_needed": "immediate"}
  },
  "pipeline_info": {
    "total_time": 23.4,
    "models_used": ["whisper", "translator", "ner", "classifier_model", "summarizer", "qa"]
  }
}
```

### 2. Get Task Status
**GET** `/audio/task/{task_id}`

Check the status and results of an audio processing task.

```bash
curl http://localhost:8125/audio/task/550e8400-e29b-41d4-a716-446655440000
```

**Response (in progress):**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "result": null,
  "error": null,
  "progress": {"message": "Task is queued"}
}
```

**Response (completed):**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "success",
  "result": { ... },
  "error": null,
  "progress": null
}
```

### 3. Cancel Task
**DELETE** `/audio/task/{task_id}`

Cancel an active task or delete task results.

```bash
curl -X DELETE http://localhost:8125/audio/task/550e8400-e29b-41d4-a716-446655440000
```

**Response:**
```json
{
  "status": "success",
  "message": "Task cancelled successfully",
  "task_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 4. Quick Audio Analysis
**POST** `/audio/analyze`

Faster analysis — transcription, classification, and summary only. No full translation or insights.

```bash
curl -X POST \
  -F "audio=@call.wav" \
  -F "language=sw" \
  http://localhost:8125/audio/analyze
```

**Parameters**: Same as `/audio/process`. Max file size: 50MB.

**Response (202 Accepted):**
```json
{
  "task_id": "analyze-abc123",
  "status": "queued",
  "message": "Quick analysis started",
  "estimated_time": "10-20 seconds",
  "status_endpoint": "/audio/task/analyze-abc123"
}
```

### 5. Get Active Tasks
**GET** `/audio/tasks/active`

Get list of all currently active audio processing tasks.

```bash
curl http://localhost:8125/audio/tasks/active
```

**Response:**
```json
{
  "active_tasks": [],
  "total_active": 0,
  "note": "Monitoring may be temporarily unavailable during heavy load"
}
```

### 6. Stream Audio Processing
**POST** `/audio/process-stream`

Process audio with real-time progress updates via Server-Sent Events (SSE).

```bash
curl -X POST \
  -F "audio=@call.wav" \
  -F "language=sw" \
  http://localhost:8125/audio/process-stream
```

**Response**: `text/event-stream`
```
event: transcription_progress
data: {"progress": 25, "status": "processing"}

event: transcription_complete
data: {"text": "Transcribed text...", "confidence": 0.95}

event: translation_complete
data: {"text": "Translated text..."}

event: classification_complete
data: {"category": "Advice and Counselling", "priority": "1"}

event: complete
data: {"status": "completed", "task_id": "550e8400-..."}
```

### 7. Real-Time Stream Processing
**POST** `/audio/process-stream-realtime`

Process audio with real-time streaming optimised for live call analysis.

```bash
curl -X POST \
  -F "audio=@chunk.wav" \
  http://localhost:8125/audio/process-stream-realtime
```

### 8. Get Queue Status
**GET** `/audio/queue/status`

```bash
curl http://localhost:8125/audio/queue/status
```

**Response:**
```json
{
  "status": "healthy",
  "workers": 1,
  "worker_info": [
    {
      "name": "worker@hostname",
      "status": "online",
      "total_tasks": {
        "process_audio_task": 122,
        "ner_extract_task": 2
      },
      "current_load": 0
    }
  ],
  "queue_stats": {
    "active_tasks": 0,
    "scheduled_tasks": 0,
    "reserved_tasks": 0,
    "total_pending": 0
  }
}
```

### 9. Worker Status
**GET** `/audio/workers/status`

Detailed Celery worker inspection including broker info and resource usage.

```bash
curl http://localhost:8125/audio/workers/status
```

**Response:**
```json
{
  "event_monitoring": {
    "workers": {},
    "total_workers": 0,
    "monitoring_status": "waiting_for_worker"
  },
  "celery_inspection": {
    "available": true,
    "stats": {
      "worker@hostname": {
        "total": {"process_audio_task": 122},
        "pid": 1,
        "uptime": 12750,
        "pool": {"implementation": "celery.concurrency.solo:TaskPool", "max-concurrency": 1}
      }
    },
    "active": {"worker@hostname": []}
  },
  "explanation": {
    "offline_during_processing": "Normal - workers can't respond to pings during GPU-intensive tasks"
  }
}
```

---

## Individual Model Endpoints

All model endpoints are asynchronous. Each returns a `task_id`. Poll the corresponding `/model/task/{task_id}` endpoint for results. Each model also has `/model/info` and `/model/demo` endpoints.

### Speech-to-Text (Whisper)

#### Transcribe Audio
**POST** `/whisper/transcribe`

```bash
curl -X POST \
  -F "audio=@call.wav" \
  -F "language=sw" \
  http://localhost:8125/whisper/transcribe
```

**Response (queued):**
```json
{
  "task_id": "abc123",
  "status": "queued",
  "message": "Transcription started. Check status at /whisper/task/{task_id}",
  "estimated_time": "5-20 seconds",
  "status_endpoint": "/whisper/task/abc123"
}
```

**Completed result** (from `GET /whisper/task/{task_id}`):
```json
{
  "task_id": "abc123",
  "status": "success",
  "result": {
    "transcript": "Msichana mdogo ana miaka 12...",
    "language": "sw",
    "confidence": 0.95,
    "duration": 120.5,
    "processing_time": 8.3,
    "model_info": {
      "model_type": "whisper",
      "hf_repo_id": "openchs/asr-whisper-largev2-v6",
      "loaded": true,
      "device": "cuda"
    }
  }
}
```

#### Get Supported Languages
**GET** `/whisper/languages`

```bash
curl http://localhost:8125/whisper/languages
```

**Response:**
```json
{
  "supported_languages": {
    "en": "English",
    "sw": "Swahili",
    "fr": "French",
    "es": "Spanish",
    "ar": "Arabic"
  },
  "total_supported": "99+ languages",
  "usage": "Pass language code in request: language='sw' for Swahili"
}
```

#### Whisper Model Info
**GET** `/whisper/info`

```bash
curl http://localhost:8125/whisper/info
```

#### Whisper Demo
**POST** `/whisper/demo`

Runs a built-in test audio sample through the model.

---

### Translation

#### Translate Text
**POST** `/translate/`

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"text": "Msichana mdogo ana matatizo", "source_language": "sw", "target_language": "en"}' \
  http://localhost:8125/translate/
```

**Response (queued):**
```json
{
  "task_id": "abc123",
  "status": "queued",
  "message": "Translation started. Check status at /translate/task/{task_id}",
  "estimated_time": "5-20 seconds",
  "status_endpoint": "/translate/task/abc123"
}
```

**Completed result** (from `GET /translate/task/{task_id}`):
```json
{
  "task_id": "abc123",
  "status": "success",
  "result": {
    "translated": "A young girl has problems",
    "processing_time": 0.76,
    "model_info": {
      "model_type": "translator",
      "hf_repo_id": "openchs/sw-en-opus-mt-mul-en-v1",
      "loaded": true,
      "device": "cuda"
    }
  }
}
```

#### Translation Model Info
**GET** `/translate/info`

#### Translation Demo
**POST** `/translate/demo`

---

### Named Entity Recognition

#### Extract Entities
**POST** `/ner/extract`

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"text": "Maria Wanjiku lives in Nairobi near Kenyatta Hospital."}' \
  http://localhost:8125/ner/extract
```

**Response (queued):**
```json
{
  "task_id": "abc123",
  "status": "queued",
  "message": "NER processing started. Check status at /ner/task/{task_id}",
  "estimated_time": "5-15 seconds",
  "status_endpoint": "/ner/task/abc123"
}
```

**Completed result** (from `GET /ner/task/{task_id}`):
```json
{
  "task_id": "abc123",
  "status": "success",
  "result": {
    "entities": [
      {"text": "Maria Wanjiku", "label": "PER", "start": 0, "end": 13, "confidence": 0.41},
      {"text": "Nairobi", "label": "LOC", "start": 22, "end": 30, "confidence": 0.86},
      {"text": "Kenyatta", "label": "LOC", "start": 35, "end": 44, "confidence": 0.30}
    ],
    "processing_time": 0.75,
    "model_info": {
      "model_type": "ner",
      "hf_repo_id": "openchs/ner_distillbert_v1",
      "loaded": true,
      "device": "cpu"
    }
  }
}
```

**Entity labels:** `PER` (person), `LOC` (location), `ORG` (organisation), `MISC` (miscellaneous)

#### NER Model Info
**GET** `/ner/info`

#### NER Demo
**POST** `/ner/demo`

---

### Case Classification

#### Classify Case
**POST** `/classifier/classify`

> **Note:** The request body uses `narrative`, not `text`.

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"narrative": "Child reports physical abuse from caregiver. Immediate danger.", "threshold": 0.5}' \
  http://localhost:8125/classifier/classify
```

**Response (queued):**
```json
{
  "task_id": "abc123",
  "status": "queued",
  "message": "Classification started. Check status at /classifier/task/{task_id}",
  "estimated_time": "10-30 seconds",
  "status_endpoint": "/classifier/task/abc123"
}
```

**Completed result** (from `GET /classifier/task/{task_id}`):
```json
{
  "task_id": "abc123",
  "status": "success",
  "result": {
    "main_category": "Advice and Counselling",
    "sub_category": "Physical Abuse",
    "sub_category_2": "Physical Health",
    "intervention": "Referral",
    "priority": "1",
    "confidence_scores": {
      "main_category": 0.51,
      "sub_category": 0.145,
      "sub_category_2": 0.134,
      "intervention": 0.736,
      "priority": 0.561
    },
    "chunks_processed": 1,
    "processing_time": 0.88,
    "model_info": {
      "model_type": "classifier",
      "hf_repo_id": "openchs/cls-gbv-distilbert-v1",
      "loaded": true,
      "device": "cuda",
      "details": {
        "categories": {"main": 7, "sub": 65, "intervention": 5, "priority": 3}
      }
    }
  }
}
```

#### Classifier Model Info
**GET** `/classifier/info`

#### Classifier Demo
**POST** `/classifier/demo`

---

### Text Summarization

#### Summarize Text
**POST** `/summarizer/summarize`

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"text": "Long transcript here...", "max_length": 150, "min_length": 50}' \
  http://localhost:8125/summarizer/summarize
```

**Response (queued):**
```json
{
  "task_id": "abc123",
  "status": "queued",
  "message": "Summarization started. Check status at /summarizer/task/{task_id}",
  "estimated_time": "10-30 seconds",
  "status_endpoint": "/summarizer/task/abc123"
}
```

**Completed result** (from `GET /summarizer/task/{task_id}`):
```json
{
  "task_id": "abc123",
  "status": "success",
  "result": {
    "summary": "A 12-year-old girl reported abuse from her caregiver in Nairobi...",
    "processing_time": 1.04,
    "model_info": {
      "model_type": "summarizer",
      "hf_repo_id": "openchs/sum-flan-t5-base-synthetic-v1",
      "loaded": true,
      "device": "cuda"
    }
  }
}
```

#### Summarizer Model Info
**GET** `/summarizer/info`

#### Summarizer Demo
**POST** `/summarizer/demo`

---

### Quality Assurance

#### Evaluate Call Quality
**POST** `/qa/evaluate`

Evaluate a call transcript against 17 quality sub-metrics across 6 dimensions: opening, listening, proactiveness, resolution, hold, and closing.

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"transcript": "Agent: Good afternoon, 116 helpline. Caller: My child is in danger.", "threshold": 0.5}' \
  http://localhost:8125/qa/evaluate
```

**Response (queued):**
```json
{
  "task_id": "abc123",
  "status": "queued",
  "message": "QA evaluation started. Check status at /qa/task/{task_id}",
  "estimated_time": "15-45 seconds",
  "status_endpoint": "/qa/task/abc123"
}
```

**Completed result** (from `GET /qa/task/{task_id}`):
```json
{
  "task_id": "abc123",
  "status": "success",
  "result": {
    "evaluations": {
      "opening": [
        {"submetric": "Use of call opening phrase", "prediction": true, "score": "✓", "probability": 0.90}
      ],
      "listening": [
        {"submetric": "Caller was not interrupted", "prediction": true, "score": "✓", "probability": 0.52},
        {"submetric": "Empathizes with the caller", "prediction": false, "score": "✗", "probability": 0.39},
        {"submetric": "Paraphrases or rephrases the issue", "prediction": false, "score": "✗", "probability": 0.22},
        {"submetric": "Uses 'please' and 'thank you'", "prediction": false, "score": "✗", "probability": 0.39},
        {"submetric": "Does not hesitate or sound unsure", "prediction": false, "score": "✗", "probability": 0.48}
      ],
      "proactiveness": [
        {"submetric": "Willing to solve extra issues", "prediction": false, "score": "✗", "probability": 0.23},
        {"submetric": "Confirms satisfaction with action points", "prediction": false, "score": "✗", "probability": 0.14},
        {"submetric": "Follows up on case updates", "prediction": false, "score": "✗", "probability": 0.12}
      ],
      "resolution": [
        {"submetric": "Gives accurate information", "prediction": false, "score": "✗", "probability": 0.42},
        {"submetric": "Correct language use", "prediction": true, "score": "✓", "probability": 0.69},
        {"submetric": "Consults if unsure", "prediction": false, "score": "✗", "probability": 0.27},
        {"submetric": "Follows correct steps", "prediction": false, "score": "✗", "probability": 0.44},
        {"submetric": "Explains solution process clearly", "prediction": false, "score": "✗", "probability": 0.31}
      ],
      "hold": [
        {"submetric": "Explains before placing on hold", "prediction": false, "score": "✗", "probability": 0.07},
        {"submetric": "Thanks caller for holding", "prediction": false, "score": "✗", "probability": 0.09}
      ],
      "closing": [
        {"submetric": "Proper call closing phrase used", "prediction": false, "score": "✗", "probability": 0.07}
      ]
    },
    "processing_time": 0.86,
    "model_info": {
      "model_type": "qa",
      "hf_repo_id": "openchs/qa-helpline-distilbert-v1",
      "loaded": true,
      "device": "cuda",
      "details": {
        "max_length": 512,
        "qa_heads_config": {"opening": 1, "listening": 5, "proactiveness": 3, "resolution": 5, "hold": 2, "closing": 1}
      }
    },
    "timestamp": "2026-02-12T11:52:12.169751"
  }
}
```

#### QA Model Info
**GET** `/qa/info`

```bash
curl http://localhost:8125/qa/info
```

**Response:**
```json
{
  "status": "api_server_mode",
  "message": "QA model loaded on Celery workers",
  "model_info": {"mode": "api_server"}
}
```

#### QA Demo
**POST** `/qa/demo`

Runs a canonical sample transcript through the model for testing.

```bash
curl -X POST http://localhost:8125/qa/demo
```

---

## Call Session Endpoints

Real-time call tracking and progressive analysis. Base path: `/api/v1/calls`

### Get All Active Calls
**GET** `/api/v1/calls/active`

Returns all calls currently tracked in the session store (both active and recently closed).

```bash
curl http://localhost:8125/api/v1/calls/active
```

**Response** (array):
```json
[
  {
    "call_id": "1770897267.45376",
    "start_time": "2026-02-12T11:51:02.360427",
    "last_activity": "2026-02-12T11:51:02.360427",
    "connection_info": {
      "client_addr": ["192.168.10.3", 57306],
      "temp_connection_id": "192.168.10.3:57306:115101",
      "start_time": "2026-02-12T11:51:02.360417"
    },
    "transcript_segments": [],
    "cumulative_transcript": "",
    "total_audio_duration": 0.0,
    "segment_count": 0,
    "status": "active",
    "processing_mode": "post_call",
    "processing_plan": {
      "mode": "post_call",
      "streaming_enabled": false,
      "postcall_enabled": true,
      "postcall_config": {
        "enable_insights": true,
        "enable_qa_scoring": true,
        "enable_summary": true,
        "processing_timeout": 300
      }
    }
  }
]
```

### Get Call Statistics
**GET** `/api/v1/calls/stats`

Summary stats across all sessions in the current store.

```bash
curl http://localhost:8125/api/v1/calls/stats
```

**Response:**
```json
{
  "active_sessions": 10,
  "total_audio_duration": 0.0,
  "total_segments": 0,
  "average_duration_per_session": 0.0,
  "session_list": ["1770897398.45425", "1770897454.45437"]
}
```

### Get Call Details
**GET** `/api/v1/calls/{call_id}`

```bash
curl http://localhost:8125/api/v1/calls/1770897267.45376
```

### Get Call Transcript
**GET** `/api/v1/calls/{call_id}/transcript`

```bash
curl "http://localhost:8125/api/v1/calls/1770897267.45376/transcript"
```

### Get Call Segments
**GET** `/api/v1/calls/{call_id}/segments`

Get transcript segments with timestamps.

```bash
curl http://localhost:8125/api/v1/calls/1770897267.45376/segments
```

### End Call Session
**POST** `/api/v1/calls/{call_id}/end`

Manually end a call and trigger post-call AI processing.

```bash
curl -X POST http://localhost:8125/api/v1/calls/1770897267.45376/end
```

### Export Call for AI Pipeline
**GET** `/api/v1/calls/{call_id}/export`

Export call data in a format suitable for feeding into the AI pipeline.

```bash
curl http://localhost:8125/api/v1/calls/1770897267.45376/export
```

### Trigger AI Pipeline
**POST** `/api/v1/calls/{call_id}/trigger-ai-pipeline`

Manually trigger the AI processing pipeline for a completed call.

```bash
curl -X POST http://localhost:8125/api/v1/calls/1770897267.45376/trigger-ai-pipeline
```

### Get Call Processing Status
**GET** `/api/v1/calls/{call_id}/processing`

Check the AI pipeline processing status for a specific call.

```bash
curl http://localhost:8125/api/v1/calls/1770897267.45376/processing
```

---

## Processing Management Endpoints

Configure and monitor processing modes. Base path: `/api/v1/processing`

### Processing Status
**GET** `/api/v1/processing/status`

Returns current processing configuration and capabilities.

```bash
curl http://localhost:8125/api/v1/processing/status
```

**Response:**
```json
{
  "status": "healthy",
  "system_capabilities": {
    "processing_modes": {
      "available_modes": ["realtime_only", "postcall_only", "hybrid", "adaptive"],
      "current_default": "hybrid",
      "realtime_enabled": false,
      "postcall_enabled": true
    },
    "audio_download": {
      "available_methods": ["scp", "http", "local", "disabled"],
      "current_method": "scp"
    }
  }
}
```

### Available Processing Modes
**GET** `/api/v1/processing/modes`

```bash
curl http://localhost:8125/api/v1/processing/modes
```

### Configure Processing
**POST** `/api/v1/processing/configure`

Update the active processing configuration.

```bash
curl -X POST http://localhost:8125/api/v1/processing/configure \
  -H "Content-Type: application/json" \
  -d '{"mode": "postcall_only"}'
```

### Create Processing Plan
**POST** `/api/v1/processing/plan`

Create a processing plan for a call based on its characteristics.

```bash
curl -X POST http://localhost:8125/api/v1/processing/plan \
  -H "Content-Type: application/json" \
  -d '{"call_id": "1770897267.45376", "language": "sw"}'
```

### Processing Statistics
**GET** `/api/v1/processing/statistics`

```bash
curl http://localhost:8125/api/v1/processing/statistics
```

### Test Processing Mode
**POST** `/api/v1/processing/test-mode/{mode}`

```bash
curl -X POST http://localhost:8125/api/v1/processing/test-mode/postcall_only
```

---

## Notification Endpoints

Manage and monitor outgoing notifications. Base path: `/api/v1/notifications`

### Notification Status
**GET** `/api/v1/notifications/status`

```bash
curl http://localhost:8125/api/v1/notifications/status
```

**Response:**
```json
{
  "notification_system": {
    "enabled": true,
    "mode": "results_only",
    "service_available": true,
    "statistics": {
      "total_considered": 0,
      "total_sent": 0,
      "total_filtered": 0
    },
    "available_modes": ["all", "results_only", "critical_only", "disabled"],
    "configuration": {
      "endpoint_url": "https://.../api/msg/",
      "timeout": 10,
      "max_retries": 3
    }
  }
}
```

### Available Notification Modes
**GET** `/api/v1/notifications/modes`

### Configure Notifications
**POST** `/api/v1/notifications/configure`

### Notification Statistics
**GET** `/api/v1/notifications/statistics`

### Reset Notification Statistics
**POST** `/api/v1/notifications/statistics/reset`

### Test Notification Filtering
**POST** `/api/v1/notifications/test`

### Notification Types
**GET** `/api/v1/notifications/types`

---

## Agent Feedback Endpoints

Allow agents to rate AI predictions for performance monitoring. Base path: `/api/v1/agent-feedback`

### Submit or Update Feedback
**POST** `/api/v1/agent-feedback/update`

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "call_id": "call_123456",
    "task": "classification",
    "feedback": 4,
    "reason": "Accurate main category, minor issue with sub-category"
  }' \
  http://localhost:8125/api/v1/agent-feedback/update
```

**Parameters:**
- `call_id` (string, required): Unique call identifier
- `task` (string, required): One of: `transcription`, `classification`, `ner`, `summarization`, `translation`, `qa`, `insights`
- `feedback` (integer, required): Rating 1 (poor) to 5 (excellent)
- `reason` (string, optional): Explanation for the rating

**Response (200 OK):**
```json
{
  "id": 1543,
  "call_id": "call_123456",
  "task": "classification",
  "prediction": {"main_category": "Advice and Counselling", "sub_category": "Physical Abuse", "priority": "1"},
  "feedback": 4,
  "reason": "Accurate main category, minor issue with sub-category",
  "created_at": "2026-01-20T10:30:00",
  "updated_at": "2026-01-20T10:35:00"
}
```

### Get Feedback for a Call
**GET** `/api/v1/agent-feedback/call/{call_id}`

```bash
curl http://localhost:8125/api/v1/agent-feedback/call/call_123456
```

**Query Parameters:**
- `task` (string, optional): Filter by task name

**Response:**
```json
[
  {
    "id": 1543,
    "call_id": "call_123456",
    "task": "classification",
    "feedback": 4,
    "reason": "Good overall accuracy",
    "created_at": "2026-01-20T10:30:00"
  }
]
```

### Get Feedback Statistics
**GET** `/api/v1/agent-feedback/statistics`

```bash
curl "http://localhost:8125/api/v1/agent-feedback/statistics?days=30"
```

**Query Parameters:**
- `task` (string, optional): Filter by task
- `days` (integer, optional): Days to look back, default: 30

**Response:**
```json
{
  "period_days": 30,
  "tasks": {
    "classification": {
      "total_predictions": 8471,
      "rated_predictions": 85,
      "rating_coverage": 1.0,
      "average_rating": 1.85,
      "min_rating": 1,
      "max_rating": 5
    },
    "transcription": {
      "total_predictions": 8471,
      "rated_predictions": 174,
      "rating_coverage": 2.05,
      "average_rating": 2.44,
      "min_rating": 1,
      "max_rating": 5
    },
    "translation": {
      "total_predictions": 8471,
      "rated_predictions": 117,
      "rating_coverage": 1.38,
      "average_rating": 2.39,
      "min_rating": 1,
      "max_rating": 5
    }
  }
}
```

### Feedback Health Check
**GET** `/api/v1/agent-feedback/health`

```bash
curl http://localhost:8125/api/v1/agent-feedback/health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "total_feedback_entries": 59303,
  "rated_entries": 564,
  "rating_coverage": 0.95,
  "timestamp": "2026-02-12T11:52:05.064738"
}
```

---

## Health & Status Endpoints

### Service Health
**GET** `/health/`

```bash
curl http://localhost:8125/health/
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-12T11:51:07.949899",
  "version": "0.1.0",
  "site_id": "dev-site-001"
}
```

### Detailed Health
**GET** `/health/detailed`

```bash
curl http://localhost:8125/health/detailed
```

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "issues": [],
  "system": {
    "cpu_count": 32,
    "memory_total": 33400012800,
    "memory_available": 21053788160,
    "memory_percent": 37.0,
    "disk_usage": 90.9
  },
  "gpu": {"gpu_available": true, "message": "CUDA available"},
  "queue": {"queue_size": 0, "max_queue_size": 100},
  "models": {
    "total": 6,
    "ready": 6,
    "implementable": 6,
    "implementable_models": ["whisper", "ner", "classifier_model", "translator", "summarizer", "qa"]
  }
}
```

### Model Status
**GET** `/health/models`

Check status of all ML models and Celery workers.

```bash
curl http://localhost:8125/health/models
```

**Response:**
```json
{
  "timestamp": "2026-02-12T11:51:14.317992",
  "mode": "api_server",
  "status": "unhealthy",
  "reason": "No Celery workers available",
  "celery_workers": [],
  "models": {}
}
```

> **Note:** `status: unhealthy` here means no workers are currently responding to inspection pings — this is normal when workers are processing GPU-intensive tasks.

### System Capabilities
**GET** `/health/capabilities`

```bash
curl http://localhost:8125/health/capabilities
```

**Response:**
```json
{
  "available_libraries": {
    "torch": "2.7.1+cu126",
    "transformers": "4.53.3",
    "spacy": "3.8.7",
    "librosa": "0.11.0"
  },
  "total_models": 6,
  "loaded_models": 0,
  "ready_for_implementation": 6,
  "ml_capabilities": {
    "gpu_processing": true,
    "transformer_models": true,
    "audio_processing": true,
    "nlp_processing": true
  }
}
```

### Resource Utilisation
**GET** `/health/resources`

```bash
curl http://localhost:8125/health/resources
```

**Response:**
```json
{
  "status": "healthy",
  "streaming_enabled": true,
  "resource_utilization": {
    "streaming": {"active_requests": 0, "max_slots": 2, "available_slots": 2, "utilization_pct": 0.0},
    "batch": {"active_requests": 0, "max_slots": 1, "available_slots": 1, "utilization_pct": 0.0}
  },
  "gpu_info": {"gpu_available": true}
}
```

### Celery Status
**GET** `/health/celery/status`

```bash
curl http://localhost:8125/health/celery/status
```

---

## Asterisk / Streaming Integration

### Asterisk TCP Status
**GET** `/asterisk/status`

Status of the TCP server that receives real-time audio from Asterisk.

```bash
curl http://localhost:8125/asterisk/status
```

**Response:**
```json
{
  "tcp_server": {
    "server_running": true,
    "active_calls": 9,
    "active_connections": 9,
    "call_sessions": {
      "1770885674.43098": {
        "audio_buffer_stats": {
          "buffer_size_bytes": 675840,
          "buffer_duration_seconds": 21.12,
          "chunks_received": 49374,
          "window_ready": false
        },
        "client_addr": "('192.168.10.3', 36656)",
        "session_status": "active"
      }
    },
    "transcription_method": "celery_workers",
    "tcp_port": 8300
  },
  "websocket_server": {
    "websocket_server_active": true,
    "active_connections": 0,
    "protocol": "websocket"
  }
}
```
