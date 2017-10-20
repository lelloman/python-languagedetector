import re


def sanitize_text(text):
    text = text.lower()
    text = re.sub("\s\s+", " ", text)
    for ele in ['=', '>', '<', '"', '\t', '\n']:
        text = text.replace(ele, "")

    return text


def string_to_sequence(s):
    # return bytearray(re.sub(r'[^\w\s0-9\'-]', '', s.lower().replace('\n', ''), flags=re.UNICODE))
    return bytearray(sanitize_text(s))
