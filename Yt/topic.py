# from collections import Counter
# import re
# from sklearn.feature_extraction.text import CountVectorizer

# def extract_topics_for_next_video(comments, num_topics=5):
#     """
#     Suggest topics for the next YouTube video based on user comments.
    
#     Args:
#         comments (list of dict): List of dictionaries containing YouTube comments.
#                                  Each dictionary must have a 'comment' field.
#         num_topics (int): Number of suggested topics to extract.
        
#     Returns:
#         list: A list of suggested topics for the next video.
#     """
#     # Combine all comment text into a single string
#     all_text = " ".join([comment['comment'] for comment in comments if 'comment' in comment])
    
#     # Define suggestion trigger phrases
#     suggestion_phrases = [
#         "can you make", "you should make", "i want", "next video", 
#         "it would be great if", "please create", "i'd love to see", 
#         "could you do", "how about", "make a video on", 
#         "please make", "can you do", "you should cover", 
#         "it would be nice if", "a tutorial on", "you should try", 
#         "a video about", "i would love to see", "can you explain", 
#         "could you talk about"
#     ]

#     # Extract sentences containing suggestion phrases
#     suggestion_sentences = []
#     for phrase in suggestion_phrases:
#         suggestion_sentences += re.findall(rf"([^.]*\b{re.escape(phrase)}\b[^.]*\.)", all_text, re.IGNORECASE)

#     # Fallback to extract keywords from all comments if no suggestions are found
#     if not suggestion_sentences:
#         vectorizer = CountVectorizer(max_features=500, stop_words='english', ngram_range=(2, 3))
#         X = vectorizer.fit_transform([comment['comment'] for comment in comments if 'comment' in comment])
#         fallback_phrases = vectorizer.get_feature_names_out()
#         return fallback_phrases[:num_topics]
    
#     # Tokenize and extract bigrams/trigrams from suggestion sentences
#     phrases = []
#     for sentence in suggestion_sentences:
#         words = re.findall(r'\b\w+\b', sentence.lower())
#         for i in range(len(words) - 1):
#             phrases.append(f"{words[i]} {words[i+1]}")
#         for i in range(len(words) - 2):
#             phrases.append(f"{words[i]} {words[i+1]} {words[i+2]}")

#     # Count occurrences of each phrase
#     phrase_counts = Counter(phrases)

#     # Define stopwords to filter out generic phrases
#     stop_words = set([
#         'the', 'and', 'to', 'a', 'of', 'in', 'is', 'for', 'that', 'on', 
#         'it', 'this', 'with', 'as', 'was', 'are', 'at', 'but', 'be', 'by', 
#         'an', 'or', 'if', 'you', 'your', 'we', 'i', 'my', 'so', 'do', 'not', 
#         'have', 'has', 'will', 'can', 'all', 'just', 'there', 'make', 'video', 
#         'next', 'please', 'could', 'should', 'about', 'how', 'create', 'love', 
#         'like', 'want', 'see', 'would', 'great', 'more', 'any', 'one', 'amazing', 
#         'best', 'step', 'step-by-step', 'awesome', 'really', 'get', 'need', 
#         'explain', 'explaining', 'cover', 'discuss', 'talk', 'tutorial', 'launching', 
#         'starting', 'guide', 'skills', 'interviews', 'freelancing', 'career', 
#         'paths', 'top', 'tools', 'apps', 'public', 'speaking', 'technical', 'pros', 
#         'cons', 'personal', 'finance', 'management', 'future', 'augmented', 'reality', 
#         'productivity', 'mental', 'health', 'podcasting', 'trends', 'renewable', 
#         'energy', 'technologies', 'branding', 'building'
#     ])

#     # Filter out stopwords and meaningless phrases
#     filtered_phrases = [phrase for phrase, count in phrase_counts.items() 
#                         if not any(word in stop_words for word in phrase.split()) and count > 1]

#     # Sort phrases by frequency and return the top `num_topics` suggestions
#     sorted_phrases = sorted(filtered_phrases, key=lambda x: phrase_counts[x], reverse=True)
    
#     return sorted_phrases[:num_topics]

from collections import Counter
import re
from sklearn.feature_extraction.text import CountVectorizer

