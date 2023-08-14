import datetime

import matplotlib.pyplot as plt

from services.mangodb_service.queries import news_by_dates

current_datetime = datetime.datetime.now()

last_10_days = current_datetime - datetime.timedelta(days=10)
# date1 = datetime(2023, 7, 20)
# date2 = datetime(2023, 7, 27)


dic_news = news_by_dates(last_10_days, current_datetime)

# Extract keys and values from the dictionary
categories = list(dic_news.keys())
values = list(dic_news.values())

# Create a bar chart
plt.bar(categories, values)

# Add labels and title
plt.xlabel('Days')
plt.ylabel('News')
plt.title('Aljazeera')

# Rotate x-axis labels for better readability
plt.xticks(rotation=50)

# Display the chart
plt.show()
