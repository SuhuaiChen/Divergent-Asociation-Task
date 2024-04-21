letter_map = {
        'Á': 'A',
        'É': 'E',
        'Í': 'I',
        'Ú': 'U',
        'Ü': 'U',
        'Ó': 'O',
        'á': 'a',
        'é': 'e',
        'í': 'i',
        'ú': 'u',
        'ü': 'u',
        'ó': 'o',
        # 'ñ': 'n',
        # 'Ñ': 'N',
    }

def normalize(text):
    new_text = ""
    for s in text:
        new_text = new_text + letter_map[s] if s in letter_map else new_text + s
    return new_text
