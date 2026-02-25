from repositories.supabase_connector import SupabaseTable
from typing import List, Any 
from models.models import ListResponse
import supabase as sb
from parsers.parsers import parseIdFromResponse


class WordlistDB(SupabaseTable):
    def __init__(self):
        super().__init__()
        self.table = 'wordlists'

    def get_wordlists(self, limit = 5) -> List[ListResponse]:
        response = self.list_items(self.table, limit=limit)
        lists = []
        for alist in response.data:
            lists.append(ListResponse.model_validate(alist))
        return lists

    def get_wordlist(self, wordlist_id: int) -> sb.PostgrestAPIResponse:
        response = self.get_items_where(self.table, 'wordlist_id', wordlist_id)
        return response

    def insert_wordlist(self, item: dict) -> int:
        response = self.insert(self.table, item)
        id = parseIdFromResponse(response)
        return id

    def update_wordlist(self, column: str, value: Any, item:dict) -> sb.PostgrestAPIResponse:
        response = self.update_where(self.table, column, value, item)
        return response

    def delete_wordlist(self, id: int) -> sb.PostgrestAPIResponse:
        response = self.delete_where(self.table, 'wordlist_id', id)
        return response