def filter_hashtags(big_string):
    words = big_string.split()
    hashtags = set(word[1:] for word in words if word.startswith("#"))
    return hashtags

def remove_hashtag_prefix(hashtags):
    return [hashtag.lstrip("#") for hashtag in hashtags]