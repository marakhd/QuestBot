from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import Class, User, Score, Quest
from schemas import ClassOut, UserBrief, UserDetail
from db import init_db
from utils import get_ranked_users
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(_):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/classes", response_model=list[ClassOut])
async def get_classes():
    return await Class.all()

@app.get("/classes/{id}", response_model=ClassOut)
async def get_classes(id: int):
    return await Class.filter(id=id).first()

@app.get("/classes/{class_id}/users", response_model=list[UserBrief])
async def get_class_users(class_id: int):
    return await get_ranked_users(class_id)

@app.get("/users/{user_id}", response_model=UserDetail)
async def get_user_detail(user_id: int):
    user = await User.get_or_none(id=user_id).prefetch_related("scores", "scores__quest")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    correct_scores = [s for s in await user.scores.all()]
    time_spent = (user.end_time - user.start_time).total_seconds() if user.start_time and user.end_time else 0

    tasks = []
    for score in correct_scores:
        quest = await score.quest.first()
        tasks.append({
            "question": quest.text,
            "your_answer": score.answer,
            "correct_answer": quest.correct_answer,
            "is_correct": score.is_decided
    })
    
    return {
        "id": user.id,
        "tg_username": user.tg_username,
        "full_name": user.full_name,
        "correct_answers": len(correct_scores),
        "total_time_seconds": round(time_spent, 2),
        "answers": tasks
    }
