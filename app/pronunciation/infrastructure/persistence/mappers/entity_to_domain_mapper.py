from app.pronunciation.domain.pronunciation import Pronunciation, Sentence, SentenceWord, UserSpeech

def map_entity_to_domain(pronunciation: dict) -> Pronunciation:

    return Pronunciation(
        id=str(pronunciation["_id"]),
        topic=pronunciation["topic"],
        finished=pronunciation["finished"],
        sentence=map_sentence_entity_to_domain(pronunciation["sentence"]),
        routine_id=str(pronunciation["routine_id"]) if pronunciation["routine_id"] != None else None,
        user_speech=map_user_speech(pronunciation["user_speech"])
    )

def map_sentence_entity_to_domain(user_sentence: dict) -> Sentence:
    return Sentence(
        words=[map_sentence_word_entity_to_domain(word) for word in user_sentence["words"]],
        sentence=user_sentence["sentence"],
        audio=user_sentence["audio"]
    )

def map_sentence_word_entity_to_domain(user_sentence_word: dict) -> SentenceWord:
    return SentenceWord(
        word=user_sentence_word["word"],
        wrong=user_sentence_word["wrong"],
        is_word=user_sentence_word["is_word"]
    )

def map_user_speech(user_speech: dict) -> UserSpeech:
    if user_speech is None:
        return None
    if user_speech["audio"] != None:
        return UserSpeech(
            audio=user_speech["audio"]
        )
    return None