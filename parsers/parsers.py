import supabase as sb
from typing import List
from models.models import WordResponse, ListOfWords


def parseGetwordsResponse(response: sb.PostgrestAPIResponse) -> ListOfWords:
        rawList = response.data
        unpackedList = []

        for aword in rawList:
            unpackedList.append(WordResponse.model_validate(aword))
        
        return ListOfWords(unpackedList)

def parseIdFromResponse(response: sb.PostgrestAPIResponse) -> int:
    try: 
        id = response.data[0]['wordlist_id']
        return id
    except KeyError as e:
        print(f"no id found in response. ")
        return -1