from repositories.supabase_connector import SupabaseTable
import supabase as sb
from typing import List
from models.models import WordResponse, ListOfWords
from parsers.parsers import parseGetwordsResponse

class WordsDB(SupabaseTable):
    def __init__(self):
        super().__init__()
        self.table = 'words'

    def insert_word(self, items: dict|list[dict]) -> sb.PostgrestAPIResponse:
        response = self.insert(self.table, items)
        return response

    def upsert_words(self, items: dict|list[dict]) -> sb.PostgrestAPIResponse:
        response = self.upsert(self.table, items)
        return response

    def get_words(self, list_id: int) -> ListOfWords:
        response = self.get_items_where(self.table, 'wordlist_id', list_id)
        unpacked_words = parseGetwordsResponse(response=response)
        
        return unpacked_words

    def delete_words_by_id(self, id_list: List[int]):
        response = self.delete_on_ids(self.table, id_list)
        return response
