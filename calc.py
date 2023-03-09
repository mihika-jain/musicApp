import database
from pymongo import MongoClient 

def get_totals(collection, track_arg):
    '''
        calculate weight of a certain track_arg
        arg is a string that is a track attribute: ex: danceability
    '''
    total = 0
    
    # iterate through collection
    for track in collection.find():
        avg_place = track['total_pos'] / track['time']
        weight = (1 / avg_place) * ((1 - track[track_arg]) ** (1/(100-track['place'])))
        total += weight

    return total

# ----------------------------------------------------------------------

def get_total_args(track_collection):
    '''
        go through values that are 0 to 1 for each top 100 songs and use get_weight to find the value for the combined list
    '''
    total_vals = {}
    total_vals['energy_total'] = get_totals(track_collection, 'energy') # perceptual measure of intensity and activity
    total_vals['danceability_total'] = get_totals(track_collection, 'danceability') # how suitable a track is for dancing
    total_vals['speechiness_total'] = get_totals(track_collection, 'speechiness') # the presence of spoken words in a track
    total_vals['acousticness_total'] = get_totals(track_collection, 'acousticness') # confidence measure of whether the track is acoustic
    total_vals['instrumentalness_total'] = get_totals(track_collection, 'instrumentalness') # predicts whether a track contains no vocals
    total_vals['liveness_total'] = get_totals(track_collection, 'liveness') # the presence of an audience in the recording
    total_vals['valence_total'] = get_totals(track_collection, 'valence') # measure describing the musical positiveness

    db = database.get_database()
    trends_collection = db['trends']
    trends_collection.insert_one(total_vals)

db = database.get_database()
track_collection = db['top100']
get_total_args(track_collection)