def extract_topics_for_next_video(comments, num_topics=10):
    """
    Suggest topics for the next YouTube video based on user comments.
    
    Args:
        comments (list of dict): List of dictionaries containing YouTube comments.
                                 Each dictionary must have a 'comment' field.
        num_topics (int): Number of suggested topics to extract.
        
    Returns:
        list: A list of suggested topics for the next video.
    """
    # Combine all comment text into a single string
    all_text = " ".join([comment['comment'] for comment in comments if 'comment' in comment])
    
    # Clean text: remove unwanted tokens like 'quot', 'br', and extra whitespace
    all_text = re.sub(r'\b(quot|br)\b', '', all_text, flags=re.IGNORECASE)
    all_text = re.sub(r'\s+', ' ', all_text).strip()
    
    # Define suggestion trigger phrases, including subscriber-specific phrases
    suggestion_phrases = [
    "can you make", "you should make", "i want", "next video", 
    "it would be great if", "please create", "i'd love to see", 
    "could you do", "how about", "make a video on", 
    "please make", "can you do", "you should cover", 
    "it would be nice if", "a tutorial on", "you should try", 
    "a video about", "i would love to see", "can you explain", 
    "could you talk about", "could you review", "please review", 
     "we want to see", "subscribers would love",
    "the community suggests", "our choice is", "you should include", 
    "please add", "check out", "consider reviewing", "talk about",
    "can you feature", "feature this", "my choice is", "my suggestion is",
    "can you make a recipe for", "you should make a video on", "i want to see", 
    "next video, could you do", "it would be great if you could share", 
    "please create a video on", "i'd love to see", "can you do a video about", 
    "how about doing a video on", "make a video on", "please make a video on", 
    "can you do a recipe for", "you should cover", "it would be nice if you could show", 
    "a tutorial on", "you should try making", "a video about", "i would love to see a recipe for", 
    "can you explain how to make", "could you talk about making", "could you review", 
    "please review a recipe for", "can you recommend a recipe for", "you should recommend some", 
    "can you discuss recipes for", "recommend recipes for", "next recipe video, could you make", 
    "next recipe video, how about trying", "recipe suggestions for", "suggest a recipe for", 
    "i recommend trying", "my favorite recipe is", "we want to see more recipes for", 
    "subscribers would love a video on", "the community suggests a recipe for", 
    "our choice is a recipe for", "you should include a recipe for", "please add a recipe for", 
    "check out this recipe idea", "consider reviewing a recipe for", "talk about making a recipe for", 
    "can you feature a recipe for", "feature a recipe for", "my choice is a recipe for", 
    "my suggestion is a recipe for"
    ]


    # Extract sentences containing suggestion phrases
    suggestion_sentences = []
    for phrase in suggestion_phrases:
        suggestion_sentences += re.findall(rf"([^.]*\b{re.escape(phrase)}\b[^.]*\.)", all_text, re.IGNORECASE)

    # If no sentences with suggestions are found, try to extract general topics
    if len(suggestion_sentences) / len(comments) < 0.03:
        vectorizer = CountVectorizer(max_features=1000, stop_words='english', ngram_range=(2, 3))
        X = vectorizer.fit_transform([comment['comment'] for comment in comments if 'comment' in comment])
        fallback_phrases = vectorizer.get_feature_names_out()
        return fallback_phrases[:num_topics]
    
    # Tokenize and extract bigrams/trigrams from suggestion sentences
    phrases = []
    for sentence in suggestion_sentences:
        words = re.findall(r'\b\w+\b', sentence.lower())
        for i in range(len(words) - 1):
            phrases.append(f"{words[i]} {words[i+1]}")
        for i in range(len(words) - 2):
            phrases.append(f"{words[i]} {words[i+1]} {words[i+2]}")

    # Count occurrences of each phrase
    phrase_counts = Counter(phrases)

    # Define stopwords to filter out generic phrases
    stop_words = set([
        'the', 'and', 'to', 'a', 'of', 'in', 'is', 'for', 'that', 'on', 
        'it', 'this', 'with', 'as', 'was', 'are', 'at', 'but', 'be', 'by', 
        'an', 'or', 'if', 'you', 'your', 'we', 'i', 'my', 'so', 'do', 'not', 
        'have', 'has', 'will', 'can', 'all', 'just', 'there', 'make', 'video', 
        'next', 'please', 'could', 'should', 'about', 'how', 'create', 'love', 
        'like', 'want', 'see', 'would', 'great', 'more', 'any', 'one', 'amazing', 
        'best', 'step', 'awesome', 'really', 'get', 'need', 'topic', 'ideas',
        'explain', 'talk', 'cover', 'tutorial', 'br', 'quot', 'read', 'watch', 
        'recommend', 'review', 'reviews', 'suggest', 'book', 'movie', 'movies', 
        'books', 'reading', 'watching', 'list', 'good', 'interesting', 'must', 
        'recent', 'popular', 'famous', 'latest', 'new', 'old', 'classic', 
        'community', 'feature', 'choice', 'subscribers', 'recommendation', 
        'recommendations', 'favorites', 'options', 'pick', 'include', 'add'
    ])

    # Filter out stopwords and meaningless phrases
    filtered_phrases = [phrase for phrase, count in phrase_counts.items() 
                        if not any(word in stop_words for word in phrase.split()) and count > 1]

    # Sort phrases by frequency and return the top `num_topics` suggestions
    sorted_phrases = sorted(filtered_phrases, key=lambda x: phrase_counts[x], reverse=True)
    
    return sorted_phrases[:num_topics]

