# News Sentiment Analysis Application

## Overview
A web-based application that analyzes company sentiment from news articles using Google News, performs sentiment analysis, and provides insights with Hindi audio summaries.

## Features
- News article extraction from Google News
- Sentiment analysis using TextBlob
- Topic extraction using NLTK
- Comparative analysis of articles
- Hindi text-to-speech summary
- Interactive web interface

## Project Structure
```
├── app.py          # Streamlit frontend
├── api.py          # FastAPI backend
├── utils.py        # Utility functions
└── requirements.txt # Dependencies
```

## Setup Instructions

1. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the API server:
```bash
uvicorn api:app --reload
```

4. In a new terminal, start the Streamlit app:
```bash
streamlit run app.py
```

5. Access the application at http://localhost:8501

## Dependencies
- FastAPI
- Streamlit
- GoogleNews
- TextBlob
- NLTK
- gTTS
- Pandas
- Plotly

## Usage
1. Enter a company name
2. Select analysis time period (1-30 days)
3. Click "Analyze" to view:
   - Sentiment metrics
   - News articles table
   - Hindi audio summary
