russian = 'йцукенгшщзхъфывапролджэячсмитьбю'
latin = 'qwertyuiop[]asdfghjkl;\'zxcvbnm,.'


def switch_layout(string: str):
    if not string:
        return ''
    if string[0] in russian:
        char_map = dict(zip(russian, latin))
    elif string[0] in latin:
        char_map = dict(zip(latin, russian))
    else:
        raise ValueError('Unsupported layout')
    return ''.join([char_map[letter] if letter in char_map else letter for letter in string])
