from config.source import telescap_db
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from apps.telejoiner.engine.tel_accounts import TelegramAccounts


class SessionManager:
    def __init__(self, data) -> None:
        self.data = data
        self.phone = data["phone"]
        self.api_id = data["apiId"]
        self.api_hash = data["apiHash"]

    @property
    def session(self):
        return telescap_db.sessions.find_one({"phone": self.phone})["session"]

    @property
    def client(self) -> TelegramClient:
        return TelegramClient(StringSession(self.session), self.api_id, self.api_hash)

    def deleteSession(self):
        telescap_db.sessions.delete_one({"phone": self.phone})
        return TelegramAccounts.deletetelegramaccount({"phone": self.phone})

    def createSession(self):
        client = TelegramClient(StringSession(), self.api_id, self.api_hash)
        client.connect()
        telegram_response = client.send_code_request(self.phone)
        if telegram_response.phone_code_hash:
            client.disconnect()
            return {"status": "sendcode", "code_hash": telegram_response.phone_code_hash}
        return {"status": "error", "message": "Failed to get code from telegram plese try again"}

    def verifyCode(self):
        try:
            client = self.client
            client.connect()
            self.client.sign_in(self.phone, int(self.data["code"]), phone_code_hash=self.data["code_hash"])
            telescap_db.sessions.insert_one({"phone": self.phone, "session": client.session.save()})
            del self.data["code"]
            del self.data["code_hash"]
            return TelegramAccounts.addtelegramaccount(self.data)
        except Exception:
            return {"status": "error", "message": "Incorrect code"}
        finally:
            client.disconnect()
