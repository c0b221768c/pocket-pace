import bcrypt


def hash_password(password: str) -> str:
    """
    パスワードをbcryptでハッシュ化する（ソルト付き）
    """
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    入力されたプレーンパスワードが、ハッシュと一致するかを検証する
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )
