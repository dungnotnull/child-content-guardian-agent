import json
import os
from typing import Dict, Any, Tuple
from src.database.models import ContentEvent
from src.models.classifiers import TextClassifier, ImageClassifier

class DecisionEngine:
    def __init__(self):
        # Load thresholds from config
        config_path = 'config/thresholds.json'
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Lazy-load classifiers to save memory until needed
        self._text_clf = None
        self._image_clf = None

    @property
    def text_clf(self):
        if self._text_clf is None:
            self._text_clf = TextClassifier()
        return self._text_clf

    @property
    def image_clf(self):
        if self._image_clf is None:
            self._image_clf = ImageClassifier()
        return self._image_clf

    async def process_content(self, profile_id: int, content_type: str, payload: str) -> Tuple[str, str, Dict[str, float]]:
        # 1. Determine Age Band (Real DB lookup in main.py, passed here as fixed for this engine logic)
        # In full system, we'd query ChildProfile.age_band
        age_band = \"middle_childhood\" 
        thresholds = self.config['age_bands'][age_band]['thresholds']
        
        scores = {}
        if content_type == 'text':
            scores = await self.text_clf.predict(payload)
        elif content_type == 'image':
            scores = await self.image_clf.predict(payload)
            
        # 2. Decision Logic
        decision = \"ALLOW\"
        reason = \"Content is appropriate for the child's age.\"
        
        # Check for critical violations regardless of age band
        max_score = max(scores.values()) if scores else 0
        if max_score >= self.config['global_defaults']['critical_block_threshold']:
            return \"BLOCK\", \"Critical safety violation detected (Extreme score).\", scores

        # Check against age-band specific thresholds
        for category, threshold in thresholds.items():
            score = scores.get(category, 0.0)
            if score > threshold:
                # Any breach of a specific threshold triggers a warning or block
                # If it's an NSFW/Violence breach, we BLOCK; for others we WARN
                if category in ['nsfw', 'violence']:
                    return \"BLOCK\", f\"Sensitive {category} content detected.\", scores
                else:
                    decision = \"WARN\"
                    reason = f\"Content contains {category} markers above age threshold.\"
                    
        return decision, reason, scores
