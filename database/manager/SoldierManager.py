from singleton import singleton
from database.MysqlConnector import MysqlConnector
from database.manager.UserProfilerManager import UserProfilerManager

@singleton
class SoldierManager:
    def add_wounded_soldiers(self):
        query = "INSERT INTO user_hospital (uid, armyId, dead, heal, finishTime) VALUES (%s, %s, %s, %s, %s)"
        connector = MysqlConnector()
        connector.connect()
        users = UserProfilerManager().getUsers(connector)
        if users != None:
            user = users[0]
            connector.execute(query,(user["uid"], "3005", 233, 0, 0))
            connector.execute(query, (user["uid"], "3006", 51, 0, 0))
        connector.close()
        return {}