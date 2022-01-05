import json
import pandas as pd
import re
from tqdm import tqdm
import langdetect as ld
from textblob import TextBlob
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict

tqdm.pandas()


def clean_text(txt):
    """
    Returns the modified text after removing digits, brackets and hyperlinks

            Parameters:
                    txt (str): A string of sentence(s)

            Returns:
                    txt (str): Modified string
    """
    txt = ' '.join(
        re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)|{.*?}|[\([{})\]]", " ", str(txt)).split())
    return txt


def is_english(txt):
    """
    Returns True if text is in plain english

            Parameters:
                    txt (str): A string of sentence(s)

            Returns:
                    True (bool): if text is in plain english
                    False (bool): otherwise
    """
    try:
        return ld.detect(txt) == 'en'
    except:
        return False


def filter_messages(txt):
    """
    Returns True if the text contains 'SHIB' or 'DOGE'

            Parameters:
                    txt (str): A string of sentence(s)

            Returns:
                    True (bool): if text contains 'SHIB' or 'DOGE'
                    False (bool): otherwise
    """
    words = re.compile('shib|doge')
    if words.search(str(txt).lower()):
        return True
    return False


def sentiment_analysis(txt):  # Function to analyze the sentiment of the message
    """
    Returns a Pandas Series containing the sentiment and sentiment score of the text

            Parameters:
                    txt (str): A string of sentence(s)

            Returns:
                    Pandas Series: sentiment(string) and sentiment score(float)
    """
    result = TextBlob(str(txt))
    polarity = result.sentiment.polarity
    if polarity > 0:
        return pd.Series(['positive', polarity])
    elif polarity == 0:
        return pd.Series(['neutral', polarity])
    else:
        return pd.Series(['negative', polarity])


def extract_day_wise_data(mod_data):
    """
    Returns a dictionary consisting of day wise sentiment analyses

            Parameters:
                    Pandas dataframe: dataframe with sentiment scores

            Returns:
                    text (str): dictionary consisting of day wise sentiment analyses
    """
    h_map = defaultdict(lambda: defaultdict(int))
    for index, row in mod_data.iterrows():
        date = row['date'].partition('T')[0]
        sentiment = row['sentiment']
        score = row['sentiment_score']
        h_map[date][sentiment] += 1
        h_map[date]['total'] += 1
        h_map[date]['total_score'] += score
    return h_map


def plot_data(day_wise_df):
    """
    Plots the day wise sentiment analyses and saves them in '.png' format

            Parameters:
                    Pandas dataframe: dataframe with day wise sentiment scores

            Returns:
                    None
    """
    avg_score_line = px.line(day_wise_df, x='date', y='avg_score')  # Line plot
    avg_score_scatter = px.scatter(day_wise_df, x='date', y='avg_score', color="avg_score")  # Scatter plot
    layout = go.Layout(
        title='Average Sentiment Score per day vs Date ',
        xaxis=dict(
            title='Date',
            tickmode='linear'),
        yaxis=dict(title='Average sentiment score'))
    avg_score = go.Figure(data=avg_score_line.data + avg_score_scatter.data,
                          layout=layout)  # combine line and scatter plots
    avg_score.show()
    avg_score.write_image("score_vs_days.png")

    daily_messages_line = px.line(day_wise_df, x='date', y='total')  # Line plot
    daily_messages_scatter = px.scatter(day_wise_df, x='date', y='total', color="total")  # Scatter plot
    layout2 = go.Layout(
        title='Total number of messages per day vs Date ',
        xaxis=dict(
            title='Date',
            tickmode='linear'),
        yaxis=dict(title='Number of messages'))
    daily_messages = go.Figure(data=daily_messages_line.data + daily_messages_scatter.data,
                               layout=layout2)  # combine line and scatter plots
    daily_messages.show()
    daily_messages.write_image("messages_vs_days.png")


def prepare_data(raw_data):
    """
    Return modified dataframe after cleaning and extracting the required data

            Parameters:
                    Pandas dataframe: raw data

            Returns:
                    Pandas dataframe: processed data
    """
    print("Removing hyperlinks, brackets and digits from messages", flush=True)
    raw_data['message_copy'] = raw_data['text'].progress_apply(clean_text)
    print("\n\nExtracting english messages from the data", flush=True)
    raw_data = raw_data[raw_data['message_copy'].progress_apply(is_english)]
    print("\n\nExtracting english messages which consists of \"SHIP\" or \"DOGE\"", flush=True)
    raw_data = raw_data[raw_data['message_copy'].progress_apply(filter_messages)]
    return raw_data


def analyze_data(processed_data):
    """
    Return a dataframe consisting of day wise sentiment analyses

            Parameters:
                    Pandas dataframe: processed data

            Returns:
                    Pandas dataframe: day wise data with sentiment analyses
    """
    cols = ['sentiment', 'sentiment_score']
    print("\n\nPerforming Sentiment analysis and extracting the day wise average sentiment score", flush=True)
    processed_data[cols] = processed_data['message_copy'].progress_apply(sentiment_analysis)
    day_map = extract_day_wise_data(processed_data)
    day_wise_df = pd.DataFrame.from_dict(day_map, orient='index')
    day_wise_df['avg_score'] = round(day_wise_df['total_score'] / day_wise_df['total'], 4)
    day_wise_df['date'] = day_wise_df.index
    return day_wise_df


if __name__ == "__main__":
    with open('messages.json', 'r', encoding='utf8') as f:
        data = json.loads(f.read())  # load data using Python JSON module

    df_messages = pd.json_normalize(data, record_path=['messages'])  # save the messages in a dataframe

    modified_data = prepare_data(df_messages)  # Preprocess message data
    analyzed_data = analyze_data(modified_data)  # Perform sentiment analysis
    plot_data(analyzed_data)  # Plot the graphs
