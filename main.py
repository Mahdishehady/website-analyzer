from fastapi import FastAPI
import datetime

from starlette.middleware.cors import CORSMiddleware

from services.mangodb_service.queries import news_by_dates, count_topics, get_total_articles, count_each_topic, \
    get_Ranged_data, searchForSubstring

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


@app.get("/getNewsByDate/{datestr}")
def react(datestr: str):
    array = datestr.split('-')

    intarray_from = array[0].split(',')
    intarray_to = array[1].split(',')

    # Convert the date components to integers
    day_from = int(intarray_from[0])
    month_from = int(intarray_from[1])
    year_from = int(intarray_from[2])

    day_to = int(intarray_to[0])
    month_to = int(intarray_to[1])
    year_to = int(intarray_to[2])

    # Create datetime objects
    date_from = datetime.datetime(year_from, month_from, day_from)
    date_to = datetime.datetime(year_to, month_to, day_to)

    dic_news = news_by_dates(date_from, date_to)
    return dic_news


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
    array = []
    dict = get_total_articles()
    array.append(dict['total'])
    return array


@app.get('/allkeywords')
def allkeys():
    return count_each_topic()


@app.get('/contentCount')
def contentCount():
    return get_Ranged_data()


@app.get('/articles/{keyword}')
def getArticles(keyword: str):
    return searchForSubstring(keyword)
