import sqlite3

import click
from flask import current_app, _app_ctx_stack
from flask.cli import with_appcontext


class SQLite3(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def _connect(self):
        conn = sqlite3.connect(current_app.config['SQLITE3_DATABASE'])
        conn.row_factory = current_app.config['SQLITE3_ROW_FACTORY']

        if current_app.debug:
            conn.set_trace_callback(current_app.logger.debug)

        return conn

    def _fetchmany(self, cursor, n):
        while 1:
            result = cursor.fetchmany(n)
            if not result:
                break
            yield result

    def _teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'sqlite3_db'):
            ctx.sqlite3_db.close()

    def init_app(self, app):
        app.config.setdefault('SQLITE3_DATABASE', ':memory:')
        app.config.setdefault('SQLITE3_ROW_FACTORY', sqlite3.Row)
        app.teardown_appcontext(self._teardown)
        app.cli.command('init-db')(self.init_db_command)

    @with_appcontext
    def init_db_command(self):
        """Clear the existing data and create new tables."""
        with current_app.open_resource('schema.sql', 'r') as f:
            self.connection.executescript(f.read())
        click.echo('Initialized the database.')

    @property
    def connection(self):
        """Возвращает объект соединения."""
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'sqlite3_db'):
                ctx.sqlite3_db = self._connect()
            return ctx.sqlite3_db

    def execute(self, query, args=()):
        """Выполняет запрос к БД и возвращает курсор."""
        with self.connection:
            return self.connection.execute(query, args)

    def query(self, query, args=(), one=False, many=None):
        """Выпоняет запрос на извлечение данных из БД и возвращает данные.

        Arguments:
            query (str): SQL-запрос
            args (tuple): значения параметров в запросе
            one (bool): вернуть только первую строчку из результата.
            many (int): вернуть генератор, где каждый элемент список из указанного количества строк результата.
        """
        cursor = self.execute(query, args)

        if one:
            return cursor.fetchone()

        if many is not None:
            return self._fetchmany(cursor, many)

        return cursor.fetchall()
