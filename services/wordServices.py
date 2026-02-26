from flask import current_app, flash, redirect, url_for, render_template
from werkzeug.datastructures import ImmutableMultiDict
from models.models import InputList, InputWord, ListResponse
from repositories.word_repository import WordsDB
from repositories.wordlist_repository import WordlistDB
from typing import List, Tuple

class NoNameException(BaseException):
    pass 


class WordService:
    def __init__(self) -> None:
        self.wordRepo = WordsDB()
        self.wordlistRepo = WordlistDB()

    
    def insert_wordlist(self, form: ImmutableMultiDict):
        name = form.get('name', '').strip()
        if not name:
            raise NoNameException('No name found when adding wordlist')

        wordlist = InputList(name=name, word_count=1)
        try:
            new_id = self.wordlistRepo.insert_wordlist(wordlist.model_dump())
        except TimeoutError as e: # just an example - never had timeouterror before. 
            current_app.logger.error(f"Supabase connection timed out when trying to add new wordlist to db. Error: {e}")
            raise Exception("something went wrong uploading to database.")
        words_to_add, count = self._extract_word_pairs(form=form, list_id=new_id)


        try: 
            self.wordRepo.insert_word(words_to_add)
        except TimeoutError as e: 
            raise Exception("something went wrong uploading to database.")            
        flash(f'Wordlist "{name}" created successfully with {count} words!', 'success')
        

    def delete_wordlist(self, wordlist_id):
        self.wordlistRepo.delete_wordlist(id=wordlist_id)

    def get_wordlist(self, wordlist_id):
        response = self.wordlistRepo.get_wordlist(wordlist_id)
        wordlist = ListResponse.model_validate(response.data[0])
        return wordlist


    def _extract_word_pairs(self, form: ImmutableMultiDict, list_id: int) -> Tuple[List[dict], int]:
               # Add words
        language_a_words = form.getlist('language_a[]')
        language_b_words = form.getlist('language_b[]')
        if len(language_a_words) != len(language_b_words):
            flash("Can't save words without translation!")

        words_to_add = []
        for lang_a, lang_b in zip(language_a_words, language_b_words):
            if lang_a.strip() and lang_b.strip(): # is this line even necessary? zip already skips empty lines. 
                entry = InputWord(
                    language_a=lang_a.strip(),
                    language_b=lang_b.strip(),
                    wordlist_id=list_id
                )
                words_to_add.append(entry.model_dump())
        return words_to_add, len(words_to_add)
