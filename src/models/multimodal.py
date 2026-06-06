import cv2
import numpy as np
from typing import List, Tuple
from src.models.classifiers import ImageClassifier

class VideoAnalysisPipeline:
    def __init__(self):
        self.image_clf = ImageClassifier()

    async def analyze_video(self, video_path: str) -> Tuple[float, str]:
        # Frame Sampling
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise IOError(\"Cannot open video file\")
            
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Sample exactly 10 frames distributed across the video
        interval = max(1, total_frames // 10)
        max_nsfw = 0.0
        
        for i in range(0, total_frames, interval):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if not ret: break
            
            # Convert OpenCV BGR to RGB for PIL/Transformers
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # We treat this as a local file path or raw image object
            # in a real implementation, we'd pass the numpy array directly to the pipeline
            score = await self.image_clf.predict(rgb_frame) 
            max_nsfw = max(max_nsfw, score.get('nsfw', 0.0))
            
        cap.release()
        return max_nsfw, \"Video analysis complete\"

class BrainRotAnalyzer:
    def calculate_engagement_score(self, video_path: str) -> float:
        cap = cv2.VideoCapture(video_path)
        prev_frame = None
        scene_changes = 0
        frames_processed = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            # Use Difference of Gaussians or simple AbsDiff for cut detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5,5), 0)
            
            if prev_frame is not None:
                diff = cv2.absdiff(gray, prev_frame)
                if np.mean(diff) > 25: # Cut threshold
                    scene_changes += 1
            
            prev_frame = gray
            frames_processed += 1
            
        cap.release()
        
        # Brain-rot index: Cuts per minute
        # Assuming 30fps, cut_rate = changes / (frames/30 / 60)
        if frames_processed == 0: return 0.0
        cut_rate = scene_changes / (frames_processed / 1800)
        return min(1.0, cut_rate / 100.0) # Normalized: 100 cuts/min = 1.0
