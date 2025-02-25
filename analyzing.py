import re
import nltk
nltk.download('wordnet')
import pandas as pd
import os
os.getcwd()
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from preprocess import preprocess
from wordcloud import WordCloud, ImageColorGenerator


# download Putin tweets dataset
file = pd.read_csv('putin_test_dataset.csv')
texts = file['Text'].tolist()

# download 140 dataset
dataset_columns  = ["sentiment", "ids", "date", "flag", "user", "text"]
dataset_encoding = "ISO-8859-1"
file2 = pd.read_csv('training.1600000.processed.noemoticon.csv',
                      encoding=dataset_encoding , names=dataset_columns)
texts2 = file2['text'].tolist()

# download Russia dataset
file3 = pd.read_csv('nltk_labeled_invade.csv')
texts3 = file3['Text'].tolist()

# preprocess Putin tweets dataset
processedText = preprocess(texts)
data = pd.DataFrame(processedText)
data.columns = ['Text']

# preprocess 140 tweets dataset
processedText2 = preprocess(texts2)

# preprocess Russia tweets dataset
processedText3 = preprocess(texts3)
data2 = pd.DataFrame(processedText3)
data2.columns = ['Text']
data2.insert(data2.shape[1], 'Labels', file3['Labels'])

# calculate sentiment score with nltk
sentiments = SentimentIntensityAnalyzer()
data["Positive"] = [sentiments.polarity_scores(i)["pos"] for i in data["Text"]]
data["Negative"] = [sentiments.polarity_scores(i)["neg"] for i in data["Text"]]
data["Neutral"] = [sentiments.polarity_scores(i)["neu"] for i in data["Text"]]
data = data[["Text", "Positive", "Negative", "Neutral"]]

# label the texts according to the scores
data["Labels"] = [0 if row['Negative'] > row['Positive'] and row['Negative'] > row['Neutral'] else 1 for idx, row in data.iterrows()]

# download labeled dataset
data.to_csv('nltk_labeled_tweets.csv')

# create word cloud plot and print out the most frequent words
def createwordcloud(text):
    wordcloud= WordCloud(max_words=1000, width=1600, height=800,
                   collocations=False,background_color="white").generate(''.join(text))
    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    print(wordcloud.words_.keys())

# putin tweets
putin_non_negative= data.loc[data['Labels'] == 1]['Text'].tolist()
putin_negative = data.loc[data['Labels'] == 0]['Text'].tolist()

createwordcloud(putin_non_negative)
createwordcloud(putin_negative)

# 140 dataset (the first 800000 data are labeled as negative, and the rest are labeled as non-negative)
non_negative_140 = processedText2[800000:]
negative_140 = processedText2[:800000]
createwordcloud(non_negative_140)
createwordcloud(negative_140)

# Russia tweets
russia_non_negative= data2.loc[data2['Labels'] == 1]['Text'].tolist()
russia_negative = data2.loc[data2['Labels'] == 0]['Text'].tolist()

createwordcloud(russia_non_negative)
createwordcloud(russia_negative)


