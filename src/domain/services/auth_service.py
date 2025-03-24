from domain.models.user_model import UserModel
from shared.security import hash_password


class AuthService:
    def __init__(self, db):
        self.user_model = UserModel(db)

    async def register_user(self, name, email, password):
        hashed_pw = hash_password(password)
        await self.user_model.create_user(name, email, hashed_pw)
        print(f"User {name} registered successfully!")

    async def login_user(self, identifier, password):
        hashed_pw = hash_password(password)
        user = await self.user_model.get_user_by_identifier_and_password(
            identifier, hashed_pw
        )
        if user:
            print(f"User {user['name']} logged in successfully!")
            return user["id"]
        else:
            print("Invalid email or username or password")
            return None

    async def change_user_name(self, user_id: int, new_name: str):
        await self.user_model.update_user_name(user_id, new_name)

    async def change_email(self, user_id: int, new_email: str):
        await self.user_model.update_email(user_id, new_email)

    async def change_password(self, user_id: int, current_pw: str, new_pw: str):
        user = await self.user_model.get_by_id(user_id)
        if not user or user["password"] != hash_password(current_pw):
            return False
        await self.user_model.update_password(user_id, hash_password(new_pw))
