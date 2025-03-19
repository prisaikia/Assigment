# utils.py
import requests
from bs4 import BeautifulSoup
import nltk
from transformers import pipeline
from gtts import gTTS
import os

# Download NLTK data (for tokenization)
nltk.download('punkt')

# Initialize sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis")

def fetch_news(company_name):
    """Fetch news articles for a given company using a simple Google search scrape."""
    url = f"https://www.google.com/search?q={company_name}+news&tbm=nws"
    headers = {"User-Agent": "Mozilla/5.0"}  # To avoid getting blocked
    response = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []
    
    # Extract links (non-JS based)
    for link in soup.select('a[href*="article"]')[:10]:  # Limit to 10 articles
        title = link.get_text()
        href = link.get('href')
        if href.startswith('/url?q='):
            href = href.split('/url?q=')[1].split('&')[0]
        articles.append({"title": title, "url": href})
    return articles

def extract_content(url):
    """Extract text content from a news article URL."""
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        content = " ".join([p.get_text() for p in paragraphs])
        return content[:1000]  # Limit content length
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def summarize_text(text):
    """Simple summarization by taking first few sentences."""
    sentences = nltk.sent_tokenize(text)
    return " ".join(sentences[:2])  # Take first 2 sentences

def analyze_sentiment(text):
    """Perform sentiment analysis on text."""
    result = sentiment_analyzer(text[:512])[0]  # Limit to 512 chars for model
    label = result['label']
    if label == "POSITIVE":
        return "Positive"
    elif label == "NEGATIVE":
        return "Negative"
    else:
        return "Neutral"

def generate_tts(text, filename="output.mp3"):
    """Generate Hindi TTS from text."""
    tts = gTTS(text=text, lang='hi', slow=False)
    tts.save(filename)
    return filename

def process_articles(company_name):
    """Process articles and return structured data."""
    articles = fetch_news(company_name)
    processed_data = {"Company": company_name, "Articles": []}
    
    for article in articles:
        content = extract_content(article["url"])
        summary = summarize_text(content)
        sentiment = analyze_sentiment(content)
        
        processed_data["Articles"].append({
            "Title": article["title"],
            "Summary": summary,
            "Sentiment": sentiment,
            "Topics": ["Company News"]  # Placeholder for simplicity
        })
    
    # Comparative analysis
    sentiment_dist = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for article in processed_data["Articles"]:
        sentiment_dist[article["Sentiment"]] += 1
    
    processed_data["Comparative Sentiment Score"] = {
        "Sentiment Distribution": sentiment_dist,
        "Coverage Difference": "Varies across articles"  # Simplified
    }
    
    return processed_data