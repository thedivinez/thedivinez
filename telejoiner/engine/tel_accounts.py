from config.source import dbcursor


class TelegramAccounts:
    @staticmethod
    def telegramaccounts(user):
        allaccounts = list(dbcursor.telegramaccounts.find({"username": user.get("username")}, {'_id': 0}))
        return {"accounts": allaccounts}

    @staticmethod
    def addtelegramaccount(data: dict):
        for unwanted in ["EIO", "transport"]:
            data.pop(unwanted)
        if not dbcursor.telegramaccounts.find_one(data):
            dbcursor.telegramaccounts.insert_one(data)
        return {"status": "success", "message": f"New {data.get('type')} added."}

    def deletetelegramaccount(data: dict):
        return dbcursor.sessions.delete_one(data)
