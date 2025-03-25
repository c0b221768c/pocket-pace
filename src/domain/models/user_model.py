class UserModel:
    def __init__(self, db):
        self.db = db

    async def create_user(self, name, email, hashed_password):
        await self.db.execute(
            "INSERT INTO users (name, email, password) VALUES ($1, $2, $3)",
            name,
            email,
            hashed_password,
        )

    async def get_user_by_identifier_and_password(self, identifier, hashed_password):
        rows = await self.db.fetch(
            """
            SELECT id, name FROM users
            WHERE (email = $1 OR name = $1) AND password = $2
            """,
            identifier,
            hashed_password,
        )
        return rows[0] if rows else None

    async def get_user_by_email_and_password(self, email, hashed_password):
        rows = await self.db.fetch(
            "SELECT id, name FROM users WHERE email = $1 AND password = $2",
            email,
            hashed_password,
        )
        return rows[0] if rows else None

    async def get_user_by_email(self, email):
        rows = await self.db.fetch(
            "SELECT id, name, password FROM users WHERE email = $1",
            email,
        )
        return rows[0] if rows else None

    async def update_user_name(self, user_id: int, new_name: str):
        await self.db.execute(
            "UPDATE users SET name = $1 WHERE id = $2", new_name, user_id
        )

    async def update_email(self, user_id: int, new_email: str):
        await self.db.execute(
            "UPDATE users SET email = $1 WHERE id = $2", new_email, user_id
        )

    async def update_password(self, user_id: int, hashed_password: str):
        await self.db.execute(
            "UPDATE users SET password = $1 WHERE id = $2", hashed_password, user_id
        )

    async def get_by_id(self, user_id: int):
        rows = await self.db.fetch(
            "SELECT * FROM users WHERE id = $1",
            user_id,
        )
        return rows[0] if rows else None

    async def get_by_identifier(self, identifier: str):
        query = """
            SELECT * FROM users
            WHERE email = $1 OR name = $1
            LIMIT 1
        """
        rows = await self.db.fetch(query, identifier)
        return rows[0] if rows else None
