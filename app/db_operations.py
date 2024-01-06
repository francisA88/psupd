import pymongo
import os
import hashlib
from pathlib import Path

from dotenv import load_dotenv

ENV_FILE = Path(__file__).parent.parent / 'variables.env'
print(ENV_FILE)
load_dotenv(ENV_FILE)

MONGO_PWD = os.getenv('MONGO_PWD')

uri = f'mongodb+srv://francium:{MONGO_PWD}@cluster0.rrjp4ls.mongodb.net/?retryWrites=true&w=majority'

conn = pymongo.MongoClient(uri)
db = conn['portfolio_database']
collection = db['portdb']

def match_api_key(key:str):
    stored_hash_key = collection.find_one({'_id': 3}) #Let the hashed key document have a _id value of 3.
    hashed_key = hashlib.sha256(key.encode()).hexdigest()
    
    print(dir(stored_hash_key))
    return hashed_key == stored_hash_key['key']

def update_cv_link(link:str) -> bool:
    query = {'_id': 123}
    try:
        collection.update_one(query, {'$set': {'cv_link': link}}, upsert=True)
        return True
    except Exception as error:
        print(error)
        return False

def add_skill(initials, name, description):
    '''
    Function used to add a skill to my MongoDB database.

    All skills should be in this format
    {
        name: '',
        initials: '',
        description: '',
        belongs_to: 'skills'
    }
    '''
    try:
        collection.insert_one({
            'name': name,
            'initials': initials,
            'description': description,
            'belongs_to': 'skills'
        })
        return True
    except Exception as error:
        return False


def add_project(name, b64_image, link, description):
    '''
    Adds a project to the MongoDB database.

    All projects should be in this format
    {
        name: '',
        link: '',
        b64_image: '',
        description: '',
        belongs_to: 'projects'
    }'''
    try:
        collection.insert_one({
            'name': name,
            'b64_image': b64_image,
            'link': link,
            'description': description,
            'belongs_to': 'projects'
        })
        return True
    except Exception as error:
        print(error)
        return False
    

if __name__ == '__main__':
    pass
    
