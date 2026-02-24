from pydantic import BaseModel

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