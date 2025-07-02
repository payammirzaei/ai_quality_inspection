from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.db.database import SessionLocal
from app.db.models import DefectReport, User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_reports(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    reports = db.query(DefectReport).filter(DefectReport.user_id == current_user.id).all()
    return [
        {
            "id": r.id,
            "image_path": r.image_path,
            "result": r.result,
            "confidence": r.confidence,
            "created_at": r.created_at
        } for r in reports
    ]

@router.get("/{report_id}")
def get_report(report_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    report = db.query(DefectReport).filter(DefectReport.id == report_id, DefectReport.user_id == current_user.id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return {
        "id": report.id,
        "image_path": report.image_path,
        "result": report.result,
        "confidence": report.confidence,
        "created_at": report.created_at
    } 