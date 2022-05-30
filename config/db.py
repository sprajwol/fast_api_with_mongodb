from pymongo import MongoClient

from models.user import ROLES_M

conn = MongoClient("mongodb://localhost:27017")
db=conn.get_database(name='pymongo')
print("db", db)
print("exists coll", db.get_collection('user'))
# if not conn.collectionExists('user'):

# db = conn.
print(db)
user_vexpr = {
    "$jsonSchema":
    {
        "bsonType": "object",
        "required": ["email", "password", "role"],
        "properties": {
            "email": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "password": {
                "bsonType": "string",
                "description": "must be a string and is not required"
            },
            "role": {
                "enum": [e.value for e in ROLES_M],
                "description": "can only be one of the enum values and is required"
            }
        }
    }
}

db.command('collMod', 'user', validator=user_vexpr, validationLevel='moderate')
