from pymongo import MongoClient

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   print("a")
   CONNECTION_STRING = "mongodb+srv://REDACTED_USER:REDACTED_PASSWORD@REDACTED_CLUSTER.mongodb.net/?retryWrites=true&w=majority"
 
   print("b")
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
   print("c")
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['billboardmusiclist']

def insert_item(item):
    print("d")
    dbname = get_database()
    print("e")
    # maybe if we're getting date automatically need a parse
    collection_name = dbname['top100']
    print("f")
    collection_name.insert_one(item)
    print("g")


# # This is added so that many files can reuse the function get_database()
# if __name__ == "__main__":   
#    # Get the database
#    dbname = get_database()