import pymongo

uri = "mongodb+srv://rehanshaikh02269:REHAN123@cluster0.nuvotwa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(uri)
print(client.list_database_names())
