from itertools import zip_longest
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from supabasehandler import WordlistDB, WordsDB
from models.models import ListResponse, WordResponse, InputList, InputWord, ListOfWords


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'


wordlists_db = WordlistDB()
words_db = WordsDB()


# Routes
@app.route('/')
def index():
    wordlists = wordlists_db.get_wordlists()
    return render_template('index.html', wordlists=wordlists)

@app.route('/wordlist/add', methods=['GET', 'POST'])
def add_wordlist():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        
        if not name:
            flash('Wordlist name is required!', 'error')
            return redirect(url_for('add_wordlist'))
            # consider changing to return render_template('add_wordlist.html'). No redirect is necessary in this case. 


        wordlist = InputList(name=name, word_count=1)
        new_id = wordlists_db.insert_wordlist({k: v for k, v in wordlist.model_dump().items() if v is not None})

        # Add words
        language_a_words = request.form.getlist('language_a[]')
        language_b_words = request.form.getlist('language_b[]')
        if len(language_a_words) != len(language_b_words):
            flash("Can't save words without translation!")

        words_to_add = []
        for lang_a, lang_b in zip(language_a_words, language_b_words):
            if lang_a.strip() and lang_b.strip():
                entry = InputWord(
                    language_a=lang_a.strip(),
                    language_b=lang_b.strip(),
                    wordlist_id=new_id
                )
                words_to_add.append(entry.model_dump())
        word_count = min(len(language_a_words), len(language_b_words))
        if word_count == 0:
            flash('At least one word pair is required!', 'error')
            return redirect(url_for('add_wordlist'))

        words_db.insert_word(words_to_add)
        flash(f'Wordlist "{name}" created successfully with {word_count} words!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_wordlist.html')

@app.route('/wordlist/edit/<int:wordlist_id>', methods=['GET', 'POST'])
def edit_wordlist(wordlist_id):
    wordlist = ListResponse.model_validate(wordlists_db.get_wordlist(wordlist_id).data[0])
    words = words_db.get_words(wordlist.id)


    if request.method == 'POST':
        name = request.form.get('name', '').strip()

        if not name:
            flash('Wordlist name is required!', 'error')
            return redirect(url_for('edit_wordlist', id=wordlist.id))

        initial_ids = {int(aword.id) for aword in words}

        word_ids = request.form.getlist('word_ids[]')
        language_a_list = request.form.getlist('language_a[]')
        language_b_list = request.form.getlist('language_b[]')

        words_to_upsert = []
        words_to_insert = []
        submitted_ids = set()

        for ind, lang_a, lang_b in zip_longest(word_ids, language_a_list, language_b_list, fillvalue=None):
            try:
                lang_a = lang_a.strip()
                lang_b = lang_b.strip()
            except AttributeError:
                app.logger.info(f"Failed to parse words in list: a: {lang_a}, b: {lang_b}. Break. ")
                break

            if lang_a and lang_b:
                # Check if it's an existing word or a brand new one
                # Handle 'new', '', or '0' as a new record
                is_new = not ind or ind == 'new' or ind == '0'

                if is_new:
                    word = InputWord(
                        language_a=lang_a,
                        language_b=lang_b,
                        wordlist_id=wordlist.id
                    )
                    words_to_insert.append(word.model_dump())
                else:
                    word_id = int(ind)
                    submitted_ids.add(word_id)
                    word = WordResponse(
                        id=word_id,
                        language_a=lang_a,
                        language_b=lang_b,
                        wordlist_id=wordlist.id
                    )
                    words_to_upsert.append(word.model_dump())

        if not words_to_upsert:
            flash('At least one word pair is required!', 'error')
            return redirect(url_for('edit_wordlist', id=wordlist.id))

        to_be_deleted = initial_ids - submitted_ids

        # Update the main list info
        wordlists_db.update_wordlist(column='wordlist_id', value=wordlist.id, item={'name': name})

        # Perform the Upsert (Updates existing, Inserts 'new' ones)
        words_db.upsert_words(words_to_upsert)
        if words_to_insert:
            words_db.insert_word(words_to_insert)

        if to_be_deleted:
            words_db.delete_words_by_id(list(to_be_deleted))

        flash(f'Wordlist "{name}" updated successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit_wordlist.html', wordlist=wordlist, words=words)

