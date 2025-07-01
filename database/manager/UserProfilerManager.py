from singleton import singleton

@singleton
class UserProfilerManager:

    def getUsers(self,connection):
        query = "SELECT * FROM userprofile;"
        if not connection:
            print("connection is None")
            return None
        return connection.execute(query)
        

