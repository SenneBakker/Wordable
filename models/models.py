from pydantic import BaseModel
from typing import List

class ListResponse(BaseModel):
    id: int
    name: str
    created_at: str
    wordlist_id: int
    word_count: int

class WordResponse(BaseModel):
    id: int
    language_a: str
    language_b: str
    wordlist_id: int


class InputList(BaseModel):
    # all the other attributes are generated
    name: str
    word_count: int

class InputWord(BaseModel):
    language_a: str
    language_b: str
    wordlist_id: int


class ListOfWords:
    def __init__(self, words: List[WordResponse]) -> None:
        self.listwords = words

    def get_word_by_id(self, ind: int):
        for aword in self.listwords:
            if aword.id == ind:
                return aword
        
        raise KeyError(f"word with id {ind} not found in list.")

class PracticeSessionData(BaseModel): 
    practice_id: int
    words: list
    incorrect_words: int
    current_ind : int
    retry_counter: int
        
