# minds_assignment
Data:
- Data(messages) was obtained from a crypto group on telegram between the dates 05/01/2021 and 05/15/2021 (inclusive)

Preprocessing:
- First, the message data is cleaned to remove hyperlinks, brackets and digits from messages.
- Then the data was analyzed using the library 'langdetect' and messages in english language were extracted.
- Then only the messages containing "SHIB" or "DOGE" were extracted.

Sentiment Analysis:
- TextBlob library was used to perform the sentiment analysis.
- This library function outputs a sentiment score for each message, where '>0' is considered as positive, '0' is considered neutral and '<0' is considered negative emotion.

Results:
- The total number of messages, positive, negative, and neutral sentiments, and average sentiment score per day are extracted into a dataframe.
- Plotly is used to plot average sentiment score vs Date and Number of messages per day vs Date

