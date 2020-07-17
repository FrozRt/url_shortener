from string import digits, ascii_letters
from flask import url_for

valid_values = tuple(digits + ascii_letters)
radix = len(valid_values)

def make_short_url(pk):
    """Создает и возвращает абсолютный короткий URL-адрес"""
    return url_for('go', short_url=convert(pk), _external=True)

def convert(number):
    """Переводит число из 10 в нашу СС"""
    if not isinstance(number, int):
        raise ValueError('Number must be integer type.')

    result = []

    while number:
        result.append(valid_values[number % radix])
        number //= radix

    result.reverse()

    return ''.join(result)


def inverse(number):
    """Переводит число из нашей в 10 СС"""
    if not isinstance(number, str):
        raise ValueError('inverse() argument must be string type.')

    result = 0

    for p, i in enumerate(reversed(number)):
        if i not in valid_values:
            raise ValueError(f'invalid literal "{i}" for inverse()')
        n = valid_values.index(i)
        result += n * radix ** p

    return result
