import pymongo


class GPUDatabase():

    def __init__(self, url):
        self.connect(url)

    def connect(self, url):
        self.client = pymongo.MongoClient(url)
        self.db = self.client["gpustat"]

    def set_state(self, planet, gpu, users, time):
        col = self.db[planet]
        new_status = {
            "_id": gpu,
            "users": users,
            "time": time
        }
        query = {
            "_id": gpu
        }
        update = {
            "$set": new_status
        }
        if [*col.find(query)]:
            col.update_one(query, update)
        else:
            col.insert_one(new_status)
        return True
