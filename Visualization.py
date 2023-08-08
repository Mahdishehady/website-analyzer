from datetime import datetime

import matplotlib.pyplot as plt
import noSQL

date1 = datetime(2023, 7, 20)
date2 = datetime(2023, 7, 27)
print(str(date1.date()))

dic_news = noSQL.news_by_dates(date1, date2)

# Extract keys and values from the dictionary
categories = list(dic_news.keys())
values = list(dic_news.values())

# Create a bar chart
plt.bar(categories, values)

# Add labels and title
plt.xlabel('Days')
plt.ylabel('News')
plt.title('News/Days')

# Rotate x-axis labels for better readability
plt.xticks(rotation=50)

# Display the chart
plt.show()
