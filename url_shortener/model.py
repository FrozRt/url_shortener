from . import db
from . import converter


SQL_INSERT_URL = '''
    INSERT INTO shortener (original_url) VALUES (?)
'''
SQL_SELECT_ALL = '''
    SELECT id, original_url, created FROM shortener
'''
SQL_SELECT_URL_BY_PK = f'{SQL_SELECT_ALL} WHERE id=?'


def get_all():
    """Возвращает все URL-адреса из БД"""
    for row in db.query(SQL_SELECT_ALL):
        url = dict(row) # конвертация sqlite3.Row в словарь
        url['short_url'] = converter.make_short_url(
            url['id']
        )
        yield url


def get_url_by_pk(pk):
    """Возвращает всю информацию по указанному URL"""
    return db.query(
        SQL_SELECT_URL_BY_PK, (pk,), one=True
    )


def get_original_url(short_url):
    """Возвращает оригинальный URL по сокращенному"""
    pk = converter.inverse(short_url)
    url = get_url_by_pk(pk)
    if url:
        return url['original_url']


def save_url(original_url):
    """Сохраняет адрес в БД и возвращает сокращенный"""
    cursor = db.execute(SQL_INSERT_URL, (original_url,))
    return converter.make_short_url(cursor.lastrowid)
