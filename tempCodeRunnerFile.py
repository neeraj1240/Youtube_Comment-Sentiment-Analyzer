import re
import os
import nltk
import joblib
import requests
import numpy as np
from bs4 import BeautifulSoup
import urllib.request as urllib
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud, STOPWORDS
from flask import Flask, render_template, request
import time
from flask import Flask, request, render_template
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import requests
import nltk
import os

# Initialize Flask app
app = Flask(__name__)

# Set up NLTK
nltk.download('vader_lexicon')

# Define function to fetch YouTube comments
def returnytcomments(url):
    comments = []
    with Chrome(executable_path=r'C:\Users\NEERAJ\Desktop\YouTube-Comments-Sentiment-Analysis-main\chromedriver_win32\chromedriver.exe') as driver:
        driver.get(url)
        driver.find_element_by_tag_name("body").send_keys(Keys.END)
        while True:
            try:
                driver.find_element_by_xpath('//*[@id="continuations"]/yt-next-continuation/paper-button').click()
                driver.find_element_by_tag_name("body").send_keys(Keys.END)
            except Exception as e:
                break
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for comment in soup.select('#content-text'):
            comments.append(comment.text)
    return comments

# Define sentiment analysis function
def analyze_sentiment(comments):
    sia = SentimentIntensityAnalyzer()
    scores = [sia.polarity_scores(comment)['compound'] for comment in comments]
    return scores

# Define word cloud generation function
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate(text)
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig('static/wordcloud.png')
    plt.close()

# Define Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['GET'])
def result():
    url = request.args.get('url')
    if url:
        comments = returnytcomments(url)
        if comments:
            scores = analyze_sentiment(comments)
            avg_score = sum(scores) / len(scores)
            pos_count = len([score for score in scores if score > 0])
            neg_count = len([score for score in scores if score < 0])
            neutral_count = len([score for score in scores if score == 0])
            text = ' '.join(comments)
            generate_wordcloud(text)
            return render_template('results.html', url=url, avg_score=avg_score, pos_count=pos_count, neg_count=neg_count, neutral_count=neutral_count)
    return 'Error: Invalid URL or no comments found.'

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
