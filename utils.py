import pandas as pd
from GoogleNews import GoogleNews
from textblob import TextBlob
from gtts import gTTS
from datetime import datetime
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

# Download required NLTK data (quiet=True suppresses console output)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def fetch_news(keyword, days=1):
    """
    Fetch news articles from Google News for a given keyword.
    Returns a pandas DataFrame with columns like 'title', 'desc', 'date', etc.
    """
    googlenews = GoogleNews(lang='en', region='US', period=f'{days}d')
    googlenews.search(keyword)
    
    # Convert the GoogleNews results into a DataFrame
    df = pd.DataFrame(googlenews.result())
    
    # Ensure required columns exist (create them if they don't)
    required_cols = ["title", "desc", "media", "date"]
    for col in required_cols:
        if col not in df.columns:
            df[col] = ""
    
    return df

def analyze_sentiment(text):
    """
    Perform sentiment analysis using TextBlob.
    Returns a dictionary with polarity and subjectivity.
    """
    analysis = TextBlob(str(text))
    return {
        'polarity': analysis.sentiment.polarity,
        'subjectivity': analysis.sentiment.subjectivity
    }

def extract_topics(text, num_topics=5):
    """
    Extract main topics from text using NLTK.
    Splits text into words, removes stopwords, and returns a frequency distribution.
    """
    words = word_tokenize(str(text).lower())
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if w.isalnum() and w not in stop_words]
    
    fdist = FreqDist(words)
    # Return the top 'num_topics' words and their frequencies as a dictionary
    return dict(fdist.most_common(num_topics))

def compare_articles(df):
    """
    Generate a comparative (aggregated) analysis of multiple articles.
    Returns average polarity, average subjectivity, and the article count.
    """
    # If DataFrame is empty, return defaults
    if df.empty:
        return {
            'average_polarity': 0.0,
            'average_subjectivity': 0.0,
            'article_count': 0
        }
    
    # Perform sentiment analysis on each article's 'desc' column
    df['sentiment'] = df['desc'].apply(analyze_sentiment)
    df['topics'] = df['desc'].apply(extract_topics)
    
    # Calculate average polarity and subjectivity
    polarities = df['sentiment'].apply(lambda x: x['polarity'])
    subjectivities = df['sentiment'].apply(lambda x: x['subjectivity'])
    
    avg_polarity = polarities.mean() if not polarities.empty else 0.0
    avg_subjectivity = subjectivities.mean() if not subjectivities.empty else 0.0
    
    return {
        'average_polarity': avg_polarity,
        'average_subjectivity': avg_subjectivity,
        'article_count': len(df)
    }

def text_to_hindi_speech(text, filename='output.mp3'):
    """
    Convert text to Hindi speech using gTTS and save as filename.
    Returns the filename for playback.
    """
    tts = gTTS(text=text, lang='hi')
    tts.save(filename)
    return filename

def generate_report(keyword, days=1):
    """
    Generate a complete sentiment analysis report for a given keyword and time period.
    Returns a dictionary with analysis metrics and article data.
    """
    # Fetch news articles
    news_df = fetch_news(keyword, days)
    
    # Compute overall analysis
    analysis = compare_articles(news_df)
    
    # Convert DataFrame to list of dictionaries for easier JSON serialization
    articles_data = news_df.to_dict('records')
    
    # Build the final report
    report = {
        'keyword': keyword,
        'time_period': f'{days} days',
        'analysis': analysis,
        'articles': articles_data,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return report
