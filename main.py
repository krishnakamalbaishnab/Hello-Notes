from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from pymongo import MongoClient

app = FastAPI()



conn = MongoClient("mongodb+srv://krishnakamalbaishnab:Databaseaccount%4002@cluster0.i7n38c5.mongodb.net")







