import pymongo

from pymongo.collection import Collection


class Connect_mongo:
    def __init__(self):
        self.client = pymongo.MongoClient(host='192.168.100.106', port=27017)
        self.db_data = self.client['douguo']

    def insert_item(self, item):
        db_collectiopn = Collection(self.db_data, 'douguo')
        db_collectiopn.insert(item)


mongo_info = Connect_mongo()
