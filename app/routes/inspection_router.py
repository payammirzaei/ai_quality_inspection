from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from app.auth.dependencies import get_current_user
from app.db.models import User, DefectReport
from app.services.ai_model import defect_detector
from app.services.image_processor import ImageProcessor
from PIL import Image
import io, os
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()

UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

bearer_scheme = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/inspect")
def inspect_image(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")
    
    try:
        # Read and validate image
        image_bytes = file.file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Validate image quality
        if not ImageProcessor.validate_image(image):
            raise HTTPException(status_code=400, detail="Image quality too low for analysis. Please upload a clearer image.")
        
        # Preprocess image for AI analysis
        processed_image = ImageProcessor.preprocess_for_detection(image)
        
        # Get image information
        image_info = ImageProcessor.get_image_info(image)
        
        # Perform real AI defect detection
        ai_result = defect_detector.detect_defects(processed_image)
        
        # Save original image
        filename = f"{current_user.username}_{file.filename}"
        save_path = os.path.join(UPLOAD_DIR, filename)
        image.save(save_path)
        
        # Save report to database
        report = DefectReport(
            user_id=current_user.id,
            image_path=save_path,
            result=ai_result["message"],
            confidence=ai_result["confidence"]
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        
        # Prepare response
        response = {
            "report_id": report.id,
            "filename": filename,
            "image_info": image_info,
            "ai_analysis": {
                "defect_detected": ai_result["defect_detected"],
                "confidence": ai_result["confidence"],
                "defect_type": ai_result["defect_type"],
                "defect_confidence": ai_result["defect_confidence"],
                "no_defect_confidence": ai_result["no_defect_confidence"],
                "bounding_box": ai_result["bounding_box"],
                "message": ai_result["message"]
            },
            "processing_info": {
                "model_used": "ResNet-50 with Custom Classifier",
                "device": str(defect_detector.device),
                "preprocessing_applied": ["RGB conversion", "Contrast enhancement", "Sharpness enhancement"]
            }
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}") 