from config.source import telescap_db


class TelegramAccounts:
    @staticmethod
    def telegramaccounts(user):
        allaccounts = list(telescap_db.telegramaccounts.find({"username": user.get("username")}, {'_id': 0}))
        return {"accounts": allaccounts}

    @staticmethod
    def addtelegramaccount(data: dict):
        for unwanted in ["EIO", "transport"]:
            data.pop(unwanted)
        if not telescap_db.telegramaccounts.find_one(data):
            telescap_db.telegramaccounts.insert_one(data)
        return {"status": "success", "message": f"New {data.get('type')} added."}

    def deletetelegramaccount(data: dict):
        return telescap_db.sessions.delete_one(data)
