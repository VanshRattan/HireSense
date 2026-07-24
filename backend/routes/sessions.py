from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
import os
import shutil
from services.audio_analysis import analyze_audio
from services.feedback_generator import generate_feedback

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("/start", response_model=schemas.SessionOut)
def start_session(session: schemas.SessionCreate, db: Session = Depends(get_db)):
    # Ensure the user exists to prevent Foreign Key constraint violations
    user = db.query(models.User).filter(models.User.id == session.user_id).first()
    if not user:
        user = models.User(id=session.user_id, email=f"test{session.user_id}@example.com", hashed_password="mock")
        db.add(user)
        db.commit()

    db_session = models.Session(user_id=session.user_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.post("/{session_id}/upload")
async def upload_chunk(session_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    db_session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    # Save the chunk for processing
    upload_dir = f"uploads/session_{session_id}"
    os.makedirs(upload_dir, exist_ok=True)
    file_location = f"{upload_dir}/{file.filename}"
    
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
        
    # Here we would normally trigger the ML pipeline or add to a queue
    return {"message": "Chunk uploaded successfully", "filename": file.filename}

@router.post("/{session_id}/finish", response_model=schemas.ReportOut)
def finish_session(session_id: int, db: Session = Depends(get_db)):
    db_session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    upload_dir = f"uploads/session_{session_id}"
    # Assuming there's a file saved. In reality, you'd concat chunks. 
    # For now, we just find the first file inside the directory.
    if not os.path.exists(upload_dir):
        raise HTTPException(status_code=400, detail="No uploads found for session")
        
    files = os.listdir(upload_dir)
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
        
    main_file = os.path.join(upload_dir, files[0])
    
    # Run analysis safely
    try:
        audio_results = analyze_audio(main_file)
    except Exception as e:
        print(f"Audio analysis failed: {e}")
        audio_results = {"filler_word_count": 0, "filler_words_used": {}, "transcript": f"Error during audio processing: {e}"}

    try:
        from services.video_analysis import analyze_video
        video_results = analyze_video(main_file)
    except Exception as e:
        print(f"Video analysis failed: {e}")
        video_results = {"eye_contact_percentage": 0, "engagement_score": 0}
    
    # Generate feedback
    feedback = generate_feedback(audio_results, video_results)
    
    # Save Report
    report = models.Report(
        session_id=session_id,
        communication_score=feedback["communication_score"],
        confidence_score=feedback["confidence_score"],
        filler_word_count=feedback["filler_word_count"],
        filler_words_used=feedback["filler_words_used"],
        feedback_summary=feedback["feedback_summary"],
        transcript=feedback["transcript"],
        wpm=feedback.get("wpm", 0.0)
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    
    return report

@router.get("/{session_id}/results", response_model=schemas.ReportOut)
def get_results(session_id: int, db: Session = Depends(get_db)):
    report = db.query(models.Report).filter(models.Report.session_id == session_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not ready or not found")
    return report

@router.get("/", response_model=list[schemas.SessionOut])
def get_sessions(user_id: int, db: Session = Depends(get_db)):
    sessions = db.query(models.Session).filter(models.Session.user_id == user_id).all()
    return sessions
