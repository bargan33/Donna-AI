
from donna_ranking import DonnaRanking
from donna_session import DonnaSession
from utils.file import save_to_json_file, parse_json_file
import os

company_reqs = '''
A person who is good at coordinating large projects, excells at teamwork and has at least some programming experience
'''


def test_init():
    if not os.path.exists('serde'):
        os.mkdir('serde')
    session_name = 'test_session'
    url = 'https://docs.google.com/forms/d/1fbog0GLT9gmdGR09MVUy13ZamgeSFr72sHioOoAi-BI/edit'
    ds = DonnaSession.create_new_session(session_name, 'serde/', url)
    ds.refresh()
    assert ds.qa[0][0][0] != ''
    dr = DonnaRanking()
    dr.init(ds, company_reqs)
    print(dr.candidates)
    assert dr.candidates[0]['full_name'] != ''
    save_to_json_file(dr.to_dict(), 'serde/' +
                      session_name + '/donna_ranking.json')
    dr2 = DonnaRanking.from_dict(parse_json_file(
        'serde/' + session_name + '/donna_ranking.json'))
    assert dr2.candidates[0]['full_name'] != ''

    DonnaSession.remove_session('serde/' + session_name)
    os.rmdir('serde')


def test_evaluate():
    if not os.path.exists('serde'):
        os.mkdir('serde')
    session_name = 'test_session'
    url = 'https://docs.google.com/forms/d/1fbog0GLT9gmdGR09MVUy13ZamgeSFr72sHioOoAi-BI/edit'
    ds = DonnaSession.create_new_session(session_name, 'serde/', url)
    ds.refresh()
    assert ds.qa[0][0][0] != ''
    dr = DonnaRanking()
    dr.init(ds, company_reqs)
    dr.evaluate()
    print(dr.candidates)
    assert dr.candidates[0]['full_name'] != ''
    assert dr.candidates[0]['total_rating'] != -1
    save_to_json_file(dr.to_dict(), 'serde/' +
                      session_name + '/donna_ranking.json')
    dr2 = DonnaRanking.from_dict(parse_json_file(
        'serde/' + session_name + '/donna_ranking.json'))
    assert dr2.candidates[0]['full_name'] != ''
    assert dr2.candidates[0]['total_rating'] != -1

    DonnaSession.remove_session('serde/' + session_name)
    os.rmdir('serde')
