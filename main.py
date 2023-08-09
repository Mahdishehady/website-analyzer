from fastapi import FastAPI
import datetime

from starlette.middleware.cors import CORSMiddleware

import noSQL

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def welcome():
    return {"Hello"}


@app.get("/getLastNews/{number}")
def index(number: int):
    current_datetime = datetime.datetime.now()

    last_10_days = current_datetime - datetime.timedelta(days=number)

    dic_news = noSQL.news_by_dates(last_10_days, current_datetime)
    return dic_news


@app.get("/top1")
def top1():
    return noSQL.count_topics()
