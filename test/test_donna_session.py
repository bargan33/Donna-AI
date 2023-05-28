from donna_session import DonnaSession
import os


def test_donna_session():
    if not os.path.exists('serde'):
        os.mkdir('serde')
    session_name = 'test_session'
    url = 'https://docs.google.com/forms/d/1fbog0GLT9gmdGR09MVUy13ZamgeSFr72sHioOoAi-BI/edit'
    ds = DonnaSession.create_new_session(session_name, 'serde/', url)
    ds.refresh()
    assert ds.qa[0][0][0] != ''
    DonnaSession.remove_session('serde/' + session_name)
    os.rmdir('serde')
