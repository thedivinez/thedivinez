from telejoiner.engine.tel_entitymanager import JoinEntities
from telejoiner.config.source import ServerConfig as task


class Instances:
    @staticmethod
    @task.asynchronous
    async def startjoining(account):
        await JoinEntities(account).joinTarget()
