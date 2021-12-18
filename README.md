# minds_assignment
Data:
- Data(messages) was obtained from a crypto group on telegram between the dates 05/01/2021 and 05/15/2021 (inclusive)

Preprocessing:
- First, the data was cleaned to get rid of unnecessary characters.
- Then the data was analyzed using the library 'langdetect' to check if the messages are in english or not.
- The messages were then filtered so that the dataset contained messages with 'SHIB' or 'DOGE' in them.

Sentiment Analysis:
- TextBlob library was used to perform the sentiment analysis.
- This library function outputs a score where '>0' is considered as positive, '0' is considered neutral and '<0' is considered negative emotion.

Results:
- The total number of messages, positive, negative, and neutral sentiments, and average sentiment score per day are extracted into a dataframe.
- Plotly is used to plot the 3D graph of Date vs Number of messages vs average sentiment score.
- ![day_wise_3d](https://user-images.githubusercontent.com/20417069/146626673-1795ea8c-9d93-4478-9209-86886aea4f02.png)
