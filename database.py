from tortoise.contrib.fastapi import register_tortoise
from dotenv import load_dotenv
import os

load_dotenv()
# DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = 'postgres://shah:2024@localhost:5432/stream'

TORTOISE_ORM = {
      "connections": {
        "default": DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": ["aerich.models","app.accounts.models"],
            "default_connection": "default",
        }
    },
}

def init_db(app):
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        # modules={"models": ["app.models"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )
