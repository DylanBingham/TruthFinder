# removing strange characters
def clean_encoding(text):
    text = text = text.replace('â€˜', "'").replace('â€™', "'").replace('â€œ', '"').replace('â€', '"')
    text = text.replace('â€“', '–').replace('â€”', '—').replace('â€', '')
    return text