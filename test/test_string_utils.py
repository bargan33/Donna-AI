import os
from utils.string import no_whitespace, extract_form_id_from_link, is_question_code, is_question_unit_tests, is_question_full_name, is_question_email, is_question_cv, is_question_phone_number


def test_no_whitespace():
    assert no_whitespace("kjhdgalskjfghslmcvnz.lka;slk")
    assert not no_whitespace("kjhdgalskjfgh slmcvnz.lka;slk")


def test_extract_form_id_from_link():
    url = 'https://docs.google.com/forms/d/1dJpjtQk6fGvpLOLiZmca9RZK4rcO_Mi7gIoH3C-faIA/edit'
    expected = '1dJpjtQk6fGvpLOLiZmca9RZK4rcO_Mi7gIoH3C-faIA'
    assert extract_form_id_from_link(url) == expected


def test_is_question_full_name():
    tc1 = '[Full Name] : dsfasdgasdfg'
    tc2 = '[coding tk] : dsfasdgasdfg'
    assert is_question_full_name(tc1)
    assert not is_question_full_name(tc2)


def test_is_question_email():
    tc1 = '[E-mail] : dsfasdgasdfg'
    tc2 = '[coding tk] : dsfasdgasdfg'
    assert is_question_email(tc1)
    assert not is_question_email(tc2)


def test_is_question_phone_number():
    tc1 = '[Phone Number] : dsfasdgasdfg'
    tc2 = '[coding tk] : dsfasdgasdfg'
    assert is_question_phone_number(tc1)
    assert not is_question_phone_number(tc2)


def test_is_question_code():
    tc1 = '[Coding Task] : dsfasdgasdfg'
    tc2 = '[coding tk] : dsfasdgasdfg'
    assert is_question_code(tc1)
    assert not is_question_code(tc2)


def test_is_question_unit_tests():
    tc1 = '[Unit Test] : dsfasdgasdfg'
    tc2 = '[Coding Tk] : dsfasdgasdfg'
    assert is_question_unit_tests(tc1)
    assert not is_question_unit_tests(tc2)


def test_is_question_cv():
    tc1 = '[CV] : dsfasdgasdfg'
    tc2 = '[Coding Tk] : dsfasdgasdfg'
    assert is_question_cv(tc1)
    assert not is_question_cv(tc2)
