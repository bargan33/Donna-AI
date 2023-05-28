import re


def no_whitespace(string: str):
    pattern = r'\s'
    if re.search(pattern, string):
        return False
    else:
        return True


def extract_form_id_from_link(url: str) -> str:
    pattern = r"(?<=forms\/d\/)[^\/]*"
    match = re.search(pattern, url)
    return match.group(0) if match else None


def is_question_full_name(question: str):
    return '[Full Name]' in question


def is_question_email(question: str):
    return '[E-mail]' in question


def is_question_phone_number(question: str):
    return '[Phone Number]' in question


def is_question_code(question: str):
    return '[Coding Task]' in question


def is_question_unit_tests(question: str):
    return '[Unit Test]' in question


def is_question_cv(question: str):
    return '[CV]' in question
