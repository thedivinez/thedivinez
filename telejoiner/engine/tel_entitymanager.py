import time, random
from config.source import telescap_db, ServerConfig
from telethon.tl.functions.channels import JoinChannelRequest
from telejoiner.engine.tel_sessionmanager import SessionManager
from telethon.tl.functions.messages import ImportChatInviteRequest


class JoinEntities:
    def __init__(self, configs):
        self.isgroup = configs["isGroup"]
        self.username = configs["username"]
        self.targetid = configs["link"].rsplit('/', 1)[-1]

    @property
    def targetAccounts(self):
        return list(telescap_db.telegramaccounts.find({"username": self.username}, {"_id": 0}))

    @ServerConfig.asynchronous
    async def joinTarget(self):
        ServerConfig.sendlogs(self.username, f"=== starting process ===")
        telegramaccounts = self.targetAccounts
        ServerConfig.sendlogs(self.username, f"=== targeting {len(telegramaccounts)} accounts ===")
        for account in telegramaccounts:
            try:
                client = SessionManager(account).client
                await client.connect()
                if self.isgroup:
                    target = await client.get_entity(self.targetid)
                    await client(JoinChannelRequest(target))
                else:
                    target = await client(ImportChatInviteRequest(self.targetid))
                await client.disconnect()
                ServerConfig.sendlogs(self.username, f"=== {account['name']} has joined {target.title} ===")
                time.sleep(random.uniform(10, 30))
            except Exception as error:
                ServerConfig.sendlogs(self.username, str(error))
        ServerConfig.sendlogs(self.username, "=== Finished Joining ===")
