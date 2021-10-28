import time, random
from config.source import telescap_db, ServerConfig
from telethon.tl.functions.channels import JoinChannelRequest
from apps.telejoiner.engine.tel_groupsfinder import GroupsFinder
from telethon.tl.functions.messages import ImportChatInviteRequest
from apps.telejoiner.engine.tel_sessionmanager import SessionManager


class JoinEntities:
    def __init__(self, configs):
        self.isgroup = configs["isGroup"]
        self.username = configs["username"]
        self.targetid = str(configs["link"])

    @property
    def targetAccounts(self):
        return list(telescap_db.telegramaccounts.find({"username": self.username}, {"_id": 0}))

    @property
    def targetEntityId(self):
        return GroupsFinder({"query": self.targetid}).getGroupLink() if self.targetid.endswith(".dhtml") else self.targetid

    @ServerConfig.asynchronous
    async def joinTarget(self):
        ServerConfig.sendlogs(self.username, f"=== starting process ===")
        telegramaccounts = self.targetAccounts
        ServerConfig.sendlogs(self.username, f"=== targeting {len(telegramaccounts)} accounts ===")
        for account in telegramaccounts:
            try:
                targetId = self.targetEntityId.rsplit('/', 1)[-1]
                client = SessionManager(account).client
                await client.connect()
                if self.isgroup:
                    target = await client.get_entity(targetId)
                    await client(JoinChannelRequest(target))
                else:
                    target = await client(ImportChatInviteRequest(targetId))
                await client.disconnect()
                ServerConfig.sendlogs(self.username, f"=== {account['name']} has joined {target.title} ===")
                time.sleep(random.uniform(10, 30))
            except Exception as error:
                ServerConfig.sendlogs(self.username, str(error))
                break
        ServerConfig.sendlogs(self.username, "=== Finished Joining ===")