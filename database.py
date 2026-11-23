import os
from pymongo import MongoClient

# move these!
avg_dance = 0.0
avg_ener = 0.0

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = os.environ["MONGODB_URI"]  # see .env.example
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)

   # Create the database for our example (we will use the same database throughout the tutorial
   return client['billboardmusiclist']

# ----------------------------------------------------------------------

def insert_track(collection, track, count):
    '''
        inserts the track (dict) into the MongoDB database
        count is 
    '''

    # set new parameters
    track['update'] = 1
    track['place'] = count
    track['time'] = 1
    track['total_pos'] = count
    
    collection.insert_one(track)

# ----------------------------------------------------------------------

def delete_track(collection, track):
    collection.delete_one(track)

def delete_whole_collection(collection):
    collection.drop()

# ----------------------------------------------------------------------

def update_many(collection):
    '''
        given a collection, calls the update_many() API function
        Updates the update parameter 
        *maybe rename to avoid confusion
    '''
    collection.update_many(
        {}, 
        {'$set': {'update': 0}},
    )

def delete_not_updated(collection):
    '''
        delete all tracks from collection that haven't been updated
    '''
    collection.delete_many({'update': 0})

def contains(collection, track_id):
    ''' 
        return true if the collection contains the track ID
    '''
    return collection.find_one({'id': track_id})

def find_one_and_update(collection, track_id, count):
    ''' 
        use collection find nad update for track (updating place, etc.)
    '''
    collection.find_one_and_update(
        {'id': track_id}, 
        {'$set': {'place': count, 'update': 1}},
    )

    collection.find_one_and_update(
        {'id': track_id}, 
        {'$inc': {'time': 1, 'total_pos': count}},
    )

# ----------------------------------------------------------------------

# # This is added so that many files can reuse the function get_database()
# if __name__ == "__main__":   
#    # Get the database
# # db_name = get_database()


# ----------------------------------------------------------------------
# testing

# db = get_database()
# collection = db['top100']
# print(contains(collection, "02Zkkf2zMkwRGQjZ7T4p8f"))