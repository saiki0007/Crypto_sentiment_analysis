# Summary
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
- ![score_vs_days](https://user-images.githubusercontent.com/20417069/148297086-814140bf-7e90-4798-8680-2cac70d7290e.png)
- ![messages_vs_days](https://user-images.githubusercontent.com/20417069/148297104-78a79814-528c-4e83-a798-5d1c3deb5a26.png)


# Running the code
- Install the packages in requirements.txt by running:
```
pip install -r requirements.txt
```
- Run the python file "crypto_sentiment_analysis" for results and plots:
```
python3 crypto_sentiment_analysis.py
```
- Note: Make sure to include "messages.json" in the same directory
