from pymongo import MongoClient

client = MongoClient("mongodb+srv://Navya:22371-Cm-058@thundercluster.irbjytt.mongodb.net/?appName=Thundercluster")
db = client["studentslist_db"]
collection = db["Students"]
