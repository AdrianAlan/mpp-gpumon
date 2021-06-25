import pymongo


class GPUDatabase():

    def __init__(self, url):
        self.connect(url)

    def connect(self, url):
        self.client = pymongo.MongoClient(url)
        self.db = self.client["gpustat"]
