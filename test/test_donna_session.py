from donna_session import DonnaSession
import os

comp_reqs = '''
A person who is good at coordinating large projects, excells at teamwork and has at least some programming experience
'''


def test_donna_session():
    if not os.path.exists('serde'):
        os.mkdir('serde')
    session_name = 'test_session'
    url = 'https://docs.google.com/forms/d/1fbog0GLT9gmdGR09MVUy13ZamgeSFr72sHioOoAi-BI/edit'
    ds = DonnaSession.create_new_session(
        session_name, 'serde/', url, comp_reqs)
    ds.refresh()
    assert ds.qa[0][0][0] != ''
    DonnaSession.remove_session('serde/' + session_name)
    os.rmdir('serde')
