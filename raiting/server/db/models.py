from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.BigIntField(pk=True)
    tg_username = fields.CharField(max_length=255, unique=True, null=True)
    tg_id = fields.BigIntField(unique=True)
    full_name = fields.CharField(max_length=255, null=True)

    last_task_number = fields.IntField(default=1)
    last_task = fields.ForeignKeyField(
        "models.Quest", related_name="last_task", null=True
    )

    quests: fields.ReverseRelation["Quest"]

    start_time = fields.DatetimeField(null=True)
    end_time = fields.DatetimeField(null=True)

    sch_class = fields.ForeignKeyField(
        "models.Class",  # Связь с таблицей classes
        related_name="users",  # Позволяет получать список пользователей через `class_obj.users.all()`
        on_delete=fields.CASCADE,  # Если класс удаляется — удаляются и пользователи
    )

    class Meta:
        table = "users"


class Class(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)

    users: fields.ReverseRelation["User"]

    is_active = fields.BooleanField(default=True, null=False)

    class Meta:
        table = "classes"


class Quest(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    data = fields.TextField(null=True)
    grade_group = fields.CharField(max_length=25)
    text = fields.TextField()
    correct_answer = fields.TextField()
    answer_type = fields.CharField(max_length=255)
    # for_class = fields.ForeignKeyField("models.Class", related_name="quests", null=True)
    is_active = fields.BooleanField(default=True)

    options: fields.ReverseRelation["OptionQuest"]

    class Meta:
        table = "questions"


class OptionQuest(Model):
    question = fields.ForeignKeyField("models.Quest", related_name="options")
    options = fields.CharField(max_length=255)
    option_text = fields.TextField()

    class Meta:
        table = "options"


class Score(Model):
    id = fields.BigIntField(pk=True)

    score = fields.IntField(default=0)

    answer = fields.TextField(null=True)

    quest = fields.ForeignKeyField(
        "models.Quest", related_name="points", on_delete="RESTRICT"
    )
    class_ = fields.ForeignKeyField(
        "models.Class", related_name="points", on_delete="CASCADE", null=True
    )

    user = fields.ForeignKeyField("models.User", related_name="scores")

    is_decided = fields.BooleanField(default=False)

    class Meta:
        table = "scores"
