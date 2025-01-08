import random

class TopicGenerator:

    topics = ["football", "travel", "technology", "food", "music", "movies", "books", "science", "history", "art", "literature", "philosophy", "religion", "politics", "economy", "business", "environment", "health", "sports", "entertainment", "science fiction", "fantasy", "horror", "mystery", "thriller", "romance", "comedy", "animation", "manga", "anime", "video games", "movies", "music", "books", "literature", "art", "science", "technology", "environment", "health", "sports", "entertainment", "science fiction", "fantasy", "horror", "mystery", "thriller", "romance", "comedy", "animation", "manga", "anime"]

    def __init__(self) -> None:
        pass

    def random_topic(self) -> str:
        return random.choice(self.topics)
