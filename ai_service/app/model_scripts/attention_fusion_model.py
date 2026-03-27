"""
Attention Fusion Multi-Task NLP Model — Service Wrapper

Loads the trained AttentionFusionModel checkpoint and provides three
inference methods that share a single DistilBERT forward pass:

  - predict_ner(text)            -> list of {token, label} dicts (non-O only)
  - predict_classification(text) -> {main_category, sub_category, intervention, priority}
  - predict_qa(text, threshold)  -> {opening:[...], listening:[...], ...}
  - predict_all(text, threshold) -> all three results combined
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

# ── PyTorch / Transformers are optional; model_loader checks availability ──
try:
    import torch
    import torch.nn as nn
    from transformers import AutoTokenizer, DistilBertModel
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    logger.warning("PyTorch / Transformers not available — AttentionFusionModel disabled")


if TORCH_AVAILABLE:

    class TaskAttentionPooling(nn.Module):
        """Per-task learned weighted sum over token positions."""

        def __init__(self, hidden_dim: int):
            super().__init__()
            self.attention = nn.Linear(hidden_dim, 1, bias=False)

        def forward(self, hidden_states: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
            scores = self.attention(hidden_states)                        # [B, L, 1]
            padding_mask = (attention_mask == 0).unsqueeze(-1)           # [B, L, 1]
            scores = scores.masked_fill(padding_mask, float("-inf"))
            weights = torch.softmax(scores, dim=1)                       # [B, L, 1]
            return (weights * hidden_states).sum(dim=1)                  # [B, H]


    class AttentionFusionModel(nn.Module):
        """
        Single DistilBERT backbone with three task-specific heads:
          ner  → per-token classifier (10 labels)
          cls  → 4 classification heads via TaskAttentionPooling
          qa   → 6 binary heads via TaskAttentionPooling
        """

        DEFAULT_QA_HEADS = {
            "opening": 1, "listening": 5, "proactiveness": 3,
            "resolution": 5, "hold": 2, "closing": 1,
        }

        def __init__(
            self,
            backbone_name: str = "distilbert-base-cased",
            dropout: float = 0.1,
            num_ner_labels: int = 10,
            num_main_cat: int = 8,
            num_sub_cat: int = 77,
            num_intervention: int = 16,
            num_priority: int = 3,
            qa_heads_config: Optional[Dict[str, int]] = None,
        ):
            super().__init__()
            if qa_heads_config is None:
                qa_heads_config = self.DEFAULT_QA_HEADS

            self.backbone = DistilBertModel.from_pretrained(backbone_name)
            hidden_dim = self.backbone.config.dim  # 768

            self.dropout = nn.Dropout(dropout)

            # NER head (token-level)
            self.ner_transform = nn.Sequential(
                nn.Linear(hidden_dim, hidden_dim), nn.GELU(), nn.Dropout(dropout)
            )
            self.ner_classifier = nn.Linear(hidden_dim, num_ner_labels)

            # Classification head (sentence-level)
            self.cls_attention = TaskAttentionPooling(hidden_dim)
            self.cls_main = nn.Linear(hidden_dim, num_main_cat)
            self.cls_sub = nn.Linear(hidden_dim, num_sub_cat)
            self.cls_intervention = nn.Linear(hidden_dim, num_intervention)
            self.cls_priority = nn.Linear(hidden_dim, num_priority)

            # QA head (sentence-level)
            self.qa_attention = TaskAttentionPooling(hidden_dim)
            self.qa_heads = nn.ModuleDict(
                {head: nn.Linear(hidden_dim, size) for head, size in qa_heads_config.items()}
            )

        def forward(self, input_ids, attention_mask, task: str, labels=None) -> dict:
            backbone_out = self.backbone(input_ids=input_ids, attention_mask=attention_mask)
            hidden_states = backbone_out.last_hidden_state  # [B, L, 768]

            if task == "ner":
                x = self.ner_transform(hidden_states)
                logits = self.ner_classifier(x)
                return {"logits": logits, "task": "ner"}

            elif task == "cls":
                pooled = self.dropout(self.cls_attention(hidden_states, attention_mask))
                logits = {
                    "main": self.cls_main(pooled),
                    "sub": self.cls_sub(pooled),
                    "intervention": self.cls_intervention(pooled),
                    "priority": self.cls_priority(pooled),
                }
                return {"logits": logits, "task": "cls"}

            elif task == "qa":
                pooled = self.dropout(self.qa_attention(hidden_states, attention_mask))
                logits = {head: layer(pooled) for head, layer in self.qa_heads.items()}
                return {"logits": logits, "task": "qa"}

            else:
                raise ValueError(f"Unknown task '{task}'. Choose from: ner, cls, qa")



# QA sub-metric labels (for human-readable output)


QA_SUBMETRIC_LABELS = {
    "opening": ["Use of call opening phrase"],
    "listening": [
        "Caller was not interrupted",
        "Empathizes with the caller",
        "Paraphrases or rephrases the issue",
        "Uses 'please' and 'thank you'",
        "Does not hesitate or sound unsure",
    ],
    "proactiveness": [
        "Willing to solve extra issues",
        "Confirms satisfaction with action points",
        "Follows up on case updates",
    ],
    "resolution": [
        "Gives accurate information",
        "Correct language use",
        "Consults if unsure",
        "Follows correct steps",
        "Explains solution process clearly",
    ],
    "hold": ["Explains before placing on hold", "Thanks caller for holding"],
    "closing": ["Proper call closing phrase used"],
}


# Service wrapper (matches the pattern of QAModel / ClassifierModel)

class AttentionFusionModelService:
    """
    Service wrapper that loads the trained checkpoint and exposes
    predict_ner / predict_classification / predict_qa / predict_all.
    """

    def __init__(self):
        from ..config.settings import settings

        self.settings = settings
        self.hf_repo = getattr(settings, "hf_attention_fusion_model", "Rogendo/attention-fusion-distilbert")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu") if TORCH_AVAILABLE else None
        self.tokenizer = None
        self.model = None
        self.label_maps = None
        self.loaded = False
        self.load_time = None
        self.error = None
        self.max_length = 512

        # Reverse label maps (built during load)
        self._ner_id_to_label: Dict[int, str] = {}
        self._cls_id_to_main: Dict[int, str] = {}
        self._cls_id_to_sub: Dict[int, str] = {}
        self._cls_id_to_interv: Dict[int, str] = {}
        self._cls_id_to_priority: Dict[int, str] = {}

    # Loading
    

    def load(self) -> bool:
        """Load exclusively from HuggingFace Hub: Rogendo/attention-fusion-distilbert"""
        if not TORCH_AVAILABLE:
            self.error = "PyTorch / Transformers not installed"
            logger.error(f"AttentionFusion: {self.error}")
            return False

        logger.info(f"Loading AttentionFusion from HuggingFace Hub: {self.hf_repo}")
        return self._load_from_hub(self.hf_repo)

    def _load_from_hub(self, repo_id: str) -> bool:
        try:
            from huggingface_hub import hf_hub_download
            hf_kwargs = self.settings.get_hf_model_kwargs()
            start = datetime.now()

            # Download model.pt and label_maps.json individually via hf_hub_download
            # (handles LFS files correctly, unlike snapshot_download)
            weights_path = hf_hub_download(repo_id=repo_id, filename="model.pt", **hf_kwargs)
            maps_path    = hf_hub_download(repo_id=repo_id, filename="label_maps.json", **hf_kwargs)

            logger.info(f"Downloaded model.pt  → {weights_path}")
            logger.info(f"Downloaded label_maps → {maps_path}")

            # Load label maps
            with open(maps_path, encoding="utf-8") as f:
                self.label_maps = json.load(f)

            ner_maps = self.label_maps["ner"]
            cls_maps = self.label_maps["cls"]
            self._ner_id_to_label    = {int(k): v for k, v in ner_maps["id_to_label"].items()}
            self._cls_id_to_main     = {int(k): v for k, v in cls_maps["id_to_main_cat"].items()}
            self._cls_id_to_sub      = {int(k): v for k, v in cls_maps["id_to_sub_cat"].items()}
            self._cls_id_to_interv   = {int(k): v for k, v in cls_maps["id_to_interv"].items()}
            self._cls_id_to_priority = {int(k): v for k, v in cls_maps["id_to_priority"].items()}

            # Load tokenizer directly from HF repo (no local files needed)
            self.tokenizer = AutoTokenizer.from_pretrained(repo_id, **hf_kwargs)

            # Build model architecture using label map dimensions
            qa_head_config = self.label_maps["qa"]["head_config"]
            self.model = AttentionFusionModel(
                backbone_name="distilbert-base-cased",
                dropout=0.0,
                num_ner_labels=len(ner_maps["label_to_id"]),
                num_main_cat=len(cls_maps["main_cat2id"]),
                num_sub_cat=len(cls_maps["sub_cat2id"]),
                num_intervention=len(cls_maps["interv2id"]),
                num_priority=len(cls_maps["priority2id"]),
                qa_heads_config=qa_head_config,
            )

            # Load weights to CPU first to avoid double GPU allocation on shared GPU
            state_dict = torch.load(weights_path, map_location="cpu")
            self.model.load_state_dict(state_dict)
            self.model.to(self.device)
            self.model.eval()

            self.loaded = True
            self.load_time = datetime.now()
            elapsed = (self.load_time - start).total_seconds()
            logger.info(f"AttentionFusion model loaded from HF Hub ({repo_id}) in {elapsed:.1f}s on {self.device}")
            return True

        except Exception as e:
            self.error = str(e)
            self.loaded = False
            logger.error(f"AttentionFusion HF Hub load failed: {e}", exc_info=True)
            return False

    def is_ready(self) -> bool:
        return self.loaded and self.model is not None

    def get_model_info(self) -> Dict[str, Any]:
        return {
            "loaded": self.loaded,
            "hf_repo": self.hf_repo,
            "device": str(self.device) if self.device else None,
            "load_time": self.load_time.isoformat() if self.load_time else None,
            "error": self.error,
            "tasks": ["ner", "cls", "qa"],
            "ner_labels": list(self._ner_id_to_label.values()) if self._ner_id_to_label else [],
            "cls_heads": ["main_category", "sub_category", "intervention", "priority"],
            "qa_heads": list(QA_SUBMETRIC_LABELS.keys()),
        }

     
    # Internal tokenizer helper
    

    def _tokenize(self, text: str, return_offsets: bool = False):
        """Tokenize a single text and return tensors on the correct device."""
        kwargs = dict(
            truncation=True,
            padding=False,
            return_tensors="pt",
            max_length=self.max_length,
        )
        if return_offsets:
            kwargs["return_offsets_mapping"] = True

        enc = self.tokenizer(text, **kwargs)
        return {k: v.to(self.device) if isinstance(v, torch.Tensor) else v
                for k, v in enc.items()}

     
    # NER
    

    def predict_ner(self, text: str) -> List[Dict[str, str]]:
        """
        Returns only the non-O entities as a list of dicts:
        [{"token": "Nairobi", "label": "LOCATION"}, ...]
        """
        enc = self._tokenize(text, return_offsets=True)
        input_ids = enc["input_ids"]
        attention_mask = enc["attention_mask"]
        offset_mapping = enc["offset_mapping"].squeeze(0).tolist()

        with torch.no_grad():
            out = self.model(input_ids=input_ids, attention_mask=attention_mask, task="ner")

        preds = out["logits"].argmax(dim=-1).squeeze(0).cpu().tolist()
        tokens = self.tokenizer.convert_ids_to_tokens(input_ids.squeeze(0).tolist())

        entities = []
        for token, pred_id, (tok_start, tok_end) in zip(tokens, preds, offset_mapping):
            if tok_start == 0 and tok_end == 0:
                continue  # skip [CLS], [SEP], [PAD]
            label = self._ner_id_to_label.get(pred_id, "O")
            if label != "O":
                entities.append({"token": token, "label": label})

        return entities

    
    # Classification
    

    def predict_classification(self, text: str) -> Dict[str, str]:
        """
        Returns predicted case labels across all four heads:
        {
          "main_category": "GBV",
          "sub_category":  "...",
          "intervention":  "...",
          "priority":      "..."
        }
        """
        enc = self._tokenize(text)
        with torch.no_grad():
            out = self.model(
                input_ids=enc["input_ids"],
                attention_mask=enc["attention_mask"],
                task="cls",
            )
        logits = out["logits"]

        return {
            "main_category": self._cls_id_to_main.get(logits["main"].argmax(dim=-1).item(), "Unknown"),
            "sub_category":  self._cls_id_to_sub.get(logits["sub"].argmax(dim=-1).item(), "Unknown"),
            "intervention":  self._cls_id_to_interv.get(logits["intervention"].argmax(dim=-1).item(), "Unknown"),
            "priority":      self._cls_id_to_priority.get(logits["priority"].argmax(dim=-1).item(), "Unknown"),
        }

    
    # QA
    

    def predict_qa(self, text: str, threshold: float = 0.5) -> Dict[str, List[Dict]]:
        """
        Returns per-head binary predictions with human-readable submetric names:
        {
          "opening": [{"submetric": "Use of call opening phrase", "passed": True, "score": 0.82}],
          "listening": [...],
          ...
        }
        """
        enc = self._tokenize(text)
        with torch.no_grad():
            out = self.model(
                input_ids=enc["input_ids"],
                attention_mask=enc["attention_mask"],
                task="qa",
            )
        logits = out["logits"]

        result = {}
        for head, labels in QA_SUBMETRIC_LABELS.items():
            probs = logits[head].sigmoid().squeeze(0).cpu().tolist()
            if isinstance(probs, float):
                probs = [probs]
            result[head] = [
                {
                    "submetric": label,
                    "passed": bool(prob > threshold),
                    "score": round(float(prob), 4),
                }
                for label, prob in zip(labels, probs)
            ]

        return result

    
    # Unified (all three heads, single backbone call per head)
    

    def predict_all(self, text: str, threshold: float = 0.5) -> Dict[str, Any]:
        """
        Run NER + Classification + QA scoring and return all results in one dict.
        Three forward passes over the shared backbone, one tokenization.
        """
        return {
            "ner": self.predict_ner(text),
            "classification": self.predict_classification(text),
            "qa": self.predict_qa(text, threshold),
        }


attention_fusion_model = AttentionFusionModelService()
