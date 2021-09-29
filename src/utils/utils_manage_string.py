import re


def remove_whitespace_from_text(text):
    return re.sub(" +", ",", text.strip())


def convert_text_to_number_list(text):
    return [int(item) for item in text.split(",")]
