from pymongo import MongoClient
import json


def connect_to_mongodb(db_name='Harry_Potter', collection_name='characters1'):
    """
    Connect to MongoDB and return the collection object.
    """
    client = MongoClient(f'mongodb://mongodbuser:example@localhost:27019/?authMechanism=DEFAULT')
    db = client[db_name]
    collection = db[collection_name]
    return collection

def load_json_data(filepath):
    """
    Load data from JSON file.
    """
    with open(filepath, 'r') as file:
        data = json.load(file)
        return data['characters']


def import_data_to_mongodb_one_by_one(collection, data):
    """
    Import each data item into MongoDB collection one by one.
    """
    for item in data:
        try:
            collection.insert_one(item)
        except:
            print("Error on data %s \n\n\n\n" % item)


def import_json_to_mongodb(collection, data):
    """
    Import GeoJSON data into MongoDB collection.
    """
    result = collection.insert_many(data)
    return result


"""
data = load_json_data('potter.json')
collection = connect_to_mongodb()
import_data_to_mongodb_one_by_one(collection, data)

"""
data = load_json_data('potter_advanced.json')
collection = connect_to_mongodb('Harry_Potter', "characters2")
result = import_json_to_mongodb(collection, data)
print(f'Imported {len(result.inserted_ids)} records into MongoDB.')


