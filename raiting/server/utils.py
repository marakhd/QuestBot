from db import User, Score
from tortoise.expressions import Q
from datetime import datetime

async def get_ranked_users(class_id: int):
    users = await User.filter(sch_class_id=class_id).prefetch_related("scores")
    data = []

    for user in users:
        correct_scores = [s for s in await user.scores.all() if s.is_decided]
        correct_count = len(correct_scores)

        if not user.start_time or not user.end_time:
            continue

        time_spent = (user.end_time - user.start_time).total_seconds()
        avg_speed = time_spent / correct_count if correct_count else float('inf')

        data.append({
            "user": user,
            "avg_speed": avg_speed,
            "correct_answers": correct_count,
            "time_spent": time_spent
        })

    sorted_data = sorted(data, key=lambda x: (x["avg_speed"], -x["correct_answers"]))

    result = []
    for i, u in enumerate(sorted_data, 1):
        result.append({
            "id": u["user"].id,
            "full_name": u["user"].full_name,
            "rank": i,
            "avg_speed": round(u["avg_speed"], 2),
            "correct_answers": u["correct_answers"]
        })

    return result
