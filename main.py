from fastapi import FastAPI
import datetime

from starlette.middleware.cors import CORSMiddleware

from services.mangodb_service.queries import news_by_dates, count_topics, get_total_articles, count_each_topic

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# default route
@app.get("/")
def welcome():
    return {"Hello"}


@app.get("/getLastNews/{number}")
def index(number: int):
    current_datetime = datetime.datetime.now()

    last_10_days = current_datetime - datetime.timedelta(days=number)

    dic_news = news_by_dates(last_10_days, current_datetime)
    return dic_news


@app.get("/top1")
def top1():
    return count_topics()


@app.get('/totalcount')
def total():
    return dict(get_total_articles())

@app.get('/allkeywords')
def allkeys():
    return count_each_topic()
