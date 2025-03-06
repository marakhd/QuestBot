from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.BigIntField(pk=True)
    tg_username = fields.CharField(max_length=255, unique=True, null=True)
    tg_id = fields.BigIntField(unique=True)
    full_name = fields.CharField(max_length=255, null=True)

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
    capitan = fields.ForeignKeyField("models.User", related_name="capitan", null=True)

    users = fields.ReverseRelation["User"]
    quests = fields.ReverseRelation["Quest"]

    state_game = fields.BooleanField(default=False)
    last_task_number = fields.IntField(default=1)
    last_task = fields.ForeignKeyField("models.Quest", related_name="last_task", null=True)

    start_time = fields.DatetimeField(null=True)

    is_active = fields.BooleanField(default=True, null=False)

    class Meta:
        table = "classes"


class Quest(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    data = fields.TextField(null=True)
    text = fields.TextField()
    answer = fields.TextField()
    type = fields.CharField(max_length=255)
    for_class = fields.ForeignKeyField("models.Class", related_name="quests", null=True)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "quests"


class Score(Model):
    id = fields.BigIntField(pk=True)

    score = fields.IntField(default=0)

    quest = fields.ForeignKeyField("models.Quest", related_name="points", on_delete="RESTRICT")
    class_ = fields.ForeignKeyField("models.Class", related_name="points", on_delete="CASCADE")

    class Meta:
        table = "scores"
