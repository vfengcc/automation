import pymongo
from pymongo.collection import Collection

client = pymongo.MongoClient(host='localhost', port=27017)
db = client['douyin']

def handler_init_task():
    task_id_collection = Collection(db, 'task_id')
    with open('douyin_id.txt') as f:
        for id in f.readlines():
            init_task = {}
            init_task['share_id'] = id.strip()
            task_id_collection.insert_one(init_task)


def handler_get_task():
    task_id_collection = Collection(db, 'task_id')
    return task_id_collection.find_one_and_delete({})

if __name__ == '__main__':
    handler_init_task()