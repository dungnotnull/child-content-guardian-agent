import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from PIL import Image
import requests
from io import BytesIO
import numpy as np
from typing import Dict, Any

class TextClassifier:
    def __init__(self, model_path: str = \"unitary/toxic-roberta-base\"):
        # In a real run, these load from disk/HF
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.pipeline = pipeline(\"text-classification\", model=self.model, tokenizer=self.tokenizer, device=-1) # CPU

    async def predict(self, text: str) -> Dict[str, float]:
        # Real inference logic
        results = self.pipeline(text)
        # Return normalized scores for categories
        # toxic-roberta returns labels like 'toxic', 'severe_toxic'
        return {res['label']: res['score'] for res in results}

class ImageClassifier:
    def __init__(self, nsfw_model: str = \"facebook/convnext-tiny-patch4-nsfw\", 
                 violence_model: str = \"microsoft/resnet-50-violence-detection\"):
        self.nsfw_pipe = pipeline(\"image-classification\", model=nsfw_model, device=-1)
        self.violence_pipe = pipeline(\"image-classification\", model=violence_model, device=-1)

    async def predict(self, image_source: str) -> Dict[str, float]:
        # Handle both URL and local path
        if image_source.startswith('http'):
            response = requests.get(image_source, timeout=5)
            img = Image.open(BytesIO(response.content))
        else:
            img = Image.open(image_source)
            
        nsfw_res = self.nsfw_pipe(img)
        viol_res = self.violence_pipe(img)
        
        # Normalize to 0-1 based on top labels
        return {
            \"nsfw\": nsfw_res[0]['score'] if nsfw_res[0]['label'] == 'nsfw' else 0.0,
            \"violence\": viol_res[0]['score'] if viol_res[0]['label'] == 'violent' else 0.0
        }
