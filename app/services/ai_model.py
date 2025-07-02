import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image
import numpy as np
import cv2
from typing import Dict, List, Tuple, Optional
import os

class DefectDetectionModel(nn.Module):
    def __init__(self, num_classes: int = 2, pretrained: bool = True):
        super(DefectDetectionModel, self).__init__()
        
        # Use ResNet-50 as backbone
        self.backbone = models.resnet50(pretrained=pretrained)
        
        # Remove the final classification layer
        num_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Identity()
        
        # Custom classification head for defect detection
        self.classifier = nn.Sequential(
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, num_classes)
        )
        
        # Defect types (0: No defect, 1: Defect)
        self.defect_types = ["No Defect", "Defect Detected"]
        
    def forward(self, x):
        features = self.backbone(x)
        logits = self.classifier(features)
        return logits
    
    def predict(self, image: Image.Image) -> Dict:
        """Perform defect detection on input image"""
        self.eval()
        
        # Preprocess image
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
        
        input_tensor = transform(image).unsqueeze(0)
        
        with torch.no_grad():
            logits = self(input_tensor)
            probabilities = F.softmax(logits, dim=1)
            
            # Get predictions
            predicted_class = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][predicted_class].item()
            
            # Determine if defect is detected
            defect_detected = predicted_class == 1
            defect_type = self.defect_types[predicted_class]
            
            # Calculate additional metrics
            defect_confidence = probabilities[0][1].item() if defect_detected else 0.0
            no_defect_confidence = probabilities[0][0].item()
            
            # Generate bounding box if defect detected (simplified)
            bounding_box = None
            if defect_detected and confidence > 0.7:
                # Simple bounding box around the center of the image
                h, w = image.size[::-1]  # PIL size is (width, height)
                center_x, center_y = w // 2, h // 2
                box_size = min(w, h) // 4
                bounding_box = [
                    center_x - box_size,
                    center_y - box_size,
                    center_x + box_size,
                    center_y + box_size
                ]
            
            return {
                "defect_detected": defect_detected,
                "confidence": confidence,
                "defect_type": defect_type,
                "defect_confidence": defect_confidence,
                "no_defect_confidence": no_defect_confidence,
                "bounding_box": bounding_box,
                "message": f"{defect_type} (Confidence: {confidence:.2%})"
            }

class DefectDetector:
    def __init__(self, model_path: Optional[str] = None):
        self.model = DefectDetectionModel()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        
        # Load pre-trained weights if available
        if model_path and os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            print(f"Loaded model from {model_path}")
        else:
            print("Using pre-trained ResNet backbone with custom classifier")
        
        self.model.eval()
    
    def detect_defects(self, image: Image.Image) -> Dict:
        """Main method to detect defects in an image"""
        try:
            result = self.model.predict(image)
            return result
        except Exception as e:
            print(f"Error during defect detection: {e}")
            return {
                "defect_detected": False,
                "confidence": 0.0,
                "defect_type": "Error",
                "defect_confidence": 0.0,
                "no_defect_confidence": 0.0,
                "bounding_box": None,
                "message": f"Error during analysis: {str(e)}"
            }

# Global model instance
defect_detector = DefectDetector() 