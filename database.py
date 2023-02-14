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
    global avg_dance
    global avg_ener

    db = get_database()
    # maybe if we're getting date automatically need a parse
    collection = db['top100']

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

# def calculate_averages(track, count):


# ----------------------------------------------------------------------

# # This is added so that many files can reuse the function get_database()
# if __name__ == "__main__":   
#    # Get the database
# # db_name = get_database()


# ----------------------------------------------------------------------
# testing

print(avg_dance)
print(avg_ener)
# delete_whole_collection()