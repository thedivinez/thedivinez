from config.source import ServerConfig as task
from apps.telejoiner.engine.tel_entitymanager import JoinEntities


class Instances:
    @staticmethod
    @task.asynchronous
    async def startjoining(account):
        await JoinEntities(account).joinTarget()
