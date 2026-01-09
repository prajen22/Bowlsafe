from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schema

from app.models import Progress
from app.schema import ProgressCreate
from sqlalchemy.orm import Session
from fastapi import Depends


app = FastAPI()

@app.post("/login", response_model=schema.LoginResponse)
def login(data: schema.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == data.email,
        models.User.password == data.password
    ).first()

    if not user:
        return {"success": False, "message": "Invalid credentials"}

    return {"success": True, "message": "Login successful"}


@app.post("/progress")
def create_progress(
    progress: schema.ProgressCreate,
    db: Session = Depends(get_db)
):
    entry = models.Progress(
        date=progress.date,
        overs=progress.overs,
        daily_target=progress.daily_target,
        effort_level=progress.effort_level,
        body_status=progress.body_status,
        session_type=progress.session_type,
        notes=progress.notes,
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return {"message": "Progress saved successfully"}


from datetime import date, timedelta
from sqlalchemy import func

@app.get("/weekly-stats")
def weekly_stats(db: Session = Depends(get_db)):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    last_week_start = week_start - timedelta(days=7)
    last_week_end = week_start - timedelta(days=1)

    this_week_overs = (
        db.query(func.sum(models.Progress.overs))
        .filter(models.Progress.date >= week_start)
        .scalar()
        or 0
    )

    last_week_overs = (
        db.query(func.sum(models.Progress.overs))
        .filter(
            models.Progress.date >= last_week_start,
            models.Progress.date <= last_week_end,
        )
        .scalar()
        or 0
    )

    percent_change = (
        ((this_week_overs - last_week_overs) / last_week_overs) * 100
        if last_week_overs > 0
        else 0
    )

    if percent_change <= 15:
        risk = "Normal"
    elif percent_change <= 25:
        risk = "Watch"
    else:
        risk = "Risk"

    return {
        "week_start": week_start,
        "this_week_overs": this_week_overs,
        "last_week_overs": last_week_overs,
        "percent_change": round(percent_change, 2),
        "risk_level": risk,
    }


@app.get("/progress")
def get_progress(db: Session = Depends(get_db)):
    return db.query(Progress).order_by(Progress.date).all()

