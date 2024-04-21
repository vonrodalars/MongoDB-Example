# imports.py
from pymongo import MongoClient
from gridfs import GridFS
import json, io, requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# database setup
def connect_to_mongodb(db_name='Pokemon', collection_name='pokedex'):
    """
    Connect to MongoDB and return the collection object.
    """
    client = MongoClient(f'mongodb://mongodbuser:example@localhost:27019/?authMechanism=DEFAULT')
    db = client[db_name]
    collection = db[collection_name]
    return collection, db


def download_and_store_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return fs.put(response.content)
    else:
        return None


def import_json_to_mongodb(collection, json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        for pokemon in data['pokemon']:
            image_id = download_and_store_image(pokemon['img'])
            if image_id:
                pokemon['image_id'] = image_id
            del pokemon['img']  # Optional: remove the image URL if not needed
            collection.insert_one(pokemon)


def load_image_from_mongodb(collection, pokedex_id):
    """
    Load an image from MongoDB using a specific Pokedex ID.
    """
    pokemon = collection.find_one({'num': pokedex_id})
    image_id = pokemon['image_id']
    image_data = fs.get(image_id).read()

    return image_data


def show(collection, pokedex_id="001"):
    image_data = load_image_from_mongodb(collection, pokedex_id)  # Replace pokedex_id with the actual ID
    img = mpimg.imread(io.BytesIO(image_data))
    plt.imshow(img)
    plt.axis('off')
    plt.show()



# Main execution
collection, db = connect_to_mongodb()
fs = GridFS(db)
#import_json_to_mongodb(collection, 'pokedex.json')
show(collection, "012")
