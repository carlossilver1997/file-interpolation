import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config
from utils.util import calculateAge

MONGO_DETAILS = config('MONGO_URI')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.person

person_collection = database.get_collection("person_collection")

def person_helper(person) -> dict:
    return {
        "id": str(person["_id"]),
        "email": person["email"],
        "givenNames": person["givenNames"],
        "lastName1": person["lastName1"],
        "lastName2": person["lastName2"],
        "position": person["position"],
        "company": person["company"],
        "phoneNumber": person["phoneNumber"],
        "birthDate": person["birthDate"],
        "address": person["address"],
        "age": calculateAge(person["birthDate"]),
    }

# Retrieve all people present in the database
async def retrieve_people():
    people = []
    async for person in person_collection.find():
        people.append(person_helper(person))
    return people


# Add a new person into to the database
async def add_person(person_data: dict) -> dict:
    person = await person_collection.insert_one(person_data)
    new_person = await person_collection.find_one({"_id": person.inserted_id})
    return person_helper(new_person)


# Retrieve a person with a matching ID
async def retrieve_person(id: str) -> dict:
    person = await person_collection.find_one({"_id": ObjectId(id)})
    if person:
        return person_helper(person)


# Update a person with a matching ID
async def update_person(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    person = await person_collection.find_one({"_id": ObjectId(id)})
    if person:
        updated_person = await person_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if update_person:
            return True
        return False


# Delete a person from the database
async def delete_person(id: str):
    person = await person_collection.find_one({"_id": ObjectId(id)})
    if person:
        await person_collection.delete_one({"_id": ObjectId(id)})
        return True