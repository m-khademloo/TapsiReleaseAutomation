import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.synchronous.database import Database

load_dotenv()


class MongoDB:
    db: Database

    def __init__(self, uri=os.getenv("MONGO_URL"), db_name=os.getenv("MONGO_DB")):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    async def register_member(self, telegram_id: int, telegram_username: str, name: str, team: str):
        # Check if user already exists
        existing_user = self.db["telegram_users"].find_one({
            "$or": [{"telegram_id": telegram_id}, {"username": f"@{telegram_username}"}]
        })
        if existing_user:
            raise Exception("Error: User already registered.")

        # Check if team exists
        team_doc = self.db["teams"].find_one({"name": team})
        if not team_doc:
            raise Exception(f"Error: Team `{team}` not found.")

        # User document
        user_doc = {
            "name": name,
            "telegram_id": telegram_id,
            "username": f"@{telegram_username}" if not telegram_username.startswith("@") else telegram_username
        }

        # Insert user
        self.db["telegram_users"].insert_one(user_doc)

        # Add user to the team's members array
        self.db["teams"].update_one(
            {"name": team},
            {"$push": {"members": user_doc}}
        )