@app.route('/wordlist/delete/<int:wordlist_id>', methods=['POST'])
def delete_wordlist(wordlist_id):
    wordlists_db.delete_wordlist(id=wordlist_id)
    flash(f'Wordlist deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/practice/<int:wordlist_id>', methods=['GET', 'POST'])
def practice(wordlist_id):
    wordlist = ListResponse.model_validate(wordlists_db.get_wordlist(wordlist_id).data[0])
    words = ListOfWords(words_db.get_words(list_id=wordlist.id))
    
    if not words:
        flash('This wordlist has no words to practice!', 'error')
        return redirect(url_for('index'))


    # Initialize session data if starting new practice
    if 'practice_id' not in session or session['practice_id'] != wordlist_id:
        session['practice_id'] = wordlist_id
        session['words'] = [w.id for w in words.listwords]
        session['incorrect_words'] = []
        session['current_index'] = 0
        session['retry_count'] = 0
    
    if request.method == 'POST':
        user_answer = request.form.get('answer', '').strip().lower()
        current_word_id = session['words'][session['current_index']]
        
        # current_word = Word.query.get(current_word_id)
        current_word = words.get_word_by_id(current_word_id)
        correct_answer = current_word.language_b.strip().lower()
        
        if user_answer == correct_answer:
            flash('Correct! Well done!', 'success')
            session['retry_count'] = 0
            session['current_index'] += 1
            
            # Check if we finished all words
            if session['current_index'] >= len(session['words']):
                # If there are incorrect words, start over with those
                if session['incorrect_words']:
                    session['words'] = session['incorrect_words'][:]
                    session['incorrect_words'] = []
                    session['current_index'] = 0
                    flash('Let\'s practice the words you got wrong!', 'info')
                else:
                    # Practice complete!
                    flash('Congratulations! You completed all words!', 'success')
                    session.pop('practice_id', None)
                    session.pop('words', None)
                    session.pop('incorrect_words', None)
                    session.pop('current_index', None)
                    session.pop('retry_count', None)
                    return redirect(url_for('index'))
        else:
            session['retry_count'] += 1
            
            if session['retry_count'] == 1:
                flash(f'Incorrect. Try again! (Hint: {correct_answer[0]}...)', 'error')
            else:
                flash(f'Incorrect. The correct answer was: {current_word.language_b}', 'error')
                # Add to incorrect words if not already there
                if current_word_id not in session['incorrect_words']:
                    session['incorrect_words'].append(current_word_id)
                session['retry_count'] = 0
                session['current_index'] += 1
                
                # Check if we finished all words
                if session['current_index'] >= len(session['words']):
                    if session['incorrect_words']:
                        session['words'] = session['incorrect_words'][:]
                        session['incorrect_words'] = []
                        session['current_index'] = 0
                        flash('Let\'s practice the words you got wrong!', 'info')
                    else:
                        flash('Congratulations! You completed all words!', 'success')
                        session.pop('practice_id', None)
                        session.pop('words', None)
                        session.pop('incorrect_words', None)
                        session.pop('current_index', None)
                        session.pop('retry_count', None)
                        return redirect(url_for('index'))
        
        session.modified = True
        return redirect(url_for('practice', wordlist_id=wordlist.id))
    
    # GET request - show current word
    current_word_id = session['words'][session['current_index']]
    current_word = words.get_word_by_id(current_word_id)
    progress = {
        'current': session['current_index'] + 1,
        'total': len(session['words']),
        'incorrect_count': len(session['incorrect_words'])
    }
    
    return render_template('practice.html',
                            wordlist_id = wordlist.id, 
                            wordlist=wordlist, 
                            word=current_word, 
                            progress=progress,
                            retry=session['retry_count'] > 0)

if __name__ == '__main__':
    app.run(debug=True)