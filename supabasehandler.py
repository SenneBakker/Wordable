import supabase as sb
from config import settings
from models import ListResponse, WordResponse, InputList, InputWord
from typing import List, Any


def get_supabase_connector():
    return sb.Client(settings.supabase_url, settings.supabase_key)


class SupabaseTable:
    def __init__(self, client = get_supabase_connector()):
        self.client = client

    def upsert(self, table:str, item: dict|list[dict]) -> sb.PostgrestAPIResponse:
        response = self.client.from_(table).upsert(item).execute()
        return response

    def insert(self, table:str, item: dict|list[dict]) -> sb.PostgrestAPIResponse:
        response = self.client.from_(table).insert(item).execute()
        return response

    def update_where(self, table: str, column: str, value, item: dict[str, str|int]) -> sb.PostgrestAPIResponse:
        """
        Wrapper function to update table in database. Where column equals value, change the dict.key column to dict.val value.
        :param table: table to be updated.
        :param column: Column to filter on. Ex: where id (column) = 3.
        :param value: Value for filter comparison. Ex: where id = 3 (value).
        :param item: key-value to change. Change dict.key column to dict.value value.
        :return: PostgrestAPIResponse.
        """
        response = self.client.from_(table).update(item).eq(column, value).execute()
        return response

    def delete_where(self, table:str, column: str, value) -> sb.PostgrestAPIResponse:
        response = self.client.from_(table).delete().eq(column, value).execute()
        return response

    def delete_on_ids(self, table:str, ids: List[int]) -> sb.PostgrestAPIResponse:
        response = self.client.from_(table).delete().in_(column='id', values=ids).execute()
        return response

    def list_items(self, table:str, limit = 5) -> sb.PostgrestAPIResponse:
        response = self.client.table(table).select("*").limit(limit).execute()
        return response

    def get_items_where(self, table:str, column: str, value) -> sb.PostgrestAPIResponse:
        response = self.client.table(table).select('*').eq(column, value).execute()
        return response

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

    def get_words(self, list_id: int) -> sb.PostgrestAPIResponse:
        response = self.get_items_where(self.table, 'wordlist_id', list_id)
        ## unpack into pydantic models
        return response

    def delete_words_by_id(self, id_list: List[int]):
        response = self.delete_on_ids(self.table, id_list)
        return response


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
        return response.data[0]['wordlist_id']

    def update_wordlist(self, column: str, value: Any, item:dict) -> sb.PostgrestAPIResponse:
        response = self.update_where(self.table, column, value, item)
        return response




# sb = SupabaseBucketConnector()
# id = 1234
#
# sb1 = get_supabase_connector()
# sb1.from_('words').upsert({'id':1, "language_a": 'hello', "language_b": 'ola', 'wordlist_id':str(id)}).execute()
# sb1.from_('wordlists').upsert({'name':'test'}).execute()
