import pandas as pd
import nltk
import string
import re
import matplotlib.pyplot as plt
import emoji
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
analyser = SentimentIntensityAnalyzer()


df = pd.read_csv("../blacklivesmatter.csv")


def extract_emojis(text):
  return ''.join(c for c in text if c in emoji.UNICODE_EMOJI)

df['Tweet_Emoji'] = df['Tweets'].apply(lambda x: extract_emojis(x))

def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    return score['compound']
  
df['Sentiment'] = df['Tweets'].apply(lambda x: sentiment_analyzer_scores(x))
df['Sentiment_Emoji'] = df['Tweet_Emoji'].apply(lambda x: sentiment_analyzer_scores(x))


print()


print(sentiment_analyzer_scores("❤"))
print(analyser.polarity_scores("💋 and 😁 "))