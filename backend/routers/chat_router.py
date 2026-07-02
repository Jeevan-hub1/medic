from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
import auth
from database import get_db
from ai.chatbot import generate_chat_response

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

@router.post("/message", response_model=schemas.ChatResponse)
def send_chat_message(
    chat_req: schemas.ChatRequest,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    session_id = chat_req.session_id
    
    # 1. Create or verify chat session
    if not session_id:
        new_session = models.ChatSession(user_id=current_user.id)
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        session_id = new_session.id
    else:
        session = db.query(models.ChatSession).filter(
            models.ChatSession.id == session_id,
            models.ChatSession.user_id == current_user.id
        ).first()
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
            
    # 2. Get history from DB to feed the model
    db_messages = db.query(models.ChatMessage).filter(
        models.ChatMessage.session_id == session_id
    ).order_by(models.ChatMessage.timestamp.asc()).all()
    
    history = []
    for msg in db_messages:
        role = "user" if msg.role == "user" else "model"
        history.append({"role": role, "content": msg.content})
        
    # 3. Call Gemini Chatbot
    bot_reply = generate_chat_response(chat_req.message, history)
    
    # 4. Save messages to DB
    user_msg = models.ChatMessage(
        session_id=session_id,
        role="user",
        content=chat_req.message
    )
    bot_msg = models.ChatMessage(
        session_id=session_id,
        role="assistant",
        content=bot_reply
    )
    
    db.add(user_msg)
    db.add(bot_msg)
    db.commit()
    
    return schemas.ChatResponse(
        response=bot_reply,
        session_id=session_id
    )

@router.get("/sessions", response_model=list)
def get_user_chat_sessions(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    sessions = db.query(models.ChatSession).filter(
        models.ChatSession.user_id == current_user.id
    ).all()
    return [{"id": s.id, "created_at": s.created_at} for s in sessions]

@router.get("/history/{session_id}", response_model=list)
def get_chat_history(
    session_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    session = db.query(models.ChatSession).filter(
        models.ChatSession.id == session_id,
        models.ChatSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
        
    messages = db.query(models.ChatMessage).filter(
        models.ChatMessage.session_id == session_id
    ).order_by(models.ChatMessage.timestamp.asc()).all()
    
    return [
        {
            "role": m.role,
            "content": m.content,
            "timestamp": m.timestamp
        }
        for m in messages
    ]
