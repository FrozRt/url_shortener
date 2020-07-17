from flask import (
    Flask,
    abort, redirect, url_for,
    render_template, flash
)
from flask_wtf import CSRFProtect, FlaskForm
import wtforms.fields as f
import wtforms.validators as v

from .flask_sqlite3 import SQLite3


# 1. Создаем объект приложения
app = Flask(__name__)
# 2. Читаем конфигурацию
app.config.update({
    'SECRET_KEY': 'Very very very secret string',
    'SQLITE3_DATABASE': 'shortener.sqlite3',
})
# 3. Создание и инициализация расширений
CSRFProtect(app)
db = SQLite3(app)

from . import model

class Form(FlaskForm):
    original_url = f.StringField('URL-адрес для сокращения', validators=[v.InputRequired(), v.URL()])

# view, endpoint
# FLASK_APP
# FLASK_ENV=development

@app.route('/')
def index():
    return render_template(
        'index.html',
        urls=model.get_all(),
        form=Form()
    )


@app.route('/shorten', methods=['GET', 'POST'])
def shorten_url():
    form = Form() # flask.request.form
                  # formdata => request.form
                  # obj      => объект
                  # data     => данные в виде словаря

    if form.validate_on_submit():
        short_url = model.save_url(form.original_url.data)
        flash(f'Короткий URL-адрес: {short_url}')
        return redirect(url_for('index'))

    return render_template('shorten.html', form=form)


@app.route('/<short_url>')
def go(short_url):
    url = model.get_original_url(short_url)

    if url is None:
        abort(404)

    return redirect(url)
