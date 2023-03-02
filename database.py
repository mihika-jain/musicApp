from pymongo import MongoClient

# move these!
avg_dance = 0.0
avg_ener = 0.0

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://REDACTED_USER:REDACTED_PASSWORD@REDACTED_CLUSTER.mongodb.net/?retryWrites=true&w=majority"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)

   # Create the database for our example (we will use the same database throughout the tutorial
   return client['billboardmusiclist']

# ----------------------------------------------------------------------

def insert_track(track, count):
    '''
        inserts the track (dict) into the MongoDB database
        count is 
    '''
    global avg_dance
    global avg_ener

    db = get_database()
    # maybe if we're getting date automatically need a parse
    collection = db['top100']

    # set new parameters
    track['update'] = 0     # initialize to 0 (false)
    track['place'] = count  # initialize to count

    # calculate weighted averages
    avg_dance += track['danceability'] * (100-count)
    avg_ener += track['energy'] * (100-count)
    
    collection.insert_one(track)

# ----------------------------------------------------------------------

def delete_track(track):
    db = get_database()
    collection = db['top100']
    collection.delete_one(track)

def delete_whole_collection():
    db = get_database()
    db['top100'].drop()

# ----------------------------------------------------------------------

def update_many(collection):
    '''
        given a collection, calls the update_many() API function
        ** maybe rename this to reduce confusion
    '''
    collection.update_many({}, {'$set': {'update': 0}})

def delete_not_updated(collection):
    '''
        delete all tracks from collection tthat haven't been updated
    '''
    collection.delete_many({'update': 0})

def contains(collection, track_id):
    ''' 
        return true if the collection contains the track ID
    '''
    return collection.find_one({'id': track_id})

def find_one_and_update(collection, track_id):
    ''' 
        return true if the collection contains the track ID
    '''
    return collection.find_one_and_update({'id': track_id}, )

# ----------------------------------------------------------------------

# # This is added so that many files can reuse the function get_database()
# if __name__ == "__main__":   
#    # Get the database
# # db_name = get_database()


# ----------------------------------------------------------------------
# testing

db = get_database()
collection = db['top100']
# print(contains(collection, "02Zkkf2zMkwRGQjZ7T4p8f"))