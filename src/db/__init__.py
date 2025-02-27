from .models import *

from tortoise import Tortoise
from config import TORTOISE_ORM, settings

async def init_db():
    await Tortoise.init(TORTOISE_ORM)

async def close_db():
    await Tortoise.close_connections()
