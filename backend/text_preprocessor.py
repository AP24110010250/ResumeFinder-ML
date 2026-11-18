# NLP text preprocessing functions for resume text

import re

# Standard English stopwords to remove without filtering technical keywords
STANDARD_STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
    "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
    "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
    "they've", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
    "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves"
}


def clean_text(text):
    # Remove URLs, email addresses, and unnecessary symbols while preserving skill characters
    if not text:
        return ""

    # Convert to lowercase
    cleaned = text.lower()

    # Remove URLs
    cleaned = re.sub(r"http\S+|www\.\S+", " ", cleaned)

    # Remove email addresses
    cleaned = re.sub(r"\S+@\S+", " ", cleaned)

    # Replace special symbols with spaces, preserving +, #, -, and / for terms like C++, C#, CI/CD
    cleaned = re.sub(r"[^\w\s\+\#\-\/]", " ", cleaned)

    # Replace multiple spaces with a single space
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned


def tokenize_text(text):
    # Tokenize cleaned text into words
    if not text:
        return []
    return text.split()


def remove_stopwords(tokens):
    # Remove general stopwords from token list
    if not tokens:
        return []
    return [token for token in tokens if token not in STANDARD_STOPWORDS]


def normalize_text(text):
    # Complete text normalization pipeline
    cleaned = clean_text(text)
    tokens = tokenize_text(cleaned)
    filtered_tokens = remove_stopwords(tokens)
    return " ".join(filtered_tokens)

