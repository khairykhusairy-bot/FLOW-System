"""
FLOW — Flood Level Observation Warning System
Detection Module: YOLO-based debris detection with OpenCV fallback
"""

import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional
import os

# Try importing ultralytics
try:
    from ultralytics import YOLO
    ULTRALYTICS_AVAILABLE = True
except ImportError:
    ULTRALYTICS_AVAILABLE = False

from utils import COCO_DEBRIS_MAP

# ─── Debris label sets ─────────────────────────────────────────────────────────
DEBRIS_KEYWORDS = {
    "bottle", "plastic_waste", "log", "branch", "trash",
    "river_debris", "cup", "bag", "can", "wrapper"
}


class DebrisDetector:
    """
    Loads a YOLO model (best.pt or fallback to yolov8n) and runs inference
    on frames to detect river debris objects.
    """

    def __init__(self, model_path: str = "best.pt", confidence: float = 0.35):
        self.confidence = confidence
        self.model = None
        self.model_type = "none"
        self.class_names: Dict[int, str] = {}
        self.using_demo_mode = False
        self._demo_tick = 0

        self._load_model(model_path)

    def _load_model(self, model_path: str):
        """Attempt to load YOLO model, with fallback chain."""
        if not ULTRALYTICS_AVAILABLE:
            print("[FLOW] ultralytics not installed — using demo mode.")
            self.using_demo_mode = True
            return

        # Try custom weights first
        if os.path.exists(model_path):
            try:
                self.model = YOLO(model_path)
                self.model_type = "custom"
                print(f"[FLOW] Loaded custom model: {model_path}")
                self._init_class_names()
                return
            except Exception as e:
                print(f"[FLOW] Failed to load {model_path}: {e}")

        # Fallback to yolov8n (downloads automatically)
        try:
            self.model = YOLO("yolov8n.pt")
            self.model_type = "coco"
            print("[FLOW] Loaded yolov8n (COCO) fallback model.")
            self._init_class_names()
            return
        except Exception as e:
            print(f"[FLOW] Could not load yolov8n: {e}")

        print("[FLOW] No model available — using demo simulation mode.")
        self.using_demo_mode = True

    def _init_class_names(self):
        """Extract class names from the loaded model."""
        if self.model and hasattr(self.model, "names"):
            self.class_names = self.model.names
        else:
            self.class_names = {i: f"class_{i}" for i in range(80)}

    def _map_label(self, raw_label: str) -> str:
        """Map COCO or custom labels to FLOW debris categories."""
        label_lower = raw_label.lower().replace(" ", "_")
        # Direct match
        if label_lower in DEBRIS_KEYWORDS:
            return label_lower
        # COCO mapping
        mapped = COCO_DEBRIS_MAP.get(raw_label.lower(), None)
        if mapped:
            return mapped
        # Keyword heuristic
        for kw in DEBRIS_KEYWORDS:
            if kw in label_lower:
                return kw
        # Return all objects in demo/fallback mode to show activity
        return label_lower

    def detect(self, frame: np.ndarray) -> List[Dict]:
        """
        Run inference on a frame and return detection results.

        Returns list of dicts:
            {
                "bbox": (x1, y1, x2, y2),
                "label": str,
                "confidence": float,
                "class_id": int,
            }
        """
        if self.using_demo_mode:
            return self._generate_demo_detections(frame)

        if self.model is None:
            return []

        try:
            results = self.model(
                frame,
                conf=self.confidence,
                verbose=False,
                stream=False,
            )
        except Exception as e:
            print(f"[FLOW] Inference error: {e}")
            return []

        detections = []
        for result in results:
            if result.boxes is None:
                continue
            for box in result.boxes:
                try:
                    x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]
                    conf = float(box.conf[0])
                    cls_id = int(box.cls[0])
                    raw_label = self.class_names.get(cls_id, f"class_{cls_id}")
                    label = self._map_label(raw_label)

                    # In custom model mode, keep all detections
                    # In COCO mode, filter to debris-like objects only
                    if self.model_type == "coco":
                        if raw_label.lower() not in COCO_DEBRIS_MAP:
                            continue

                    detections.append({
                        "bbox": (x1, y1, x2, y2),
                        "label": label,
                        "confidence": conf,
                        "class_id": cls_id,
                    })
                except Exception:
                    continue

        return detections

    def _generate_demo_detections(self, frame: np.ndarray) -> List[Dict]:
        """
        Generate realistic simulated detections for demo / no-model mode.
        Detections move and vary over time to simulate a live river feed.
        """
        h, w = frame.shape[:2]
        self._demo_tick += 1
        t = self._demo_tick

        np.random.seed(t // 8)  # Change every ~8 frames for smooth motion

        debris_classes = [
            "bottle", "plastic_waste", "log",
            "branch", "trash", "river_debris"
        ]
        detections = []
        n = np.random.randint(3, 10)

        for i in range(n):
            # Oscillate positions with time
            base_x = int((w * (i + 1)) / (n + 1))
            base_y = int(h * 0.35 + h * 0.3 * np.random.rand())
            dx = int(30 * np.sin(t * 0.05 + i * 1.2))
            dy = int(10 * np.cos(t * 0.08 + i * 0.8))

            x1 = max(0, base_x + dx - np.random.randint(20, 60))
            y1 = max(0, base_y + dy - np.random.randint(15, 40))
            x2 = min(w - 1, x1 + np.random.randint(40, 100))
            y2 = min(h - 1, y1 + np.random.randint(30, 70))

            label = debris_classes[i % len(debris_classes)]
            conf = round(0.55 + 0.40 * np.random.rand(), 3)

            detections.append({
                "bbox": (x1, y1, x2, y2),
                "label": label,
                "confidence": conf,
                "class_id": i,
            })

        return detections

    def set_confidence(self, confidence: float):
        self.confidence = max(0.1, min(0.99, confidence))

    @property
    def status(self) -> str:
        if self.using_demo_mode:
            return "Demo Mode (No Model)"
        return f"YOLO ({self.model_type})"
