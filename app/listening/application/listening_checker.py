from app.listening.domain.listening import Listening, Word

class ListeningChecker:

    def __init__(self) -> None:
        pass

    def extract_wrong_words(self, listening: Listening) -> list[Word]:
        return [word for sentence in listening.sentences for word in sentence.words if word.wrong]