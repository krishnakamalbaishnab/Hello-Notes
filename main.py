from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

conn = MongoClient("mongodb+srv://krishnakamalbaishnab:Databaseaccount%4002@cluster0.i7n38c5.mongodb.net")



@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = conn.hellonotes.notes.find({})
    newDocs =[]
    for doc in docs:
        newDocs.append({
            "id": doc["_id"],
            "note" : doc["note"]
        })
    return templates.TemplateResponse("index.html", {"request": request, "newDocs":newDocs})


@app.get("/")
async def root():
    return {"message": "Hello World"}

