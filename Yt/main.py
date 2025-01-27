
# import csv
# import requests
# from urllib.parse import urlparse, parse_qs
# from video_statistics import get_video_statistics  # Importing the new module
# from sentiment_analysis import analyze_sentiments, visualize_sentiments
# from topic import extract_topics_for_next_video

# # Replace with your actual YouTube Data API key
# API_KEY = "AIzaSyCQ2gMqPA1yC_bh_eH2KRemBzHmswx5Gwk"

# # Extract video ID from a YouTube URL
# def extract_video_id(url):
#     parsed_url = urlparse(url)
#     if parsed_url.hostname == 'youtu.be':
#         return parsed_url.path[1:]  # Extract the video ID from the path
#     elif parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
#         query_params = parse_qs(parsed_url.query)
#         return query_params.get('v', [None])[0]  # Extract the video ID from query parameters
#     return None

# # Fetch comments for the video
# def get_comments(video_id, api_key):
#     comments = []
#     url = f"https://www.googleapis.com/youtube/v3/commentThreads"
#     params = {
#         'part': 'snippet',
#         'videoId': video_id,
#         'key': api_key,
#         'maxResults': 100
#     }

#     while True:
#         response = requests.get(url, params=params)
#         if response.status_code != 200:
#             print(f"Error: {response.status_code}")
#             break

#         data = response.json()
#         for item in data.get('items', []):
#             comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
#             username = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
#             comments.append({"username": username, "comment": comment})

#         next_page_token = data.get('nextPageToken')
#         if not next_page_token:
#             break

#         params['pageToken'] = next_page_token

#     return comments

# # Save comments to a CSV file
# def save_to_csv(comments, filename='youtube_comments.csv'):
#     with open(filename, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=["username", "comment"])
#         writer.writeheader()
#         for comment in comments:
#             writer.writerow(comment)

# # Main function
# if __name__ == "__main__":
#     youtube_url = input("Enter the YouTube Video URL: ")
#     video_id = extract_video_id(youtube_url)

#     if video_id:
#         # Fetch video statistics
#         stats = get_video_statistics(video_id, API_KEY)
#         if stats:
#             print(f"Video Statistics:")
#             print(f"Views: {stats['views']}")
#             print(f"Likes: {stats['likes']}")
#             print(f"Comments: {stats['comments']}")

#         # Fetch and save comments
#         comments = get_comments(video_id, API_KEY)
#         save_to_csv(comments)
#         print(f"Comments saved to 'youtube_comments.csv'.")

#          # Perform Sentiment Analysis
#         sentiments, sentiment_details = analyze_sentiments(comments)
#         print(f"Sentiment Analysis Results: {sentiments}")

#         # Visualize Sentiment Distribution
#         visualize_sentiments(sentiments)

#                 # Extract Topics
#         topics = extract_topics_for_next_video(comments, num_topics=5)
#         print("\nTop 5 Topics from Comments:")
#         for idx, topic in enumerate(topics, 1):
#             print(f"{idx}. {topic}")

#     else:
#         print("Invalid YouTube URL.")

from flask import Flask, request, jsonify
import csv
import requests
from urllib.parse import urlparse, parse_qs
from video_statistics import get_video_statistics
from sentiment_analysis import analyze_sentiments, visualize_sentiments
from topic import extract_topics_for_next_video

from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Replace with your actual YouTube Data API key
API_KEY = "AIzaSyCQ2gMqPA1yC_bh_eH2KRemBzHmswx5Gwk"

# Extract video ID from a YouTube URL
def extract_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]  # Extract the video ID from the path
    elif parsed_url.hostname in ("www.youtube.com", "youtube.com"):
        query_params = parse_qs(parsed_url.query)
        return query_params.get("v", [None])[0]  # Extract the video ID from query parameters
    return None

# Fetch comments for the video
def get_comments(video_id, api_key):
    comments = []
    url = f"https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "part": "snippet",
        "videoId": video_id,
        "key": api_key,
        "maxResults": 100,
    }

    while True:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        data = response.json()
        for item in data.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            username = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
            comments.append({"username": username, "comment": comment})

        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break

        params["pageToken"] = next_page_token

    return comments

@app.route("/analyze", methods=["POST"])
def analyze_video():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debugging line
        youtube_url = data.get("url")
        print("YouTube URL:", youtube_url)  # Debugging line

        if not youtube_url:
            return jsonify({"error": "YouTube URL is required"}), 400

        video_id = extract_video_id(youtube_url)
        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400

        # Fetch video statistics
        stats = get_video_statistics(video_id, API_KEY)
        if not stats:
            return jsonify({"error": "Failed to fetch video statistics"}), 500

        # Fetch comments
        comments = get_comments(video_id, API_KEY)
        if not comments:
            return jsonify({"error": "Failed to fetch comments"}), 500

        # Perform sentiment analysis
        sentiments, sentiment_details = analyze_sentiments(comments)

        # Extract topics from comments
        topics = extract_topics_for_next_video(comments, num_topics=5)

        # Prepare the response
        result = {
            "statistics": stats,
            "sentiments": {
                "positive": sentiments.get("positive", 0),
                "negative": sentiments.get("negative", 0),
                "neutral": sentiments.get("neutral", 0),
            },
            "comments": [{"username": c["username"], "comment": c["comment"]} for c in comments[:10]],
            "topics": topics,
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
