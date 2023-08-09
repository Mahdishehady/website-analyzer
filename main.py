from fastapi import FastAPI
import datetime

from starlette.middleware.cors import CORSMiddleware

import noSQL

current_datetime = datetime.datetime.now()

last_10_days = current_datetime - datetime.timedelta(days=10)

dic_news = noSQL.news_by_dates(last_10_days, current_datetime)


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


@app.get("/getLastNews")
def index():
    return dic_news
