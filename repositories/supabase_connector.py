import supabase as sb
from config import settings
from typing import List


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