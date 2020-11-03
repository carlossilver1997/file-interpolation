from fastapi import APIRouter, Body, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from typing import Optional
from files import read_and_interpolate_file, sendEmail
from starlette.responses import FileResponse
import os

from app.server.database import (
    add_person,
    delete_person,
    retrieve_people,
    retrieve_person,
    update_person
)
from app.server.models.person import (
    ErrorResponseModel,
    ResponseModel,
    PersonSchema,
    UpdatePersonModel,
)


router = APIRouter()


@router.post("/", response_description="Person data added into the database")
async def add_person_data(person: PersonSchema = Body(...)):
    person = jsonable_encoder(person)
    new_person = await add_person(person)
    return ResponseModel(new_person, "Person added successfully.")


@router.get("/", response_description="People retrieved")
async def get_people():
    people = await retrieve_people()
    if people:
        return ResponseModel(people, "People data retrieved successfully")
    return ResponseModel(people, "Empty list returned")


@router.get("/{id}", response_description="Person data retrieved")
async def get_person_data(id):
    person = await retrieve_person(id)
    if person:
        return ResponseModel(person, "Person data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Person doesn't exist.")


@router.put("/{id}")
async def update_person_data(id: str, req: UpdatePersonModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_person = await update_person(id, req)
    if updated_person:
        return ResponseModel(
            "Person with ID: {} name update is successful".format(id),
            "Person name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the person data.",
    )


@router.delete("/{id}", response_description="Person data deleted from the database")
async def delete_person_data(id: str):
    deleted_person = await delete_person(id)
    if deleted_person:
        return ResponseModel(
            "Person with ID: {} removed".format(id), "Person deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Person with id {0} doesn't exist".format(id)
    )


@router.post("/write-files/{id}", response_description="Generate file in pdf, txt, or word")
async def get_person_data(id, ext):
    person = await retrieve_person(id)
    if person:
        read_and_interpolate_file('./carta_agradecimiento.txt', person, ext)
        cwd = os.getcwd()
        return FileResponse("{}/static/{}.{}".format(cwd,id,ext))
    return ErrorResponseModel("An error occurred.", 404, "Person doesn't exist.")

@router.post("/send-email/{id}", response_description="Send email")
async def get_person_data(background_tasks: BackgroundTasks,id):
    person = await retrieve_person(id)
    if person:
        sendEmail(background_tasks,'./carta_agradecimiento.txt',person)
        return ResponseModel(person, "Person data retrieved successfully")

    return ErrorResponseModel("An error occurred.", 404, "Person doesn't exist.")

@router.get("/write-files/all", response_description="Generate documents for each person")
async def get_people():
    people = await retrieve_people()
    cwd = os.getcwd()
    if people:
        files = []
        for person in people:
            read_and_interpolate_file('./carta_agradecimiento.txt', person, 'txt')
            files.append(FileResponse("{}/static/{}.{}".format(cwd,person["id"],'txt')))
        return files
    return ResponseModel(people, "Empty list returned")