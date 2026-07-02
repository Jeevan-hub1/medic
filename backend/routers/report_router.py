import json
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import models
import schemas
import auth
from database import get_db
from ai.report_analyzer import analyze_health_report_text

router = APIRouter(
    prefix="/reports",
    tags=["reports"]
)

@router.post("/analyze", response_model=schemas.HealthReport)
async def upload_and_analyze_report(
    file: UploadFile = File(...),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    try:
        content_bytes = await file.read()
        
        # Determine how to extract text from file
        report_text = ""
        filename_lower = file.filename.lower()
        
        if filename_lower.endswith(".txt"):
            report_text = content_bytes.decode("utf-8", errors="ignore")
        elif filename_lower.endswith(".pdf"):
            # Simple PDF extraction placeholder: attempt to parse if PyPDF2 works,
            # otherwise decode ASCII printable characters or fallback
            try:
                import io
                from pypdf import PdfReader
                reader = PdfReader(io.BytesIO(content_bytes))
                text_list = [page.extract_text() for page in reader.pages]
                report_text = "\n".join(text_list)
            except Exception:
                # If library not present/fails, use a clean string decode fallback
                report_text = content_bytes.decode("utf-8", errors="ignore")[:3000]
        else:
            # Decode printable parts or fallback to file metadata + size
            report_text = f"Analyze health data from file: {file.filename} (Size: {len(content_bytes)} bytes)"
            
        # Clean/truncate if needed
        if not report_text.strip():
            report_text = "Empty report content or binary scan"
            
        # Call Gemini report analyzer
        analysis_data = analyze_health_report_text(report_text)
        
        # Save to database
        db_report = models.HealthReport(
            user_id=current_user.id,
            file_path=file.filename,
            analysis_json=json.dumps(analysis_data)
        )
        
        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        return db_report
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report analysis failed: {str(e)}")

@router.get("/my-reports", response_model=list)
def get_user_reports(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    reports = db.query(models.HealthReport).filter(
        models.HealthReport.user_id == current_user.id
    ).order_by(models.HealthReport.uploaded_at.desc()).all()
    
    result = []
    for r in reports:
        try:
            analysis = json.loads(r.analysis_json)
        except Exception:
            analysis = {}
        result.append({
            "id": r.id,
            "file_path": r.file_path,
            "uploaded_at": r.uploaded_at,
            "analysis": analysis
        })
    return result
