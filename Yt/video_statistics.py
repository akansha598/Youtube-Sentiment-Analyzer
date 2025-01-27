import requests

# Fetch video statistics (views, likes, comments)
def get_video_statistics(video_id, api_key):
    """
    Fetches the statistics (view count, like count, comment count) for a given YouTube video.
    
    Args:
        video_id (str): The YouTube video ID.
        api_key (str): Your YouTube Data API key.
    
    Returns:
        dict: A dictionary containing 'views', 'likes', and 'comments' counts.
    """
    url = f"https://www.googleapis.com/youtube/v3/videos"
    params = {
        'part': 'statistics',
        'id': video_id,
        'key': api_key
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            statistics = data["items"][0]["statistics"]
            return {
                "views": int(statistics.get("viewCount", 0)),
                "likes": int(statistics.get("likeCount", 0)),
                "comments": int(statistics.get("commentCount", 0))
            }
        else:
            print("No video found with the given ID.")
            return None
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None
