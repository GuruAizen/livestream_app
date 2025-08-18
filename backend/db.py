from pymongo import MongoClient
from bson import ObjectId

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["claimss"]
overlays = db["overlays"]

def create_overlay(data):
    """Create a new overlay document in MongoDB."""
    if not data.get('position') or not data.get('size'):
        raise ValueError("Position and size are required")
    result = overlays.insert_one(data)
    return str(result.inserted_id)

def get_overlays():
    """Retrieve all valid overlays from MongoDB."""
    try:
        return list(overlays.find(
            { "position": { "$exists": True }, "size": { "$exists": True } },
            { '_id': 0, 'id': { '$toString': '$_id' }, 'type': 1, 'content': 1, 'position': 1, 'size': 1 }
        ))
    except Exception as e:
        raise RuntimeError(f"Failed to fetch overlays: {str(e)}")

def update_overlay(id, data):
    """Update an overlay document by ID."""
    try:
        result = overlays.update_one({"_id": ObjectId(id)}, {"$set": data})
        return result.modified_count > 0
    except bson.errors.InvalidId:
        raise ValueError("Invalid ID format")
    except Exception as e:
        raise RuntimeError(f"Failed to update overlay: {str(e)}")

def delete_overlay(id):
    """Delete an overlay document by ID."""
    try:
        result = overlays.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
    except bson.errors.InvalidId:
        raise ValueError("Invalid ID format")
    except Exception as e:
        raise RuntimeError(f"Failed to delete overlay: {str(e)}")