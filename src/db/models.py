from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.BigIntField(pk=True)
    tg_username = fields.CharField(max_length=255, unique=True)
    tg_id = fields.BigIntField(unique=True)
    full_name = fields.CharField(max_length=255, null=True)

    class_id = fields.ForeignKeyField(
        "models.Class",  # Связь с таблицей classes
        related_name="users",  # Позволяет получать список пользователей через `class_obj.users.all()`
        on_delete=fields.CASCADE,  # Если класс удаляется — удаляются и пользователи
    )

    class Meta:
        table = "users"


class Class(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    capitan_id = fields.ForeignKeyField(
        "models.User", related_name="capitan", null=True
    )
    is_active = fields.BooleanField(default=True)

    users = fields.ReverseRelation["User"]
    quests = fields.ReverseRelation["Quest"]
    
    state_game = fields.BooleanField(default=False)
    last_task = fields.IntField(default=1)

    class Meta:
        table = "classes"


class Quest(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    text = fields.TextField()
    answer = fields.TextField()
    type = fields.CharField(max_length=255)
    for_class = fields.ForeignKeyField("models.Class", related_name="quests")
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "quests"


class Point(Model):
    id = fields.BigIntField(pk=True)

    quest = fields.ForeignKeyField("models.Quest", related_name="points")
    class_ = fields.ForeignKeyField("models.Class", related_name="points")

    class Meta:
        table = "points"
