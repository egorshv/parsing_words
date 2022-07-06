from translate import Translator
from db_dispatcher import DbDispatcher


# data = get_data()
def write_data(data):
    translator = Translator(to_lang="ru")
    try:
        db = DbDispatcher('data.db')
        word_list = [item[1] for item in db.read_all_data('data')]
        for word in data:
            if word not in word_list:
                db.write_data({'word': word, 'translation': translator.translate(word)}, 'data')
        return 1
    except Exception as e:
        return e
