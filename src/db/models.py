class User:
    def __init__(self, user_data: dict):
        self.tg_id: int = user_data["tg_id"]
        self.ban_list: list[dict] = user_data["ban_list"]
        self.info = {
            "username": user_data["username"],
            "state": user_data["notify"],
            "access": user_data["access"],
        }

    def get_ban_list(self) -> list[dict]:
        return self.ban_list
