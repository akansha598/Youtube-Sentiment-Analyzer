import requests
from transformers import TFAutoModelForSequenceClassification, AutoTokenizer
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os

# Load the pre-trained DistilBERT model and tokenizer
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
try:
    model = TFAutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    print(f"Model '{model_name}' and tokenizer loaded successfully!")
except Exception as e:
    print(f"Error loading model or tokenizer: {e}")
    exit()

# Function to analyze sentiments
def analyze_sentiments(comments):
    """
    Analyze the sentiments of a list of YouTube comments using DistilBERT.

    Args:
        comments (list of dict): List of dictionaries containing YouTube comments. 
                                 Each dictionary must have a 'comment' field.

    Returns:
        tuple: 
            - A dictionary containing sentiment counts (positive, negative).
            - A list of detailed sentiment analysis for each comment.
    """
    sentiments = {'positive': 0, 'negative': 0}
    sentiment_details = []

    for comment in comments:
        try:
            # Extract the comment text and username
            comment_text = comment.get('comment', '')
            username = comment.get('username', 'Anonymous')

            # Skip empty comments
            if not comment_text:
                continue

            # Tokenize and preprocess input
            inputs = tokenizer(comment_text, return_tensors="tf", truncation=True, padding=True)
            outputs = model(inputs.input_ids)
            scores = tf.nn.softmax(outputs.logits, axis=1).numpy()[0]
            label = np.argmax(scores)  # 0: Negative, 1: Positive
            confidence = scores[label]

            # Determine sentiment and update counts
            if label == 1:  # Positive
                sentiments['positive'] += 1
                sentiment = "positive"
            else:  # Negative
                sentiments['negative'] += 1
                sentiment = "negative"

            # Append detailed sentiment results
            sentiment_details.append({
                'username': username,
                'comment': comment_text,
                'sentiment': sentiment,
                'score': round(confidence, 4)
            })
        except Exception as e:
            print(f"Error processing comment: {comment}. Error: {e}")
            continue

    return sentiments, sentiment_details

# Function to visualize sentiments
def visualize_sentiments(sentiments):
    """
    Visualize the sentiment analysis results as a pie chart.

    Args:
        sentiments (dict): Dictionary containing sentiment counts (positive, negative).
    """
    try:
        labels = sentiments.keys()
        sizes = sentiments.values()

        plt.figure(figsize=(8, 6))
        plt.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=140,
            colors=['#28a745', '#dc3545']
        )
        plt.axis('equal')  # Ensure the pie chart is circular
        plt.title('Sentiment Analysis of YouTube Comments (DistilBERT)')

        # Save or display the plot
        if not os.environ.get('DISPLAY', ''):  # Check if display is not supported
            plt.savefig('sentiment_analysis_pie_chart.png')
            print("No display detected. Saved pie chart as 'sentiment_analysis_pie_chart.png'.")
        else:
            plt.show()

    except Exception as e:
        print(f"Error visualizing sentiments: {e}")